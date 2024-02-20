import typing
import httpx
from hunt import __get_proxy__

class Pandora:
      module_name = 'Pandora'
      module_domain = 'pandora.com'

      def __check__(base: typing.Any) -> None:
          structure = base.__base_structure__(Pandora.module_name, Pandora.module_domain, exists = None)
          try:
            proxy = __get_proxy__()
            proxy = ({
                'http://'  : 'http://{}'.format(proxy),
                'https://' : 'http://{}'.format(proxy)} if proxy else None)
            payload = {'pat': 'VIjmmBO/2e5lLeMc4Wzmu+jcRSNsDktfyKBDtIavXr1XtYd4A5qOA/Vw==', 'cb': '', 'searchString': base.email, 'startIndex': '0', 'pageSize': '200'}
            request = httpx.post('https://www.pandora.com/content/mobile/find_people_search.vm', headers = base.__base_headers__({
                'Accept': 'text/html, */*; q=0.01',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Host': 'www.pandora.com',
                'Origin': 'https://www.pandora.com',
                'Referer': 'https://www.pandora.com/content/mobile/find_people_search.vm',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'X-Requested-With': 'XMLHttpRequest'
            }), data = payload, proxies = proxy)
            structure[1]['response'] = request
            structure[1]['response_status_code'] = request.status_code
            try:
              if '<div class="js-touchstart js-follow-items double-link">' in request.text:
                 structure[1]['exists'] = True
                 try:
                   profile = request.text.split('<h6 class="media--people__text truncate-line" data-qa="followPage_username">')[1].split('</')[0]
                   profile_request = httpx.get('https://www.pandora.com/content/mobile/profile.vm?query={}'.format(profile), headers = base.__base_headers__({
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                       'Cache-Control': 'max-age=0',
                       'sec-fetch-dest': 'document',
                       'sec-fetch-mode': 'navigate',
                       'sec-fetch-site': 'none',
                       'sec-fetch-user': '?1',
                   }), proxies = proxy)
                   if '<strong data-qa="profilePage_profile_header_username">' in profile_request.text:
                      bio = profile_request.text.split('<h6 class="profile-info--marginBottomLrg" data-qa="profilePage_bio_info">')[1].split('</h6>')[0]
                      stations = profile_request.text.split('<div class="button-doubleLayer__number">')[1].split('</div>')[0]
                      likes = profile_request.text.split('<div class="button-doubleLayer__number" data-qa="profilePage_likes_tab_count">')[1].split('</div>')[0]
                      followers = profile_request.text.split('<div class="button-doubleLayer__number" data-qa="profilePage_followers_tab_count">')[1].split('</div>')[0]
                      following = profile_request.text.split('<div class="button-doubleLayer__number" data-qa="profilePage_following_tab_count">')[1].split('</div>')[0]
                      structure[1]['additional_info'] = {
                        'Username': profile,
                        'Bio': bio,
                        'Stations': stations,
                        'Likes': likes,
                        'Followers': followers,
                        'Following': following
                      }
                 except Exception as E:
                        structure[1]['error'] = type(E)
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
