import re
import requests
import PyUtls as utils

utils.bprint('Started')

def check_and_write(script, name):
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
            with open(f"valid_links {name}.txt", "a") as f:
                f.write(script + "\n")
                utils.success(script)
        else:
            utils.error(script)

    except Exception as ex:
        print(ex)
        pass