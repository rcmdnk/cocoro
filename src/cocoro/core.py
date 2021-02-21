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
            'Connection': 'close',
        }

    def read_config(self):
        with open(self.config_file, 'r') as f:
            self.config = yaml.safe_load(f)

    def get_headers(self, **kw):
        headers = self.headers.copy()
        for k, v in kw.items():
            headers[k] = v
        return headers

    def get_cookie(self):
        url = self.url_prefix + '/setting/login/'
        params = '&'.join(
            f'{k}={v}' for k, v in {
                'appSecret': self.config['appSecret'],
                'serviceName': 'iClub'
            }.items())
        data = '{"terminalAppId":"https:\\/\\/db.cloudlabs.sharp.co.jp'\
            f'\\/clpf\\/key\\/{self.config["terminalAppIdKey"]}"'\
            '}'
        headers = self.get_headers(**{'Connection': 'keep-alive',
                                      'Accept-Language': 'ja-jp'})
        response = requests.post(url, headers=headers, params=params,
                                 data=data)
        if response.status_code != 200 or 'JSESSIONID' not in response.cookies:
            raise Exception('Failed to get cookie')
        return response.cookies['JSESSIONID']

    def run(self):
        pass

    def switch(self, on=True):
        url = self.url_prefix + '/control/deviceControl'
        cookies = {
            'JSESSIONID': self.get_cookie(),
        }
        params = (
            ('boxId', 'https://db.cloudlabs.sharp.co.jp/clpf/key/'
                      f'{self.config["boxIdKey"]}'),
            ('appSecret', urllib.parse.unquote(self.config['appSecret'])),
        )
        if on:
            code1 = '30'
            code2 = '00030000000000000000000000FF00000000000000000000000000'
        else:
            code1 = '31'
            code2 = '000300000000000000000000000000000000000000000000000000'
        data = '{"controlList":[{"status":[{"valueSingle":{"code":'+code1+'},'\
            '"statusCode":"80","valueType":"valueSingle"},'\
            '{"valueBinary":{"code":"'+code2+'"},'\
            '"statusCode":"F3","valueType":"valueBinary"}'\
            '],'\
            f'"deviceId":"{self.config["deviceId"]}",'\
            f'"echonetNode":"{self.config["echonetNode"]}",'\
            f'"echonetObject":"{self.config["echonetObject"]}'\
            '"}]}'
        headers = self.get_headers(**{'Connection': 'close',
                                      'Proxy-Connection': 'close'})
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
