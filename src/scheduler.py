import schedule
import time
import threading
import logging
import json
import os
import asyncio
import inspect
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

# Configure logging
logger = logging.getLogger(__name__)

class SchedulerManager:
    def __init__(self, persistence_file=None):
        self.running = False
        self.thread = None
        self.jobs = {}  # Dictionary to map chat_id to their scheduled jobs
        self.daily_jobs = [] # List of timezone-aware daily jobs
        self.loop = None
        
        if persistence_file:
            self.persistence_file = persistence_file
        else:
            # Default to ./data/scheduled_jobs.json relative to this file
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.persistence_file = os.path.join(base_dir, "data", "scheduled_jobs.json")
            
        self.loaded_data = self._load_persistence()

    def set_loop(self, loop):
        self.loop = loop

    def _load_persistence(self):
        if os.path.exists(self.persistence_file):
            try:
                with open(self.persistence_file, 'r') as f:
                    data = json.load(f)
                if not isinstance(data, dict):
                    logger.warning(f"Persistence file has incorrect format (expected dict, got {type(data)}). Ignoring old data.")
                    return {}
                return data
            except json.JSONDecodeError:
                logger.warning("Persistence file is empty or malformed. Starting fresh.")
                return {}
            except Exception as e:
                logger.error(f"An unexpected error occurred while loading persistence file: {e}")
                return {}
        return {}

    def _save_persistence(self):
        try:
            # Ensure directory exists
            directory = os.path.dirname(self.persistence_file)
            if not os.path.exists(directory):
                os.makedirs(directory)

            with open(self.persistence_file, 'w') as f:
                json.dump(self.loaded_data, f, indent=4)
        except Exception as e:
            logger.error(f"Error saving persistence file: {e}")

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run_pending, daemon=True)
            self.thread.start()
            logger.info("Scheduler started.")

    def _run_pending(self):
        while self.running:
            schedule.run_pending()
            self._check_daily_jobs()
            time.sleep(1)

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
            logger.info("Scheduler stopped.")

    def _check_daily_jobs(self):
        # Get current UTC time once per iteration
        now_utc = datetime.now(timezone.utc)
        
        # DEBUG: Heartbeat every 30 seconds to verify scheduler is alive
        if now_utc.second % 30 == 0:
            logger.info(f"⏰ Scheduler Heartbeat: UTC is {now_utc.strftime('%H:%M:%S')}. Monitoring {len(self.daily_jobs)} jobs.")
        
        for job in self.daily_jobs:
            try:
                if job['timezone'] == 'UTC':
                    tz = timezone.utc
                else:
                    tz = ZoneInfo(job['timezone'])
                # Convert UTC now to user's timezone
                now_tz = now_utc.astimezone(tz)
                
                target_hour, target_minute = map(int, job['time'].split(':'))
                
                # DEBUG: Log if we are in the same hour, to see if minutes are mismatching
                if now_utc.second == 0 and now_tz.hour == target_hour:
                     logger.info(f"🔍 Checking Job '{job['city']}': Target {job['time']} vs Current {now_tz.strftime('%H:%M')} (TZ: {job['timezone']})")

                # Check if times match (ignoring seconds)
                if now_tz.hour == target_hour and now_tz.minute == target_minute:
                    today_str = now_tz.strftime("%Y-%m-%d")
                    
                    # Ensure it runs only once per day
                    if job.get('last_run') != today_str:
                        logger.info(f"✅ Triggering job for {job['city']} at {now_tz.strftime('%H:%M')}!")
                        job['last_run'] = today_str
                        
                        # Update persistence data to match runtime data
                        str_chat_id = str(job['chat_id'])
                        if str_chat_id in self.loaded_data:
                            for p_job in self.loaded_data[str_chat_id]:
                                if p_job.get('city') == job['city'] and p_job.get('time') == job['time']:
                                    p_job['last_run'] = today_str
                                    break
                        self._save_persistence()

                        # Run the job function
                        if inspect.iscoroutinefunction(job['func']):
                            if self.loop:
                                asyncio.run_coroutine_threadsafe(job['func'](), self.loop)
                            else:
                                logger.error(f"Cannot run async job for {job['city']}: No event loop set.")
                        else:
                            threading.Thread(target=job['func']).start()
                    elif now_utc.second == 0:
                        logger.info(f"ℹ️ Job for {job['city']} already ran today ({today_str}).")
            except Exception as e:
                logger.error(f"Error checking daily job for {job.get('chat_id')}: {e}")

    def load_jobs(self, job_func):
        count = 0
        for chat_id_str, job_list in self.loaded_data.items():
            try:
                chat_id = int(chat_id_str)
            except ValueError:
                chat_id = chat_id_str

            for job_data in job_list:
                city = job_data.get("city")
                time_str = job_data.get("time")
                timezone_str = job_data.get("timezone", "UTC")
                last_run = job_data.get("last_run")
                
                if city and time_str:
                    if self._schedule_internal(chat_id, city, time_str, job_func, timezone_str, last_run):
                        count += 1
        logger.info(f"Restored {count} jobs from persistence.")

    def _schedule_internal(self, chat_id, city, time_str, job_func, timezone_str="UTC", last_run=None):
        try:
            if inspect.iscoroutinefunction(job_func):
                async def job_wrapper():
                    logger.info(f"Running scheduled job for {chat_id} - {city}")
                    try:
                        await job_func(chat_id, city)
                    except Exception as e:
                        logger.error(f"Error executing job for {chat_id}: {e}")
            else:
                def job_wrapper():
                    logger.info(f"Running scheduled job for {chat_id} - {city}")
                    try:
                        job_func(chat_id, city)
                    except Exception as e:
                        logger.error(f"Error executing job for {chat_id}: {e}")

            # Add to internal list instead of schedule library
            job_entry = {
                'chat_id': chat_id,
                'city': city,
                'time': time_str,
                'timezone': timezone_str,
                'func': job_wrapper,
                'last_run': last_run
            }
            
            self.daily_jobs.append(job_entry)
            return True
        except Exception as e:
            logger.error(f"Error scheduling job internal: {e}")
            return False

    def add_daily_job(self, chat_id, city, time_str, job_func, timezone_str="UTC"):
        if self._schedule_internal(chat_id, city, time_str, job_func, timezone_str):
            # Persistence logic
            str_chat_id = str(chat_id)
            if str_chat_id not in self.loaded_data:
                self.loaded_data[str_chat_id] = []
            
            # Remove existing job for same city if exists (update)
            self.loaded_data[str_chat_id] = [
                job for job in self.loaded_data[str_chat_id] 
                if job.get('city') != city
            ]
            
            self.loaded_data[str_chat_id].append({"city": city, "time": time_str, "timezone": timezone_str, "last_run": None})
            self._save_persistence()
            
            logger.info(f"Scheduled daily news for {chat_id} in {city} at {time_str} ({timezone_str})")
            return True
        return False

    def remove_daily_job(self, chat_id, city):
        # Update persistence
        str_chat_id = str(chat_id)
        removed = False
        if str_chat_id in self.loaded_data:
            original_count = len(self.loaded_data[str_chat_id])
            self.loaded_data[str_chat_id] = [
                job for job in self.loaded_data[str_chat_id] 
                if job.get('city') != city
            ]
            if len(self.loaded_data[str_chat_id]) < original_count:
                self._save_persistence()
                removed = True
        
        # Update runtime jobs list (daily_jobs)
        self.daily_jobs = [job for job in self.daily_jobs if not (job['chat_id'] == chat_id and job['city'] == city)]

        if removed:
            logger.info(f"Removed daily news for {chat_id} in {city}")
            return True
        return False

# Global instance
scheduler_manager = SchedulerManager()

def parse_time(time_str):
    formats = ["%H:%M", "%I:%M%p", "%I:%M %p"]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(time_str.upper(), fmt)
            return dt.strftime("%H:%M")
        except ValueError:
            continue
    return None

def handle_dailynews_logic(chat_id, args, job_callback):
    if len(args) < 2:
        return False, None, None

    # Check for timezone in the last argument
    timezone_str = "UTC"
    possible_tz = args[-1]
    
    try:
        if possible_tz == "UTC":
            timezone_str = possible_tz
            args = args[:-1]
        else:
            ZoneInfo(possible_tz)
            timezone_str = possible_tz
            args = args[:-1] # Pop timezone
    except Exception:
        pass # Last arg is not a timezone

    if len(args) < 2:
        return False, None, None

    raw_time = args[-1]
    city = " ".join(args[:-1])
    
    formatted_time = parse_time(raw_time)
    
    if not formatted_time:
        return False, None, None

    success = scheduler_manager.add_daily_job(chat_id, city, formatted_time, job_callback, timezone_str)
    
    if success:
        return True, city, formatted_time
    else:
        return False, None, None