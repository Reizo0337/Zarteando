import schedule
import time
import threading
import logging
import json
import os
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)

class SchedulerManager:
    def __init__(self, persistence_file="scheduled_jobs.json"):
        self.running = False
        self.thread = None
        self.jobs = {}  # Dictionary to map chat_id to their scheduled jobs
        self.persistence_file = persistence_file
        self.loaded_data = self._load_persistence()

    def _load_persistence(self):
        if os.path.exists(self.persistence_file):
            try:
                with open(self.persistence_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading persistence file: {e}")
                return {}
        return {}

    def _save_persistence(self):
        try:
            with open(self.persistence_file, 'w') as f:
                json.dump(self.loaded_data, f, indent=4)
        except Exception as e:
            logger.error(f"Error saving persistence file: {e}")

    def start(self):
        """Starts the scheduler in a separate thread."""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run_pending, daemon=True)
            self.thread.start()
            logger.info("Scheduler started.")

    def _run_pending(self):
        while self.running:
            schedule.run_pending()
            time.sleep(1)

    def stop(self):
        """Stops the scheduler."""
        self.running = False
        if self.thread:
            self.thread.join()
            logger.info("Scheduler stopped.")

    def load_jobs(self, job_func):
        """Loads and schedules jobs from the persistence file."""
        count = 0
        for chat_id_str, job_list in self.loaded_data.items():
            try:
                chat_id = int(chat_id_str)
            except ValueError:
                chat_id = chat_id_str

            for job_data in job_list:
                city = job_data.get("city")
                time_str = job_data.get("time")
                if city and time_str:
                    if self._schedule_internal(chat_id, city, time_str, job_func):
                        count += 1
        logger.info(f"Restored {count} jobs from persistence.")

    def _schedule_internal(self, chat_id, city, time_str, job_func):
        try:
            def job_wrapper():
                logger.info(f"Running scheduled job for {chat_id} - {city}")
                try:
                    job_func(chat_id, city)
                except Exception as e:
                    logger.error(f"Error executing job for {chat_id}: {e}")

            # Schedule the job
            # schedule.every().day.at(time_str) expects HH:MM or HH:MM:SS
            tag = f"{chat_id}_{city}"
            job = schedule.every().day.at(time_str).do(job_wrapper).tag(tag)
            
            if chat_id not in self.jobs:
                self.jobs[chat_id] = []
            self.jobs[chat_id].append(job)
            return True
        except Exception as e:
            logger.error(f"Error scheduling job internal: {e}")
            return False

    def add_daily_job(self, chat_id, city, time_str, job_func):
        """
        Schedules a daily job for a specific chat and city at a given time.
        """
        if self._schedule_internal(chat_id, city, time_str, job_func):
            # Persistence logic
            str_chat_id = str(chat_id)
            if str_chat_id not in self.loaded_data:
                self.loaded_data[str_chat_id] = []
            
            # Check for duplicates
            exists = False
            for job in self.loaded_data[str_chat_id]:
                if job.get('city') == city and job.get('time') == time_str:
                    exists = True
                    break
            
            if not exists:
                self.loaded_data[str_chat_id].append({"city": city, "time": time_str})
                self._save_persistence()
            
            logger.info(f"Scheduled daily news for {chat_id} in {city} at {time_str}")
            return True
        return False

    def remove_daily_job(self, chat_id, city):
        """Removes all daily jobs for a specific city and chat_id."""
        tag = f"{chat_id}_{city}"
        schedule.clear(tag)
        
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
        
        # Update runtime jobs list
        if chat_id in self.jobs:
            self.jobs[chat_id] = [job for job in self.jobs[chat_id] if tag not in job.tags]

        if removed:
            logger.info(f"Removed daily news for {chat_id} in {city}")
            return True
        return False

# Global instance
scheduler_manager = SchedulerManager()

def parse_time(time_str):
    """
    Attempts to parse a time string into HH:MM format (24-hour).
    Supports: HH:MM, H:MM, HH:MMAM/PM, H:MMAM/PM
    """
    formats = ["%H:%M", "%I:%M%p", "%I:%M %p"]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(time_str.upper(), fmt)
            return dt.strftime("%H:%M")
        except ValueError:
            continue
    return None

def handle_dailynews_logic(chat_id, args, job_callback):
    """
    Logic for the /dailynews command.
    
    :param chat_id: Telegram chat ID.
    :param args: List of arguments (e.g. ["Madrid", "8:00AM"]).
    :param job_callback: Function to execute when schedule triggers.
    :return: Tuple (success, city, formatted_time)
    """
    if len(args) < 2:
        return False, None, None

    raw_time = args[-1]
    city = " ".join(args[:-1])
    
    formatted_time = parse_time(raw_time)
    
    if not formatted_time:
        return False, None, None

    success = scheduler_manager.add_daily_job(chat_id, city, formatted_time, job_callback)
    
    if success:
        return True, city, formatted_time
    else:
        return False, None, None