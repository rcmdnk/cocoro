import os
import json
import urllib
from logging import getLogger, NullHandler
import yaml
import requests


class Cocoro():
    def __init__(self, config_file=None, verbose='info'):
        self.config = {}

        if config_file is None:
            config_file = os.environ.get('COCORO_CONFIG',
                                         '~/.config/cocoro/config.yml')
        config_file = os.path.expanduser(config_file)
        self.config_file = config_file
        self.read_config()

        self.logger = getLogger(__name__)
        verbose = self.get_verbose(verbose)
        if verbose == -1:
            self.logger.warning(f'Invalid verbose level: {verbose}.')
        else:
            self.logger.setLevel(verbose)
        self.logger.addHandler(NullHandler())

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

        self.control = {
            'switch': {
                'on': (
                    '30',
                    '00030000000000000000000000FF00000000000000000000000000'),
                'off': (
                    '31',
                    '000300000000000000000000000000000000000000000000000000')},
            'humi': {
                'on': (
                    None,
                    '000900000000000000000000000000FF0000000000000000000000'),
                'off': (
                    None,
                    '000900000000000000000000000000000000000000000000000000')},
            'mode': {
                'auto': (
                    None,
                    '010100001000000000000000000000000000000000000000000000'),
                'sleep': (
                    None,
                    '010100001100000000000000000000000000000000000000000000'),
                'pollen': (
                    None,
                    '010100001300000000000000000000000000000000000000000000'),
                'quiet': (
                    None,
                    '010100001400000000000000000000000000000000000000000000'),
                'medium': (
                    None,
                    '010100001500000000000000000000000000000000000000000000'),
                'high': (
                    None,
                    '010100001600000000000000000000000000000000000000000000'),
                'recommendation': (
                    None,
                    '010100002000000000000000000000000000000000000000000000'),
                'effective': (
                    None,
                    '010100004000000000000000000000000000000000000000000000')}}

    def read_config(self):
        with open(self.config_file, 'r') as f:
            self.config.update(yaml.safe_load(f))

    def get_verbose(self, verbose):
        if isinstance(verbose, int):
            return verbose
        if verbose.isdigit():
            return int(verbose)
        levels = {'notest': 0, 'debug': 10, 'info': 20, 'warn': 30,
                  'warning': 30, 'error': 40, 'fatal': 50}
        if verbose in levels:
            return levels[verbose]
        return -1

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
            return
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
        echonetData = self.config['box'][0]['echonetData'][0]
        data = {
            'controlList': [{
                'status': [{
                    'valueBinary': {'code': self.control[system][target][1]},
                    'statusCode': 'F3',
                    'valueType': 'valueBinary'
                }],
                'deviceId': echonetData['deviceId'],
                'echonetNode': echonetData['echonetNode'],
                'echonetObject': echonetData['echonetObject']
            }]
        }
        if self.control[system][target][0] is not None:
            data['controlList'][0]['status'].append(
                {
                    'valueSingle': {'code': self.control[system][target][0]},
                    'statusCode': '80',
                    'valueType': 'valueSingle'
                })
        data = json.dumps(data)
        response = requests.post(url, headers=headers, params=params,
                                 cookies=cookies, data=data)
        if response.status_code != 200:
            raise Exception('Failed to access')
        data = response.json()
        if data['controlList'][0]['errorCode'] is not None:
            raise Exception(f'Failed: {system} {target}')
