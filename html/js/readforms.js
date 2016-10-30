/* Custom JS file
 This provides all the fuctions for reading forms on the Pi Data Logger
 */
 
function getSerial() {
	var serial = document.forms["piData"]["sn"].value;
	window.alert("this is the serial number you entered " + serial);
	document.getElementById('sn').value=serial;
	return;
/*	document.cookie("serialNumber", serial, Sun, 15 Jul 2100 00:00:01 GMT); */
}





/*
If you want to save the form data on the server side, I would do it with php like this: 
<?php
$action = $_GET["action"];
$myText = $_POST["mytext"];

if($action = "save") {
  $targetFolder = "/path/to/folder";
  file_put_contents($targetFolder."mytext.txt", $myText);
}
?>   
<html>
<head>
 <title>myform</title>
</head>
<body>
  <form action="?action=save" name="myform" method="post">
    <input type=text name="mytext">
    <input type="submit" value="save">
  </form>
</body>
</html>

*/