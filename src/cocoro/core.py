import os
import yaml
import urllib
import requests


class Cocoro():
    def __init__(self, config_file=None):
        if config_file is None:
            config_file = os.environ.get(
                'COCORO_CONFIG',
                os.environ.get('HOME')+'/.config/cocoro/config.yml')
        self.config_file = config_file
        self.read_config()
        self.url_prefix = 'https://hms.cloudlabs.sharp.co.jp/hems/pfApi/ta'
        self.headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': '*/*',
            'User-Agent': 'smartlink_v200i Mozilla/5.0 '
                          '(iPhone; CPU iPhone OS 14_4 like Mac OS X) '
                          'AppleWebKit/605.1.15 (KHTML, like Gecko) '
                          'Mobile/15E148',
            'Accept-Language': 'ja-jp',
            'Connection': 'keep-alive',
            'Proxy-Connection': 'keep-alive',
        }

    def read_config(self):
        with open(self.config_file, 'r') as f:
            self.config = yaml.safe_load(f)

    def get_headers(self, **kw):
        headers = self.headers.copy()
        for k, v in kw.items():
            headers[k] = v
        return headers

    def get_app_secret(self):
        return urllib.parse.unquote(self.config['appSecret'])

    def get_cookies(self):
        if 'cookies' in self.config:
            return self.config['cookies']
        url = self.url_prefix + '/setting/login/'
        headers = self.get_headers()
        params = (
            ('appSecret', self.get_app_secret()),
            ('serviceName', 'iClub'),
        )
        data = '{"terminalAppId":"https:\\/\\/db.cloudlabs.sharp.co.jp'\
            f'\\/clpf\\/key\\/{self.config["terminalAppIdKey"]}"'\
            '}'
        response = requests.post(url, headers=headers, params=params,
                                 data=data)
        if response.status_code != 200 or 'JSESSIONID' not in response.cookies:
            raise Exception('Failed to get cookie')
        self.config['cookies'] = {'JSESSIONID': response.cookies['JSESSIONID']}
        return self.config['cookies']

    def get_box(self):
        if 'box' in self.config:
            return self.config['box']
        url = self.url_prefix + '/setting/boxInfo/'
        headers = self.get_headers()
        cookies = self.get_cookies()
        params = (
            ('appSecret', self.get_app_secret()),
            ('mode', 'other'),
        )
        response = requests.get(url, headers=headers, params=params,
                                cookies=cookies)
        if response.status_code != 200:
            raise Exception('Failed to access')
        self.config.update(response.json())

    def switch(self, on=True):
        self.get_box()
        url = self.url_prefix + '/control/deviceControl'
        headers = self.get_headers(**{'Connection': 'close',
                                      'Proxy-Connection': 'close'})
        cookies = self.get_cookies()
        params = (
            ('appSecret', self.get_app_secret()),
            ('boxId', self.config['box'][0]['boxId']),
        )
        if on:
            code1 = '30'
            code2 = '00030000000000000000000000FF00000000000000000000000000'
        else:
            code1 = '31'
            code2 = '000300000000000000000000000000000000000000000000000000'
        echonetData = self.config['box'][0]['echonetData'][0]
        data = '{"controlList":[{"status":[{"valueSingle":{"code":'+code1+'},'\
            '"statusCode":"80","valueType":"valueSingle"},'\
            '{"valueBinary":{"code":"'+code2+'"},'\
            '"statusCode":"F3","valueType":"valueBinary"}'\
            '],'\
            f'"deviceId":"{echonetData["deviceId"]}",'\
            f'"echonetNode":"{echonetData["echonetNode"]}",'\
            f'"echonetObject":"{echonetData["echonetObject"]}'\
            '"}]}'
        response = requests.post(url, headers=headers, params=params,
                                 cookies=cookies, data=data)
        if response.status_code != 200:
            raise Exception('Failed to access')
        data = response.json()
        if data['controlList'][0]['errorCode'] is not None\
                or data['controlList'][1]['errorCode'] is not None:
            if on:
                raise Exception('Failed to switch on')
            else:
                raise Exception('Failed to switch off')

    def on(self):
        self.switch(on=True)

    def off(self):
        self.switch(on=False)
