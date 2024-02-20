import typing
from hunt import __get_proxy__, __get_client__

class Microsoft:
      module_name = 'Microsoft'
      module_domain = 'microsoft.com'

      def __check__(base: typing.Any) -> None:
          structure = base.__base_structure__(Microsoft.module_name, Microsoft.module_domain, exists = None)
          try:
            proxy = __get_proxy__()
            proxy = ({
                'http'  : 'http://{}'.format(proxy),
                'https' : 'http://{}'.format(proxy)} if proxy else None)
            client = __get_client__()
            if proxy:
               client.proxies.update(proxy)
            data_request = client.get('https://login.live.com/', headers = base.__base_headers__({
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Connection': 'keep-alive',
                'Host': 'login.live.com',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1'
            }))
            try:
              uaid = data_request.text.split('&uaid=')[1].split('"')[0] if '&uaid' in data_request.text else None
              ppft = data_request.text.split('name="PPFT"')[1].split('value="')[1].split('"')[0] if 'name="PPFT"' in data_request.text else None
              credential_type_url = data_request.text.split('CC:')[1].split('\'')[1] if 'CC:' in data_request.text else ''
              request = client.post(credential_type_url, headers = base.__base_headers__({
                  'Accept': 'application/json',
                  'client-request-id': uaid,
                  'Connection': 'keep-alive',
                  'Content-Type': 'application/json; charset=UTF-8',
                  'Cookie': ' '.join('{}={};'.format(cookie.name, cookie.value) for cookie in data_request.cookies),
                  'Host': 'login.live.com',
                  'hpgact': '0',
                  'hpgid': '33',
                  'Origin': 'https://login.live.com',
                  'Referer': 'https://login.live.com/',
                  'sec-fetch-dest': 'empty',
                  'sec-fetch-mode': 'cors',
                  'sec-fetch-site': 'same-origin'
              }), json = {
                  'checkPhones': False,
                  'federationFlags': 3,
                  'flowToken': ppft,
                  'forceotclogin': False,
                  'isCookieBannerShown': False,
                  'isExternalFederationDisallowed': False,
                  'isFidoSupported': True,
                  'isOtherIdpSupported': False,
                  'isRemoteConnectSupported': False,
                  'isRemoteNGCSupported': True,
                  'isSignup': False,
                  'otclogindisallowed': False,
                  'uaid': uaid,
                  'username': base.email
              })
              structure[1]['response'] = request
              structure[1]['response_status_code'] = request.status_code
              try:
                if request.json().get('IfExistsResult') == 0:
                   structure[1]['exists'] = True
                   username = str(request.json().get('Username'))
                   location = str(request.json().get('Location'))
                   federated_auths = []
                   email_hints = []
                   if request.json().get('Credentials'):
                      if request.json()['Credentials'].get('HasGitHubFed'): federated_auths.append('Github')
                      if request.json()['Credentials'].get('HasGoogleFed'): federated_auths.append('Google')
                      if request.json()['Credentials'].get('HasLinkedInFed'): federated_auths.append('LinkedIn')
                      if request.json()['Credentials'].get('OtcLoginEligibleProofs'):
                         for hint in request.json()['Credentials']['OtcLoginEligibleProofs']:
                             email_hints.append(hint['display'])
                   structure[1]['additional_info'] = {
                     'Username': username,
                     'Location': location,
                     'Federated Auths': federated_auths,
                     'Email Hints': email_hints
                   }
                else:
                  structure[1]['exists'] = False
              except Exception as E:
                     if request.status_code == 429:
                        structure[1]['ratelimited'] = True
                        base.output.append(structure)
                        return
                     structure[1]['error'] = type(E)
                     structure[1]['error_description'] = str(E)
            except Exception as E:
                   structure[1]['error'] = type(E)
                   structure[1]['error_description'] = str(E)
            base.output.append(structure)
            return
          except Exception as E:
                 structure[1]['error'] = str(type(E))
                 structure[1]['error_description'] = str(E)
          base.output.append(structure)
