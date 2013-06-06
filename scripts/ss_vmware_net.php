<?php $no_http_headers = true; /* display No errors */ error_reporting(0); include_once(dirname(__FILE__) . "/../lib/snmp.php"); if 
(!isset($called_by_script_server)) {
	include_once(dirname(__FILE__) . "/../include/config.php");
	array_shift($_SERVER["argv"]);
	print call_user_func_array("ss_vmware_esx_net", $_SERVER["argv"]);
}
function ss_vmware_esx_net($hostname, $host_id, $snmp_auth, $cmd, $arg1 = "", $arg2 = "") {
	$snmp = explode(":", $snmp_auth);
	$snmp_version = $snmp[0];
	$snmp_port = $snmp[1];
	$snmp_timeout = $snmp[2];
	$snmpv3_auth_username = "";
	$snmpv3_auth_password = "";
	$snmpv3_auth_protocol = "";
	$snmpv3_priv_passphrase = "";
	$snmpv3_priv_protocol = "";
	$snmp_community = "";
	if ($snmp_version == 3) {
		$snmpv3_auth_username = $snmp[4];
		$snmpv3_auth_password = $snmp[5];
		$snmpv3_auth_protocol = $snmp[6];
		$snmpv3_priv_passphrase = $snmp[7];
		$snmpv3_priv_protocol = $snmp[8];
	}else{
		$snmp_community = $snmp[3];
	}
	$oids = array(
	        "ifaddr" => ".1.3.6.1.4.1.6876.3.4.1.4",
	        "netname" => ".1.3.6.1.4.1.6876.3.4.1.2",
	        "pktstx" => ".1.3.6.1.4.1.6876.3.4.1.6",
	        "kbtx" => ".1.3.6.1.4.1.6876.3.4.1.7",
	        "vmid" => ".1.3.6.1.4.1.6876.2.1.1.7",
	        "displayname" => ".1.3.6.1.4.1.6876.2.1.1.2",
	        "netvmid" => ".1.3.6.1.4.1.6876.3.4.1.3",
	        "index" => ".1.3.6.1.4.1.6876.3.4.1.1",
	        "pktsrx" => ".1.3.6.1.4.1.6876.3.4.1.8",
	        "kbrx" => ".1.3.6.1.4.1.6876.3.4.1.9"
		);
	if ($cmd == "index") {
		$return_arr = ss_vmware_esx_net_reindex(cacti_snmp_walk($hostname, $snmp_community, $oids["index"], $snmp_version, $snmpv3_auth_username, 
$snmpv3_auth_password, $snmp_port, $snmp_timeout, read_config_option("snmp_retries"), SNMP_POLLER));
		for ($i=0;($i<sizeof($return_arr));$i++) {
			print $return_arr[$i] . "\n";
		}
	}elseif ($cmd == "query") {
		$arg = $arg1;
		$arr_index = ss_vmware_esx_net_reindex(cacti_snmp_walk($hostname, $snmp_community, $oids["index"], $snmp_version, $snmpv3_auth_username, 
$snmpv3_auth_password, $snmp_port, $snmp_timeout, read_config_option("snmp_retries"), SNMP_POLLER));
		
		if ($arg == "index") {
			for ($i=0;($i<sizeof($arr_index));$i++) {
                        	print $arr_index[$i] . "!" . $arr_index[$i] . "\n";
			}
			
		}elseif ($arg == "vmid") {
			$arr_netvmid = ss_vmware_esx_net_reindex(cacti_snmp_walk($hostname, $snmp_community, $oids["netvmid"], $snmp_version, 
$snmpv3_auth_username, $snmpv3_auth_password, $snmp_port, $snmp_timeout, read_config_option("snmp_retries"), SNMP_POLLER));
	                for ($i=0;($i<sizeof($arr_index));$i++) {
       	                        print $arr_index[$i] . "!" . $arr_netvmid[$i] . "\n";
	                }
		
		}elseif ($arg == "displayname" || $arg == "netreference") {
			$arr = ss_vmware_esx_net_vmid_reindex(cacti_snmp_walk($hostname, $snmp_community, $oids["displayname"], $snmp_version, 
$snmpv3_auth_username, $snmpv3_auth_password, $snmp_port, $snmp_timeout, read_config_option("snmp_retries"), SNMP_POLLER));
			$arr_vmid = ss_vmware_esx_net_vmid_reindex(cacti_snmp_walk($hostname, $snmp_community, $oids["vmid"], $snmp_version, 
$snmpv3_auth_username, $snmpv3_auth_password, $snmp_port, $snmp_timeout, read_config_option("snmp_retries"), SNMP_POLLER));
			$combination = array();
	                for ($i=0;($i<sizeof($arr));$i++) {
        	                $combination[$arr_vmid[$i]] = $arr[$i];
	                }
			$arr_netvmid = ss_vmware_esx_net_reindex(cacti_snmp_walk($hostname, $snmp_community, $oids["netvmid"], $snmp_version, 
$snmpv3_auth_username, $snmpv3_auth_password, $snmp_port, $snmp_timeout, read_config_option("snmp_retries"), SNMP_POLLER));
			if ($arg == "netreference") {
				$arr_netname = ss_vmware_esx_net_reindex(cacti_snmp_walk($hostname, $snmp_community, $oids["netname"],	$snmp_version, 
$snmpv3_auth_username, $snmpv3_auth_password, $snmp_port, $snmp_timeout, read_config_option("snmp_retries"), SNMP_POLLER));
                        }
			for ($i=0;($i<sizeof($arr_index));$i++) {
                                if ($arg == "netreference") {
                                        if (isset($combination[$arr_netvmid[$i]])) {
                                                print $arr_index[$i] . "!" . $combination[$arr_netvmid[$i]] . "/" . $arr_netname[$i] . "\n";
                                        } else {
                                                print $arr_index[$i] . "!console" . "/" . $arr_netname[$i] . "\n";
                                        }
                                } else {
		                        if (isset($combination[$arr_netvmid[$i]])) {
        		                        print $arr_index[$i] . "!" . $combination[$arr_netvmid[$i]] . "\n";
	        	                } else {
	                	                print $arr_index[$i] . "!console\n";
	                        	}
				}
	                }
		}else {
			$arr = ss_vmware_esx_net_reindex(cacti_snmp_walk($hostname, $snmp_community, $oids[$arg], $snmp_version, $snmpv3_auth_username, 
$snmpv3_auth_password, $snmp_port, $snmp_timeout, read_config_option("snmp_retries"), SNMP_POLLER));
			for ($i=0;($i<sizeof($arr_index));$i++) {
				print $arr_index[$i] . "!" . $arr[$i] . "\n";
			}
		}
	}elseif ($cmd == "get") {
		$arg = $arg1;
		$index = $arg2;
		if ($arg != "displayname" && $arg != "netreference") {
			return cacti_snmp_get($hostname, $snmp_community, $oids[$arg] . ".$index", $snmp_version, $snmpv3_auth_username, 
$snmpv3_auth_password, $snmp_port, $snmp_timeout, read_config_option("snmp_retries"), SNMP_POLLER);
		}else {
			/* get VM ID from the snmp cache since it is faster */
			$vmid = eregi_replace("[^0-9]", "", db_fetch_cell("select field_value from host_snmp_cache where host_id=$host_id and 
field_name='vmID' and snmp_index=$index"));
			if (!$vmid || $vmid == -1) {
				return "U";
			}
			$result = cacti_snmp_get($hostname, $snmp_community, $oids["displayname"] . ".$vmid", $snmp_version, $snmpv3_auth_username, 
$snmpv3_auth_password, $snmp_port, $snmp_timeout, read_config_option("snmp_retries"), SNMP_POLLER);
                        if ($arg == "netreference") {
                                $result .= "/" . cacti_snmp_get($hostname, $snmp_community, $oids["netname"] . ".$index", $snmp_version,
 $snmpv3_auth_username, $snmpv3_auth_password, $snmp_port, $snmp_timeout, read_config_option("snmp_retries"), SNMP_POLLER);
                        }
                        return $result;
		}
	}
}
function ss_vmware_esx_net_reindex($arr) {
	$return_arr = array();
	for ($i=0;($i<sizeof($arr));$i++) {
		$return_arr[$i] = $arr[$i]["value"];
	}
	return $return_arr;
}
function ss_vmware_esx_net_vmid_reindex($arr) {
        $return_arr = array();
        for ($i=0;($i<sizeof($arr));$i++) {
                if (ereg("\.([0-9]+)$", $arr[$i]["oid"], $regs)) {
                        $return_arr[$regs[1]] = $arr[$i]["value"];
                }
        }
        return $return_arr;
}
?>
