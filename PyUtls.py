import os
from datetime import datetime
from typing import Optional
import platform
import shutil
from time import sleep as wait
import threading as thr

platform = platform.platform().split("-")[0]
columns = shutil.get_terminal_size().columns
lines = int(round(shutil.get_terminal_size().lines/2, 0))



os.system('')

now = datetime.now()

threads = []


class colors:
    CEND      = '\33[0m'
    CBOLD     = '\33[1m'
    CITALIC   = '\33[3m'
    CURL      = '\33[4m'
    CBLINK    = '\33[5m'
    CBLINK2   = '\33[6m'
    CSELECTED = '\33[7m'

    CBLACK  = '\33[30m'
    CRED    = '\33[31m'
    CGREEN  = '\33[32m'
    CYELLOW = '\33[33m'
    CBLUE   = '\33[34m'
    CVIOLET = '\33[35m'
    CBEIGE  = '\33[36m'
    CWHITE  = '\33[37m'

    CBLACKBG  = '\33[40m'
    CREDBG    = '\33[41m'
    CGREENBG  = '\33[42m'
    CYELLOWBG = '\33[43m'
    CBLUEBG   = '\33[44m'
    CVIOLETBG = '\33[45m'
    CBEIGEBG  = '\33[46m'
    CWHITEBG  = '\33[47m'

    CGREY    = '\33[90m'
    CRED2    = '\33[91m'
    CGREEN2  = '\33[92m'
    CYELLOW2 = '\33[93m'
    CBLUE2   = '\33[94m'
    CVIOLET2 = '\33[95m'
    CBEIGE2  = '\33[96m'
    CWHITE2  = '\33[97m'

    CGREYBG    = '\33[100m'
    CREDBG2    = '\33[101m'
    CGREENBG2  = '\33[102m'
    CYELLOWBG2 = '\33[103m'
    CBLUEBG2   = '\33[104m'
    CVIOLETBG2 = '\33[105m'
    CBEIGEBG2  = '\33[106m'
    CWHITEBG2  = '\33[107m'

class projectDetails:
    owner = ''
    projectName = ''
    version = ''


class settings:
    printCap = True
    timeColor = colors.CVIOLET2
    logo = ''
    logoColor = colors.CWHITE2
    logoOnClear = False
    centerLogo = False
    startanimadelay = .1
    startmsg = ''
    logoAnim = True
    logoAnimDelay = .01


def current_time():
    return f'{colors.CGREY}[{colors.CEND}{settings.timeColor}{now.strftime("%H:%M:%S")}{colors.CEND}{colors.CGREY}]{colors.CEND}'

def logo():
    if settings.logoAnim == True:
        if settings.centerLogo:
            for line in settings.logo.split('\n'):
                wait(settings.logoAnimDelay)
                print(settings.logoColor+line.center(columns)+colors.CEND)
                
        else:
            wait(settings.logoAnimDelay)
            print(settings.logoColor+settings.logo+colors.CEND)
    else:
        if settings.centerLogo:
            for line in settings.logo.split('\n'):
                print(settings.logoColor+line.center(columns)+colors.CEND)
        else:
            print(settings.logoColor+settings.logo+colors.CEND)

def animLogo(delay:int):
    if settings.centerLogo:
        for line in settings.logo.split('\n'):
            wait(delay)
            print(settings.logoColor+line.center(columns)+colors.CEND)
            
    else:
        wait(delay)
        print(settings.logoColor+settings.logo+colors.CEND)

def startUp(waitForDone:bool):
    def main():
        for i in range(lines):
            print()
            wait(settings.startanimadelay)


        print(colors.CWHITE2+settings.startmsg.center(columns)+colors.CEND+'\n')
        for line in settings.logo.split('\n'):
            wait(settings.startanimadelay)
            print(settings.logoColor+line.center(columns)+colors.CEND)
        print(f'{colors.CWHITE2}{projectDetails.projectName} - Made by: {projectDetails.owner}'.center(columns))
        wait(settings.startanimadelay)
        print(f'v{projectDetails.version}{colors.CEND}'.center(columns))

        for i in range(lines):
            print()
            wait(settings.startanimadelay)
        wait(1)
        clear()


    if waitForDone == True:
        startUpThr = thr.Thread(target=main)
        startUpThr.name = 'startup'
        threads.append(startUpThr)
        startUpThr.start()
        startUpThr.join()
        
    else:
        startUpThr = thr.Thread(target=main)
        startUpThr.name = 'startup'
        threads.append(startUpThr)
        startUpThr.start()

def waitForStartup():
    for i in threads:
        if i.name == 'startup':
            i.join()

def error(why):
    waitForStartup()
    print(f'{current_time()} {colors.CBOLD+colors.CREDBG2}ERROR{colors.CEND+colors.CWHITE}: {colors.CBOLD+colors.CRED2+str(why)}{colors.CEND}')

def warn(why, solve: Optional = None) ->  None:
    waitForStartup()
    if not solve:
        print(f'{current_time()} {colors.CBOLD+colors.CYELLOWBG}WARNING{colors.CEND+colors.CWHITE}: {colors.CBOLD+colors.CYELLOW2+why+colors.CEND}')
    else:
        print(f'{current_time()} {colors.CBOLD+colors.CYELLOWBG}WARNING{colors.CEND+colors.CWHITE}: {colors.CBOLD+colors.CYELLOW2+str(why)+colors.CEND} - {colors.CITALIC+colors.CYELLOW+str(solve)+colors.CEND}')

def success(message):
    waitForStartup()
    print(f'{current_time()} {colors.CBOLD+colors.CGREENBG}SUCCESS{colors.CEND+colors.CWHITE}: {colors.CBOLD+colors.CGREEN+str(message)+colors.CEND}')

def fail(message):
    waitForStartup()
    print(f'{current_time()} {colors.CBOLD+colors.CREDBG}FAIL{colors.CEND+colors.CWHITE}: {colors.CBOLD+colors.CRED2+str(message)+colors.CEND}')

def binput(ask):
    waitForStartup()
    return input(f'{current_time()} {colors.CWHITE+ask+colors.CEND}')

def bprint(message: Optional = None) -> None:
    waitForStartup()
    if message:
        if settings.printCap:
            print(f'{current_time()} {colors.CBOLD+colors.CWHITE+str(message).capitalize()}')
        else:
            print(f'{current_time()} {colors.CBOLD+colors.CWHITE+message}')
    else:
        print()

def clear():
    if platform == "Windows":
        import os
        os.system("cls")
        if settings.logoOnClear:
            logo()
    elif platform == "Linux":
        try:
            import os
            os.system("clear")
            if settings.logoOnClear:
                logo()
        except:
            import replit
            replit.clear()
            if settings.logoOnClear:
                logo()


# def makeMenu(**opts):
#     for opt,do in opts.items():
#         print(f'This {opt} has to do {do}')