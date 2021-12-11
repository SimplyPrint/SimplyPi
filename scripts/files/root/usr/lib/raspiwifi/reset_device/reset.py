import os
import re
import time
import subprocess
import reset_lib

pi_map = {'Raspberry Pi Zero 2 W Rev 1.0': 'PiZero2'}

counter = 0
cpuinfo = subprocess.check_output(['cat', '/proc/cpuinfo']).decode('utf-8')

serial_match = re.search(r"Serial\s+:\s(\S+)$", cpuinfo, re.MULTILINE)
if serial_match:
    serial_last_four = serial_match.group(1)[-4:]
else:
    serial_last_four = '0000'

model_info_match = re.search(r"Model\s+:\s(.+)$", cpuinfo, re.MULTILINE)
if model_info_match:
    model_info = pi_map[model_info_match.group(1).strip()]
else:
    model_info = 'unknown'

config_hash = reset_lib.config_file_hash()
ssid_prefix = config_hash['ssid_prefix'].strip()
reboot_required = False

reboot_required = reset_lib.wpa_check_activate(config_hash['wpa_enabled'], config_hash['wpa_key'])

reboot_required = reset_lib.update_ssid(ssid_prefix, serial_last_four, model_info)

if reboot_required == True:
    os.system('reboot')

