#!/usr/local/bin/php
<?php declare(ticks = 1);

$stdin = fopen('php://stdin', 'r');

// echo "COMMUNICATION STARTED\n PID :: " . getmypid() . "\n\n";

$servername = "localhost";
$username = "root";
$password = "password";
$dbname = "mining";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

while(true) {
    sleep( 5 );
    $readers = array($fifoFile, $stdin);
    if (($stream = stream_select( $readers, $writers, $except, 0, 15 )) === false) {
        print "A stream error occurred\n";
        break;
    } else {
        $line = fgets($stdin); // I think were going to make this a search function

        $sql = "INSERT INTO messages (sender, type, time, content)
        VALUES ('John', 'type1', '2017-01-01', 'TESTING')";

        if ($conn->query($sql) === TRUE) {
            echo "New record created successfully";
        } else {
            echo "Error: " . $sql . "<br>" . $conn->error;
        }

        echo $line;
    }
}
$conn->close();
