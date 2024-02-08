import colorama
from hunt import *
from hunt.modules.replit import Replit
from hunt.modules.twitter import Twitter

hunt = Base(
    input(
        f'{colorama.Style.BRIGHT}{colorama.Fore.RED}*{colorama.Style.RESET_ALL} Email: '
    )
)

functions = [
   Replit.__check__,
   Twitter.__check__
]

for function in functions:
    function(hunt)

for response in hunt.output:
    if response[1]['exists']:
       print(f'{colorama.Style.BRIGHT}{colorama.Fore.LIGHTBLUE_EX}-{colorama.Style.RESET_ALL} {response[1]["module_domain"]} ({response[0]})')
