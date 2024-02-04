import httpx
import json
import os
import random
import string
import tls_client
import ua_generator

setting = json.load(open('./hunt/data/config.json', 'r', encoding = 'utf-8'))
proxies = list(proxy for proxy in open(setting['proxy_file'], 'r', encoding = 'utf-8'))

def __get_proxy__() -> str | None:
    if len(proxies):
       return random.choice(proxies).strip()
    
def __get_client_identifier__() -> str:
    return random.choice([
        'chrome_117',
        'chrome_112',
        'chrome_107',
        'chrome_106',
        'chrome_105',
        'chrome_104',
        'chrome_103',
        'chrome_102'
    ])

def __get_client__(client_identifier = __get_client_identifier__()) -> tls_client.Session:
    return tls_client.Session(client_identifier = client_identifier, random_tls_extension_order = True)

class Base:
      def __init__(base, email: str, proxy: str | None = None):
          base.output = []
          base.agent = ua_generator.generate(device = ('desktop'), browser = ('chrome'))
          base.email = email
      
      def __base_headers__(base, headers: dict = {}) -> dict:
          return {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'sec-ch-ua': base.agent.ch.brands,
            'sec-ch-ua-mobile': base.agent.ch.mobile,
            'sec-ch-ua-platform': base.agent.ch.platform,
           **headers,
            'User-Agent': base.agent.text
          }
      
      def __base_structure__(
          base, 
          module_name: str, 
          module_domain: str, 
          exists: bool, 
          response: httpx.Response | tls_client.response.Response | None = None,
          response_status_code: int | None = None,
          ratelimited: bool = False, 
          error: str | Exception | None = None, 
          error_description: str | None = None) -> tuple:
          return (module_name, {
             'module_domain': module_domain,
             'exists': exists,
             'ratelimited': ratelimited,
             'response': response,
             'response_status_code': response_status_code,
             'error': error,
             'error_description': error_description
          })
