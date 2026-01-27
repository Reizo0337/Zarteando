<?php
$logs_file = '../src/data/logs.txt';

if (file_exists($logs_file)) {
    // Disable caching to ensure we always get the latest logs
    header("Cache-Control: no-store, no-cache, must-revalidate, max-age=0");
    header("Cache-Control: post-check=0, pre-check=0", false);
    header("Pragma: no-cache");
    header("Content-Type: text/plain");

    echo file_get_contents($logs_file);
}
?>
