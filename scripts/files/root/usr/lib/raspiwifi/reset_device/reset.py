import os
import re
import subprocess
import reset_lib

pi_map = {'Raspberry Pi Zero 2 W Rev 1.0': 'PiZero2',
          'Raspberry Pi 3 Model B Rev 1.2': 'Pi3B',
          'Raspberry Pi 3 Model B Plus Rev 1.3': 'Pi3B+',
          'Raspberry Pi 4 Model B Rev 1.2': 'Pi4B',
          'Raspberry Pi 4 Model B Rev 1.1': 'Pi4B',
          'Raspberry Pi 4 Model B Rev 1.4': 'Pi4B',
          'Raspberry Pi 2 Model B Rev 1.1': 'Pi2B',
          'Raspberry Pi Zero W Rev 1.1': 'PiZero',
          'Raspberry Pi Zero 2 Rev 1.0': 'PiZero2',
          'Raspberry Pi 3 Model A Plus Rev 1.0': 'Pi3A',
          'Raspberry Pi Model B Rev 2': 'Pi1B',
          'Raspberry Pi Model B Plus Rev 1.2': 'Pi1B+',
          'Raspberry Pi 400 Rev 1.0': 'Pi400',
          'Hardkernel Odroid XU4': 'OdroidXU4',
          'Raspberry Pi Compute Module 3 Plus Rev 1.0': 'PiCompute3+',
          'Xunlong Orange Pi Zero': 'OrangePiZero',
          'Xunlong Orange Pi PC': 'OrangePiPC'
          }

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

if reboot_required:
    os.system('reboot')
