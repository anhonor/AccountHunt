import typing
import httpx
from hunt import __get_proxy__

class Poshmark:
      module_name = 'Poshmark'
      module_domain = 'poshmark.com'

      def __check__(base: typing.Any) -> None:
          structure = base.__base_structure__(Poshmark.module_name, Poshmark.module_domain, exists = None)
          try:
            proxy = __get_proxy__()
            proxy = ({
                'http://'  : 'http://{}'.format(proxy),
                'https://' : 'http://{}'.format(proxy)} if proxy else None)
            payload = {'query': base.email, 'type': 'people', 'src': 'dir'}
            request = httpx.get('https://poshmark.com/search', params = payload, headers = base.__base_headers__({
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1'
            }), proxies = proxy)
            try:
              if '<div class="follow-list__container card card--medium">' in request.text:
                 structure[1]['exists'] = True
                 closet = request.text.split('<a href="/closet/')[1].split('"')[0]
                 try:
                   closet_request = httpx.get('https://poshmark.com/closet/{}'.format(closet), headers = base.__base_headers__({
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                       'sec-fetch-dest': 'document',
                       'sec-fetch-mode': 'navigate',
                       'sec-fetch-site': 'same-origin',
                       'sec-fetch-user': '?1'
                   }))
                   if '"$_closet":{"closetUserInfo":' in closet_request.text:
                      full_name = closet_request.text.split('"full_name":"')[1].split('"')[0]
                      country = closet_request.text.split('"home_domain":"')[1].split('"')[0].upper()
                      gender = closet_request.text.split('"gender":"')[1].split('"')[0].title()
                      city = closet_request.text.split('"profile":{"city":"')[1].split('"')[0] if '"profile":{"city":"' in closet_request.text else None
                      state = closet_request.text.split('"profile":{')[1].split('"state":"')[1].split('"')[0] if '"state":"' in closet_request.text.split('"profile":{')[1] else None
                      twitter = closet_request.text.split('"tw_info":"')[1].split('"')[0] if '"tw_info":"' in closet_request.text else None
                      facebook = closet_request.text.split('"fb_info":"')[1].split('"')[0] if '"fb_info":"' in closet_request.text else None
                      tumblr = closet_request.text.split('tm_info":"')[1].split('"')[0] if 'tm_info":"' in closet_request.text else None
                      following = closet_request.text.split('"following":')[1].split(',')[0]
                      followers = closet_request.text.split('"followers":')[1].split(',')[0]
                      created_at = closet_request.text.split('"created_at":"')[1].split('"')[0]
                      structure[1]['additional_info'] = {
                          'Username': closet,
                          'Full Name': full_name,
                          'Facebook': facebook,
                          'Tumblr': tumblr,
                          'Twitter': twitter,
                          'Country': country,
                          'Gender': gender,
                          'City': city,
                          'State': state,
                          'Following': following,
                          'Followers': followers,
                          'Created At': created_at
                      }
                 except Exception as E:
                        structure[1]['error'] = str(type(E))
                        structure[1]['error_description'] = str(E)
              else:
                structure[1]['exists'] = False
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

# ~ pretty rough, will update soon. ~ 
