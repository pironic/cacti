<?php
// put this file on your remote server and then use the url in the script config.
error_reporting(0);

if (ini_get('disable_functions')) {
	$disabled_funcs=array_map('trim',explode(',',ini_get('disable_functions')));
}

$action=$_GET["action"];


$users[0]="Unavailable";
$users[1]="--";
$loadnow="Unavailable";
$load15="--";
$load30="--";
if (in_array('exec',$disabled_funcs)) {
	$load=file_get_contents("/proc/loadavg");
	$load=explode(' ',$load);
	$loadnow=$load[0];
	$load15=$load[1];
	$load30=$load[2];
} else {
	$reguptime=trim(exec("uptime"));
	if ($reguptime) {
		if (preg_match("/, *(\d) (users?), .*: (.*), (.*), (.*)/",$reguptime,$uptime)) {
			$users[0]=$uptime[1];
			$users[1]=$uptime[2];
			$loadnow=$uptime[3];
			$load15=$uptime[4];
			$load30=$uptime[5];
		}
	}
}
if (in_array('shell_exec',$disabled_funcs)) {
	$uptime_text=file_get_contents("/proc/uptime");
	$uptime=substr($uptime_text,0,strpos($uptime_text," "));
} else {
	$uptime=shell_exec("cut -d. -f1 /proc/uptime");
}
$days=floor($uptime/60/60/24);
$hours=str_pad($uptime/60/60%24,2,"0",STR_PAD_LEFT);
$mins=str_pad($uptime/60%60,2,"0",STR_PAD_LEFT);
$secs=str_pad($uptime%60,2,"0",STR_PAD_LEFT);
$phpver=phpversion();
$mysqlver=mysql_get_client_info();
$zendver=zend_version();
echo "name:cerato users:".$users[0];
//echo " users1:".$users[1];
echo " load1:".$loadnow;
echo " load5:".$load15;
echo " load15:".$load30;
echo " uptime:\"{$days} Days {$hours}:{$mins}:{$secs}\" ";
echo "\eof";

?>