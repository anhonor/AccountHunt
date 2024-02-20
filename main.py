import colorama
import os
from hunt import *
from hunt.modules import microsoft
from hunt.modules import pandora
from hunt.modules import replit
from hunt.modules import sleeper
from hunt.modules import twitter

hunt = Base(
    input(
        f'{colorama.Style.BRIGHT}{colorama.Fore.LIGHTBLUE_EX}EMAIL{colorama.Style.RESET_ALL}: '
    )
)

os.system('clear || cls')

functions = [
   microsoft.Microsoft.__check__,
   pandora.Pandora.__check__,
   replit.Replit.__check__,
   sleeper.Sleeper.__check__,
   twitter.Twitter.__check__,
]

for function in functions:
    function(hunt)

print('+----- EXISTING -----+')
for response in hunt.output:
    if response[1]['exists']:
       print(f'{colorama.Style.BRIGHT}{colorama.Fore.LIGHTBLUE_EX}EXISTS{colorama.Style.RESET_ALL}')
       print(f'{response[0]} - {response[1]["module_domain"]}')
       if response[1]['additional_info']:
          for key, value in response[1]['additional_info'].items():
              print(f'{colorama.Style.BRIGHT}{colorama.Fore.LIGHTBLUE_EX}~{colorama.Style.RESET_ALL} {key}: {value}')
       else:
          print(f'{colorama.Style.BRIGHT}{colorama.Fore.RED}~{colorama.Style.RESET_ALL} No Additional Information')
       print('')

print('+----- INVALID -----+')
for response in hunt.output:
    if not response[1]['exists']:
       print(f'{colorama.Style.BRIGHT}{colorama.Fore.RED}INVALID{colorama.Style.RESET_ALL} {response[0]} ({response[1]["module_domain"]})')
      
