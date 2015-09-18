<?php

$stateJSON = $_POST["stateJSON"];

$fileName = "stateJSON";
$i = 1;
while (file_exists("../JSONOutputs/$fileName.json")) {
	$fileName = "stateJSON" . $i;
	echo $fileName;
	$i++;
}
echo "finished";
echo $fileName;

$fp = fopen("../JSONOutputs/$fileName.json", "w");

fwrite($fp, $stateJSON);
fclose($fp);

?>