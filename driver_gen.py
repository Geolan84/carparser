import logging
import json
import undetected_chromedriver as uc
from fake_generator import FakeGenerator
import os


def send_command(driver, cmd, params = {}):
  post_url = driver.command_executor._url + '/session/{0:s}/chromium/send_command_and_get_result'.format(driver.session_id)
  response = driver.command_executor._request('POST', post_url, json.dumps({'cmd': cmd, 'params': params}))
  if ('status' in response ) and response['status']:
    raise Exception(response.get('value'))
  
def set_authenticated_proxy_through_plugin(proxy, number):
    if not os.path.exists(f'pluginfile{number}'):
        os.mkdir(f'pluginfile{number}', mode = 0o777,)

    pluginfile = f'pluginfile{number}'
    manifest_json = """
            {
                "version": "1.0.0",
                "manifest_version": 2,
                "name": "Chrome Proxy",
                "permissions": [
                    "proxy",
                    "tabs",
                    "unlimitedStorage",
                    "storage",
                    "<all_urls>",
                    "webRequest",
                    "webRequestBlocking"
                ],
                "background": {
                    "scripts": ["background.js"]
                },
                "minimum_chrome_version":"22.0.0"
            }
            """
    background_js = """
            var config = {
                    mode: "fixed_servers",
                    rules: {
                    singleProxy: {
                        scheme: "http",
                        host: "%s",
                        port: parseInt(%s)
                    },
                    bypassList: ["localhost"]
                    }
                };

            chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

            function callbackFn(details) {
                return {
                    authCredentials: {
                        username: "%s",
                        password: "%s"
                    }
                };
            }

            chrome.webRequest.onAuthRequired.addListener(
                        callbackFn,
                        {urls: ["<all_urls>"]},
                        ['blocking']
            );
            """ % (proxy['proxy_address'], str(proxy['proxy_port']), proxy['username'], proxy['password'])

    with open(f'pluginfile{number}/manifest.json', 'w') as file:
        file.write(manifest_json)

    with open(f'pluginfile{number}/background.js', 'w') as file:
        file.write(background_js)
    return pluginfile

def get_chromedriver(number: int, fake: FakeGenerator, use_agent=True, use_proxy=True):
    if use_proxy:
        opts = uc.ChromeOptions()
        ip, port, ip_log, ip_pass = fake.get_new_ip()
        proxy = dict(
            proxy_address = ip,
            proxy_port = port,
            username = ip_log,
            password = ip_pass
        )
        logging.info('Generated %s', str(proxy))
        pluginfile = set_authenticated_proxy_through_plugin(proxy, number)
        opts.add_argument(f'--proxy-server=http://{ip}:{port}')
        opts.add_argument('--load-extension={}'.format(pluginfile))
        driver = uc.Chrome(options=opts)        
    else:
        driver = uc.Chrome()

    if use_agent:
        ua = fake.get_new_agent()
        logging.info('Generated %s', ua)
        send_command(driver, 'Network.setUserAgentOverride', {'userAgent': ua})

    if use_proxy:
        return driver, ip
    else:
        return driver, "None"