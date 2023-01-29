import PyUtls as utils


def install(module):
    import os
    utils.bprint(f'{module} not found installing...')
    os.system(f'pip install {module}')
    utils.success(f'Installed {module}')


utils.bprint('looking for uninstalled modules')
try:
    import selenium
except ModuleNotFoundError:
    install('selenium')

try:
    import bs4
except ModuleNotFoundError:
    install('bs4')

try:
    import requests
except ModuleNotFoundError:
    install('requests')

utils.success('Done')
