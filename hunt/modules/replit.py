import typing
import httpx
from hunt import __get_proxy__

class Replit:
      module_name = 'Replit'
      module_domain = 'replit.com'

      def __check__(base: typing.Any) -> None:
          structure = base.__base_structure__(Replit.module_name, Replit.module_domain, exists = None)
          try:
            proxy = __get_proxy__()
            proxy = ({
                'http://'  : 'http://{}'.format(proxy),
                'https://' : 'http://{}'.format(proxy)} if proxy else None)
            payload = {'email': base.email}
            request = httpx.post('https://replit.com/data/user/exists', headers = base.__base_headers__({
                'Accept': 'application/json',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json',
                'Origin': 'https://replit.com',
                'Referer': 'https://replit.com/signup',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'X-Requested-With': 'XMLHttpRequest'
            }), json = payload, proxies = proxy)
            structure[1]['response'] = request
            structure[1]['response_status_code'] = request.status_code
            try:
              if request.json().get('exists'):
                 structure[1]['exists'] = True
              elif not request.json().get('exists'):
                 structure[1]['exists'] = False
            except Exception as E:
                   if request.status_code == 429:
                      structure['ratelimited'] = True; base.output.append(structure)
                      return
                   structure[1]['error'] = type(E)
                   structure[1]['error_description'] = str(E)
            base.output.append(structure)
            return
          except Exception as E:
                 structure[1]['error'] = str(type(E))
                 structure[1]['error_description'] = str(E)
          base.output.append(structure)
