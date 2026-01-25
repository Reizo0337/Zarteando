<?php
require_once __DIR__ . '/vendor/autoload.php';

$dotenv = Dotenv\Dotenv::createImmutable(__DIR__ . '/../');
$dotenv->load();

// File paths
$users_file = '../data/user_preferences.json';
$logs_file = '../data/logs.txt';
$bot_file = '../src/bot.py';


// Get user count
$user_count = 0;
if (file_exists($users_file)) {
    $users_data = json_decode(file_get_contents($users_file), true);
    if ($users_data) {
        $user_count = count($users_data);
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
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NewsPodBot Admin Panel</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>Admin Panel</h1>

        <div class="card">
            <h2>Statistics</h2>
            <p><strong>Total Users:</strong> <?php echo $user_count; ?></p>
        </div>

        <div class="card">
            <h2>Send Global Message</h2>
            <form action="index.php" method="post">
                <textarea name="message" rows="4" placeholder="Enter your message here..."></textarea>
                <button type="submit" name="send_message">Send Message</button>
            </form>
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
    <script src="script.js"></script>
</body>
</html>
