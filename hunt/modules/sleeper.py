import typing
import httpx
from hunt import __get_proxy__

class Sleeper:
      module_name = 'Sleeper Fantasy'
      module_domain = 'sleeper.com'

      def __check__(base: typing.Any) -> None:
          structure = base.__base_structure__(Sleeper.module_name, Sleeper.module_domain, exists = None)
          try:
            proxy = __get_proxy__()
            proxy = ({
                'http://'  : 'http://{}'.format(proxy),
                'https://' : 'http://{}'.format(proxy)} if proxy else None)
            payload = {'operationName': 'login_context_by_email_or_phone_or_username', 'query': 'query login_context_by_email_or_phone_or_username {\n        login_context_by_email_or_phone_or_username(email_or_phone_or_username: \"%s\")\n      }' % base.email, 'variables': {}}
            request = httpx.post('https://sleeper.com/graphql', headers = base.__base_headers__({
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Origin': 'https://sleeper.com',
                'Referer': 'https://sleeper.com/login',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'X-Sleeper-Graphql-Op': 'login_context_by_email_or_phone_or_username'
            }), json = payload, proxies = proxy)
            structure[1]['response'] = request
            structure[1]['response_status_code'] = request.status_code
            try:
              if request.json().get('errors'):
                 structure[1]['exists'] = False
              else:
                 if not request.json().get('errors') and request.json().get('data') and request.json()['data'].get('login_context_by_email_or_phone_or_username'):
                    structure[1]['exists'] = True
                    structure[1]['additional_info'] = {
                        'Display Name': str(request.json()['data']['login_context_by_email_or_phone_or_username'].get('display_name')),
                        'Masked Email': str(request.json()['data']['login_context_by_email_or_phone_or_username'].get('masked_email')),
                        'Masked Phone': str(request.json()['data']['login_context_by_email_or_phone_or_username'].get('masked_phone')),
                        'Real Name': str(request.json()['data']['login_context_by_email_or_phone_or_username'].get('real_name')),
                        'User ID': str(request.json()['data']['login_context_by_email_or_phone_or_username'].get('user_id'))
                    }
            except Exception as E:
                   if request.status_code == 429:
                      structure[1]['ratelimited'] = True
                      base.output.append(structure)
                      return
                   structure[1]['error'] = type(E)
                   structure[1]['error_description'] = str(E)
            base.output.append(structure)
            return
          except Exception as E:
                 structure[1]['error'] = str(type(E))
                 structure[1]['error_description'] = str(E)
          base.output.append(structure)
