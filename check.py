import re
import requests
import threading
import PyUtls as utils
from datetime import datetime

file_name = utils.binput('File name: ')

valid = 0
invalid = 0

utils.bprint('Started')

def check_and_write(script):
    global valid, invalid
    match = re.search(r'"(https?://.*?)"', script)
    url = None
    if match:
        url = match.group(1)
    else:
        match = re.search(r'"(https?://.*?)"', script)
        if match:
            url = match.group(1)
    
    try:
        response = requests.get(url)
        if response.status_code != 404:
            with open(f"valid_links.txt", "a") as f:
                f.write(script + "\n")
                utils.success(script)
                valid += 1
        else:
            utils.error(script)
            invalid += 1

    except Exception as ex:
        print(ex)
        pass

with open(file_name) as f:
    scripts = [line.strip() for line in f]

threads = [threading.Thread(target=check_and_write, args=(string,)) for string in scripts]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

utils.bprint(f'Ended. Vaild: {valid} Invalid: {invalid}')