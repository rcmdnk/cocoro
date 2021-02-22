import os
import json
import requests
import urllib
import yaml


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
        data = {'terminalAppId': 'https://db.cloudlabs.sharp.co.jp/clpf/key/'
                                 f'{self.config["terminalAppIdKey"]}'}
        data = json.dumps(data).replace('/', '\\/')
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

    def device_control(self, system, target):
        self.get_box()
        url = self.url_prefix + '/control/deviceControl'
        headers = self.get_headers(**{'Connection': 'close',
                                      'Proxy-Connection': 'close'})
        cookies = self.get_cookies()
        params = (
            ('appSecret', self.get_app_secret()),
            ('boxId', self.config['box'][0]['boxId']),
        )
        code1 = None
        if system == 'ope':
            if target == 'on':
                code1 = '30'
                code2 = \
                    '00030000000000000000000000FF00000000000000000000000000'
            else:
                code1 = '31'
                code2 = \
                    '000300000000000000000000000000000000000000000000000000'
        elif system == 'humi':
            if target == 'on':
                code2 = \
                    '000900000000000000000000000000FF0000000000000000000000'
            else:
                code2 = \
                    '000900000000000000000000000000000000000000000000000000'
        elif system == 'mode':
            if target == 'auto':
                code2 = \
                    '010100001000000000000000000000000000000000000000000000'
            elif target == 'sleep':
                code2 = \
                    '010100001100000000000000000000000000000000000000000000'
            elif target == 'pollen':
                code2 = \
                    '010100001300000000000000000000000000000000000000000000'
            elif target == 'quiet':
                code2 = \
                    '010100001400000000000000000000000000000000000000000000'
            elif target == 'medium':
                code2 = \
                    '010100001500000000000000000000000000000000000000000000'
            elif target == 'high':
                code2 = \
                    '010100001600000000000000000000000000000000000000000000'
            elif target == 'recommendation':
                code2 = \
                    '010100002000000000000000000000000000000000000000000000'
            elif target == 'effective':
                code2 = \
                    '010100004000000000000000000000000000000000000000000000'
        echonetData = self.config['box'][0]['echonetData'][0]
        data = {
            'controlList': [{
                'status': [{
                    'valueBinary':{'code': code2},
                    'statusCode': 'F3',
                    'valueType': 'valueBinary'
                }],
                'deviceId': echonetData['deviceId'],
                'echonetNode': echonetData['echonetNode'],
                'echonetObject': echonetData['echonetObject']
            }]
        }
        if code1 is not None:
            data['controlList'][0]['status'].append(
                {
                    'valueSingle': {'code': code1},
                    'statusCode': '80',
                    'valueType': 'valueSingle'
                })
        data = json.dumps(data)
        response = requests.post(url, headers=headers, params=params,
                                 cookies=cookies, data=data)
        if response.status_code != 200:
            raise Exception('Failed to access')
        data = response.json()
        if data['controlList'][0]['errorCode'] is not None\
                or data['controlList'][1]['errorCode'] is not None:
            if on:
                raise Exception('Failed to operation on')
            else:
                raise Exception('Failed to operation off')

    def on(self):
        self.device_control('ope', target='on')

    def off(self):
        self.device_control('ope', target='off')

    def humi_on(self):
        self.device_control('humi', target='on')

    def humi_off(self):
        self.device_control('humi', target='off')

    def mode_auto(self):
        self.device_control('mode', target='auto')

    def mode_sleep(self):
        self.device_control('mode', target='sleep')

    def mode_pollen(self):
        self.device_control('mode', target='pollen')

    def mode_quiet(self):
        self.device_control('mode', target='quiet')

    def mode_medium(self):
        self.device_control('mode', target='medium')

    def mode_high(self):
        self.device_control('mode', target='high')

    def mode_recommendation(self):
        self.device_control('mode', target='recommendation')

    def mode_effective(self):
        self.device_control('mode', target='effective')
