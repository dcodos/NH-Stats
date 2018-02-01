#!/usr/local/bin/php
<?php


# Count from 1 to 10 with a sleep
for ($count = 1; $count <= 10; $count++) {
	echo $count . "\n";
	usleep(500000);
}
?>
// declare(ticks = 1);
//
// $stdin = fopen('php://stdin', 'r');
//
// // echo "COMMUNICATION STARTED\n PID :: " . getmypid() . "\n\n";
//
// $servername = "localhost";
// $username = "root";
// $password = "password";
// $dbname = "mining";
//
// // Create connection
// $conn = new mysqli($servername, $username, $password, $dbname);
// // Check connection
// if ($conn->connect_error) {
//     die("Connection failed: " . $conn->connect_error);
// }
//
// while(true) {
//   sleep(5);
//   echo "Testing";
// }
// while(true) {
    // sleep( 5 );
    //     $line = fgets($stdin); // I think were going to make this a search function
    //
    //     $sql = "INSERT INTO messages (sender, type, time, content)
    //     VALUES ('John', 'type1', '2017-01-01', 'TESTING')";
    //
    //     if ($conn->query($sql) === TRUE) {
    //         echo "New record created successfully";
    //     } else {
    //         echo "Error: " . $sql . "<br>" . $conn->error;
    //     }
    //
    //     echo $line;
// }
// $conn->close();
