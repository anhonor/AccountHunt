import typing
import httpx
from hunt import __get_proxy__

class Twitter:
      module_name = 'Twitter'
      module_domain = 'twitter.com'

      def __check__(base: typing.Any) -> None:
          structure = base.__base_structure__(Twitter.module_name, Twitter.module_domain, exists = None)
          try:
            proxy = __get_proxy__()
            proxy = ({
                'http://'  : 'http://{}'.format(proxy),
                'https://' : 'http://{}'.format(proxy)} if proxy else None)
            params = {'email': base.email}
            request = httpx.get('https://api.twitter.com/i/users/email_available.json', params = params, headers = base.__base_headers__({
                'Accept': '*/*',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Host': 'api.twitter.com',
                'Origin': 'https://twitter.com',
                'Referer': 'https://twitter.com/',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'no-cors',
                'sec-fetch-site': 'same-site',
                'x-twitter-active-user': 'yes',
                'x-twitter-client-language': 'en'
            }), proxies = proxy)
            structure[1]['response'] = request
            structure[1]['response_status_code'] = request.status_code
            try:
              if request.json().get('taken'):
                 structure[1]['exists'] = True
              elif not request.json().get('taken'):
                 structure[1]['exists'] = False
            except Exception as E:
                   if request.status_code == 429:
                      structure[1]['ratelimited'] = True; base.output.append(structure)
                      return
                   structure[1]['error'] = type(E)
                   structure[1]['error_description'] = str(E)
            base.output.append(structure)
            return
          except Exception as E:
                 structure[1]['error'] = str(type(E))
                 structure[1]['error_description'] = str(E)
          base.output.append(structure)
