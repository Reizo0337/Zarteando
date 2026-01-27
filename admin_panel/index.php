<?php
require_once __DIR__ . '/vendor/autoload.php';

$dotenv = Dotenv\Dotenv::createImmutable(__DIR__ . '/../');
$dotenv->load();

// File paths
$users_file = '../src/data/user_preferences.json';
$logs_file = '../src/data/logs.txt';
$bot_file = '../src/bot.py';
$scheduled_jobs_file = '../src/data/scheduled_jobs.json';


// Get user count
$user_count = 0;
if (file_exists($users_file)) {
    $users_data = json_decode(file_get_contents($users_file), true);
    if ($users_data) {
        $user_count = count($users_data);
    }
}

// Get statistics
$easy_commands = 0;
$podcast_generations = 0;
$summary_generations = 0;

if (file_exists($logs_file)) {
    $logs_content = file_get_contents($logs_file);
    $log_entries = explode("\n", $logs_content);
    $one_month_ago = strtotime('-1 month');

    foreach ($log_entries as $entry) {
        if (trim($entry) === '') {
            continue;
        }

        preg_match('/\[(.*?)\]/', $entry, $matches);
        if (isset($matches[1])) {
            $log_date = strtotime($matches[1]);
            if ($log_date >= $one_month_ago) {
                if (strpos($entry, 'requested help') !== false) {
                    $easy_commands++;
                } elseif (strpos($entry, 'Generated podcast script') !== false || strpos($entry, 'Generated audio') !== false) {
                    $podcast_generations++;
                } elseif (strpos($entry, 'Sent daily summary') !== false || strpos($entry, 'requested a summary') !== false) {
                    $summary_generations++;
                }
            }
        }
    }
}

// Get logs
$logs = '';
if (file_exists($logs_file)) {
    $logs = file_get_contents($logs_file);
}


// Clear logs
if (isset($_POST['clear_logs'])) {
    if (file_exists($logs_file)) {
        file_put_contents($logs_file, '');
    }
    header("Location: index.php");
    exit();
}

// Handle Scheduled Jobs Actions
if (isset($_POST['update_job']) || isset($_POST['delete_job'])) {
    if (file_exists($scheduled_jobs_file)) {
        $jobs_data = json_decode(file_get_contents($scheduled_jobs_file), true);
        if ($jobs_data) {
            $chat_id = $_POST['chat_id'];
            $job_index = $_POST['job_index'];

            if (isset($jobs_data[$chat_id][$job_index])) {
                if (isset($_POST['delete_job'])) {
                    array_splice($jobs_data[$chat_id], $job_index, 1);
                    if (empty($jobs_data[$chat_id])) {
                        unset($jobs_data[$chat_id]);
                    }
                } elseif (isset($_POST['update_job'])) {
                    $jobs_data[$chat_id][$job_index]['city'] = $_POST['city'];
                    $jobs_data[$chat_id][$job_index]['time'] = $_POST['time'];
                    $jobs_data[$chat_id][$job_index]['timezone'] = $_POST['timezone'];
                }
                file_put_contents($scheduled_jobs_file, json_encode($jobs_data, JSON_PRETTY_PRINT));
            }
        }
    }
    header("Location: index.php");
    exit();
}

// Send global message
if (isset($_POST['send_message']) && !empty($_POST['message'])) {
    $message = $_POST['message'];
    $user_ids = [];
    if (file_exists($users_file)) {
        $users_data = json_decode(file_get_contents($users_file), true);
        if ($users_data) {
            $user_ids = array_keys($users_data);
        }
    }

    $bot_token = $_ENV['TELEGRAM_BOT_TOKEN'];

    if ($bot_token && !empty($user_ids)) {
        $url = "https://api.telegram.org/bot{$bot_token}/sendMessage";
        foreach ($user_ids as $user_id) {
            $data = [
                'chat_id' => $user_id,
                'text' => $message
            ];
            $options = [
                'http' => [
                    'header'  => "Content-type: application/x-www-form-urlencoded\r\n",
                    'method'  => 'POST',
                    'content' => http_build_query($data),
                ],
            ];
            $context  = stream_context_create($options);
            file_get_contents($url, false, $context);
        }
    }
    header("Location: index.php");
    exit();
}

// Run diagnostics
$diagnostics_output = '';
if (isset($_POST['run_diagnostics'])) {
    $pythonScript = realpath(__DIR__ . '/../src/check_services.py');
    if ($pythonScript && file_exists($pythonScript)) {
        $cmd = "python " . escapeshellarg($pythonScript) . " 2>&1";
        $diagnostics_output = shell_exec($cmd);
    } else {
        $diagnostics_output = "Error: Could not locate check_services.py";
    }
}

// Get Scheduled Jobs
$scheduled_jobs = [];
if (file_exists($scheduled_jobs_file)) {
    $data = json_decode(file_get_contents($scheduled_jobs_file), true);
    if ($data) {
        $scheduled_jobs = $data;
    }
}

// --- ANALYTICS PARSING ---
$podcasts_per_day = [];
$popular_cities = [];
$popular_topics = [];
$tts_times = [];
$last_tts_start = null;

if (file_exists($logs_file)) {
    $lines = file($logs_file, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    foreach ($lines as $line) {
        // Regex to capture timestamp and message: [YYYY-MM-DD HH:MM:SS.mmmmmm] Message
        if (preg_match('/^\[(.*?)\]\s*(.*)$/', $line, $matches)) {
            $ts_str = $matches[1];
            $msg = $matches[2];
            
            try {
                $dt = new DateTime($ts_str);
                $date = $dt->format('Y-m-d');
                $timestamp = (float)$dt->format('U.u');
            } catch (Exception $e) { continue; }

            // 1. Usage (Podcasts Generated)
            if (strpos($msg, 'Sent podcast to user') !== false) {
                if (!isset($podcasts_per_day[$date])) $podcasts_per_day[$date] = 0;
                $podcasts_per_day[$date]++;
            }

            // 2. Popular Cities
            if (preg_match('/requested a podcast for city:\s*(.*)\.$/i', $msg, $city_matches)) {
                $city = ucwords(strtolower(trim($city_matches[1])));
                if (!isset($popular_cities[$city])) $popular_cities[$city] = 0;
                $popular_cities[$city]++;
            }

            // 3. Popular Topics
            if (preg_match('/has interests:\s*\[(.*?)\]/i', $msg, $topic_matches)) {
                $topics_raw = str_replace(["'", '"'], '', $topic_matches[1]);
                foreach (explode(',', $topics_raw) as $t) {
                    $t = ucfirst(strtolower(trim($t)));
                    if (!empty($t)) {
                        if (!isset($popular_topics[$t])) $popular_topics[$t] = 0;
                        $popular_topics[$t]++;
                    }
                }
            }

            // 4. TTS Production Times
            if (strpos($msg, 'Generating audio from script') !== false) {
                $last_tts_start = $timestamp;
            } elseif (strpos($msg, 'Audio generated at') !== false) {
                if ($last_tts_start !== null) {
                    $duration = $timestamp - $last_tts_start;
                    if ($duration > 0 && $duration < 600) $tts_times[] = round($duration, 2);
                    $last_tts_start = null;
                }
            }
        }
    }
}

ksort($podcasts_per_day);
arsort($popular_cities);
arsort($popular_topics);

$avg_tts = count($tts_times) > 0 ? round(array_sum($tts_times) / count($tts_times), 2) : 0;

$chart_data = [
    'dates' => array_keys($podcasts_per_day),
    'counts' => array_values($podcasts_per_day),
    'cities' => array_keys(array_slice($popular_cities, 0, 10)),
    'city_counts' => array_values(array_slice($popular_cities, 0, 10)),
    'topics' => array_keys(array_slice($popular_topics, 0, 10)),
    'topic_counts' => array_values(array_slice($popular_topics, 0, 10)),
    'avg_tts' => $avg_tts
];
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NewsPodBot Admin Panel</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>Admin Panel</h1>

        <div class="card">
            <h2>Analytics Dashboard</h2>
            <div class="charts-grid">
                <div class="chart-container full-width">
                    <canvas id="usageChart"></canvas>
                </div>
                <div class="chart-container">
                    <canvas id="citiesChart"></canvas>
                </div>
                <div class="chart-container">
                    <canvas id="topicsChart"></canvas>
                </div>
                <div class="stat-box">
                    <h3>Avg Audio Generation Time</h3>
                    <p class="big-number"><?php echo $avg_tts; ?>s</p>
                </div>
            </div>
        </div>

        <div class="card">
            <h2>Statistics</h2>
            <p><strong>Total Users:</strong> <?php echo $user_count; ?></p>
        </div>

        <div class="card">
            <h2>Monthly Statistics</h2>
            <p><strong>Easy Commands:</strong> <?php echo $easy_commands; ?></p>
            <p><strong>Podcast Generations:</strong> <?php echo $podcast_generations; ?></p>
            <p><strong>Summary Generations:</strong> <?php echo $summary_generations; ?></p>
        </div>

        <div class="card">
            <h2>Send Global Message</h2>
            <form action="index.php" method="post">
                <textarea name="message" rows="4" placeholder="Enter your message here..."></textarea>
                <button type="submit" name="send_message">Send Message</button>
            </form>
        </div>

        <div class="card">
            <h2>Service Diagnostics</h2>
            <form action="index.php" method="post">
                <button type="submit" name="run_diagnostics" class="diagnostics-btn">Run System Checks</button>
            </form>
            <?php if ($diagnostics_output): ?>
                <div class="diagnostics-output">
                    <?php echo htmlspecialchars($diagnostics_output); ?>
                </div>
            <?php endif; ?>
        </div>

        <div class="card">
            <h2>Scheduled Jobs</h2>
            <div style="overflow-x: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>Chat ID</th>
                            <th>City</th>
                            <th>Time</th>
                            <th>Timezone</th>
                            <th>Last Run</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($scheduled_jobs as $chat_id => $jobs): ?>
                            <?php foreach ($jobs as $index => $job): ?>
                                <tr>
                                    <form action="index.php" method="post">
                                        <td><?php echo htmlspecialchars($chat_id); ?></td>
                                        <td><input type="text" name="city" value="<?php echo htmlspecialchars($job['city']); ?>"></td>
                                        <td><input type="text" name="time" value="<?php echo htmlspecialchars($job['time']); ?>"></td>
                                        <td><input type="text" name="timezone" value="<?php echo htmlspecialchars($job['timezone'] ?? 'UTC'); ?>"></td>
                                        <td><?php echo htmlspecialchars($job['last_run'] ?? '-'); ?></td>
                                        <td>
                                            <input type="hidden" name="chat_id" value="<?php echo htmlspecialchars($chat_id); ?>">
                                            <input type="hidden" name="job_index" value="<?php echo $index; ?>">
                                            <button type="submit" name="update_job" class="btn-small">Save</button>
                                            <button type="submit" name="delete_job" class="btn-small btn-danger">Delete</button>
                                        </td>
                                    </form>
                                </tr>
                            <?php endforeach; ?>
                        <?php endforeach; ?>
                        <?php if (empty($scheduled_jobs)): ?>
                            <tr><td colspan="6" style="text-align:center;">No scheduled jobs found.</td></tr>
                        <?php endif; ?>
                    </tbody>
                </table>
            </div>
        </div>

        <div class="card">
            <h2>Logs</h2>
            <form action="index.php" method="post" class="clear-logs-form">
                <button type="submit" name="clear_logs">Clear Logs</button>
            </form>
            <div class="logs-container">
                <pre><?php echo htmlspecialchars($logs); ?></pre>
            </div>
        </div>
    </div>
    <script>
        window.chartData = <?php echo json_encode($chart_data); ?>;
    </script>
    <script src="script.js"></script>
</body>
</html>
