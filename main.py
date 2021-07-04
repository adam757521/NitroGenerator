import NitroChecker
import time
import colorama
from colorama import Fore
import os


colorama.init()


def pad_to_center(l: list, w: int) -> str:
    return '\n'.join([' ' * (w // 2 - (len(max(l, key=len)) // 2)) + x for x in l])


def print_nitro():
    text = f'''{Fore.CYAN}
@@@@@@@@@@@@@@@@@@@################################@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@#######################################@@@@@@@@@@@@@
((((((((((((((((((@@########################################%@@@@@@@@@
(((((((((((((((((((((((((((((@%########////////////############@@@@@@@
((((&&((((((((%&&&&&&&&&&&&&@@#####/////%@@@@@@@@&/////##########@@@@@
(@@****@@(((@###################(///&@&            ,@@////########@@@@
@@@@@@@@((((@@@@@@@@@@@@@######///@@                  @@///########@@@
@@@@@@@&(((((((((((((((((@####///@      ,,,,,,,,,,      @///########@@
######((((((((((((@@@@@@@%###///@(    ,,,,,,,,,,,,,,     @///#######@@
((((((((((((((((%@###########///@    ,,,,,,,,,,,,,,,,    @///#######@@
((((((((((((((((((@@@@#######///@/    .,,,,,,,,,,,,.     @///#######@@
&&&&&&&&&&(((((((((((@########///@      ,,,,,,,,,,      @///########@@
@@@@@@@@@@%&(((((((((#@########///@@                  @@///########@@@
@@@@    @@@&&(((((((((#@########(///&@@            @@@////########@@@@
@@@@@@@@@@&&((((((((((((@&#########/////(@@@@@@@@#/////##########@@@@@
&&&&&&&&&&(((((((((((((((#@############(///////////############@@@@@@@
(((((((((((((((( (( ((((((((@@##############################@@@@@@@@@@
(((((((((((((((((**((((((((((((@@########################@@@@@@@@@@@@@
&&&&&&&&&((&&&(((((((((((((((((((((@@@@%##########%@@@@@@@@@@@@@@@@@@@{Fore.WHITE}
    '''.replace('@', ' ')

    width = os.get_terminal_size().columns
    print(pad_to_center(text.splitlines(), width))


def print_title():
    text = f'''{Fore.CYAN}
░█████╗░██████╗░░█████╗░███╗░░░███╗██╗░██████╗  ███╗░░██╗██╗████████╗██████╗░░█████╗░
██╔══██╗██╔══██╗██╔══██╗████╗░████║╚█║██╔════╝  ████╗░██║██║╚══██╔══╝██╔══██╗██╔══██╗
███████║██║░░██║███████║██╔████╔██║░╚╝╚█████╗░  ██╔██╗██║██║░░░██║░░░██████╔╝██║░░██║
██╔══██║██║░░██║██╔══██║██║╚██╔╝██║░░░░╚═══██╗  ██║╚████║██║░░░██║░░░██╔══██╗██║░░██║
██║░░██║██████╔╝██║░░██║██║░╚═╝░██║░░░██████╔╝  ██║░╚███║██║░░░██║░░░██║░░██║╚█████╔╝
╚═╝░░╚═╝╚═════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝░░░╚═════╝░  ╚═╝░░╚══╝╚═╝░░░╚═╝░░░╚═╝░░╚═╝░╚════╝░

░██████╗░███████╗███╗░░██╗███████╗██████╗░░█████╗░████████╗░█████╗░██████╗░
██╔════╝░██╔════╝████╗░██║██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗
██║░░██╗░█████╗░░██╔██╗██║█████╗░░██████╔╝███████║░░░██║░░░██║░░██║██████╔╝
██║░░╚██╗██╔══╝░░██║╚████║██╔══╝░░██╔══██╗██╔══██║░░░██║░░░██║░░██║██╔══██╗
╚██████╔╝███████╗██║░╚███║███████╗██║░░██║██║░░██║░░░██║░░░╚█████╔╝██║░░██║
{Fore.WHITE}'''.replace('░', ' ')

    width = os.get_terminal_size().columns
    print(pad_to_center(text.splitlines(), width))


print_nitro()
print_title()


print(f"{Fore.GREEN}Please enter the delay in seconds between gift checks{Fore.WHITE}")
generator_delay = float(input("[USER] --> "))

nitro_checker = NitroChecker.NitroChecker(NitroChecker.ErrorHandler())

while True:
    random_code = nitro_checker.generate_code()
    response = nitro_checker.check_code(random_code)

    rate_limit_time = time.time() - nitro_checker.rate_limit['rate_timestamp']

    if rate_limit_time <= nitro_checker.rate_limit['rate_delay']:
        time_to_wait = nitro_checker.rate_limit['rate_delay'] - rate_limit_time

        nitro_checker.format_message(Fore.RED, 'Rate Limited', f'Waiting {time_to_wait} seconds.')
        time.sleep(time_to_wait)

    if response == NitroChecker.Responses.RATE_LIMITED:
        nitro_checker.format_message(Fore.RED, 'Rate Limited', random_code, len(nitro_checker.cache))

    elif response == NitroChecker.Responses.VALID:
        nitro_checker.format_message(Fore.GREEN, 'Valid Code!', random_code, len(nitro_checker.cache))

        with open('codes.txt', 'a') as f:
            f.write(random_code + '\n')

    elif response == NitroChecker.Responses.IN_CACHE:
        nitro_checker.format_message(Fore.GREEN, 'Code in Cache', random_code)

    elif response == NitroChecker.Responses.INVALID_GIFT:
        nitro_checker.format_message(Fore.CYAN, 'Invalid Code', random_code, len(nitro_checker.cache))

    elif response == NitroChecker.Responses.ALREADY_CLAIMED:
        nitro_checker.format_message(Fore.CYAN, 'Code Already Claimed', random_code, len(nitro_checker.cache))

    time.sleep(generator_delay)
