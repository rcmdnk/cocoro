import os
import json
import urllib
import logging
import yaml
import requests


class Cocoro():
    def __init__(self, config_file=None, appSecret=None, terminalAppIdKey=None,
                 name=None, log_level='info'):
        self.config = {}

        if config_file is None:
            config_file = os.environ.get('COCORO_CONFIG',
                                         '~/.config/cocoro/config.yml')
        config_file = os.path.expanduser(config_file)
        self.config_file = config_file
        self.read_config()
        if appSecret is not None:
            self.config['appSecret'] = appSecret
        if terminalAppIdKey is not None:
            self.config['terminalAppIdKey'] = terminalAppIdKey
        self.config['name'] = name

        self.logger = logging.getLogger(self.__class__.__name__)
        log_level = self.get_log_level(log_level)
        if log_level == -1:
            self.logger.warning(f'Invalid log_level level: {log_level}.')
        else:
            self.logger.setLevel(log_level)
        self.logger.addHandler(logging.NullHandler())

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
            'humidification': {
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

    @staticmethod
    def get_log_level(log_level):
        if isinstance(log_level, int):
            return log_level
        if log_level.isdigit():
            return int(log_level)
        levels = {'debug': logging.DEBUG,
                  'info': logging.INFO, 'warn': logging.WARN,
                  'warning': logging.WARNING, 'error': logging.ERROR,
                  'fatal': logging.FATAL}
        if log_level.lower() in levels:
            return levels[log_level.lower()]
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
            self.logger.error('Failed to get cookie')
            return False
        self.config['cookies'] = {'JSESSIONID': response.cookies['JSESSIONID']}
        return self.config['cookies']

    def get_box_par(self):
        for box in self.config['box']:
            for echonetData in box['echonetData']:
                name = echonetData['labelData']['name'].strip('"\'')
                if (self.config['name'] is None
                        or name
                        == self.config['name']):
                    self.config['boxId'] = box['boxId']
                    self.config['echonetData'] = echonetData
                    self.config['name'] = name
                    return True
        if self.config['name'] is None:
            self.logger.error('Could not find any device')
            return False
        self.config['boxId'] = self.config['box'][0]['boxId']
        self.config['echonetData'] = self.config['box'][0]['echonetData'][0]
        self.logger.warning(
            f'Could not find device named {self.config["name"]}. '
            'Use the first device: '
            f'{self.config["echonetData"]["labelData"]["name"]}.')
        return True

    def get_box(self):
        if 'box' in self.config:
            return True
        url = self.url_prefix + '/setting/boxInfo/'
        headers = self.get_headers()
        cookies = self.get_cookies()
        if not cookies:
            return False
        params = (
            ('appSecret', self.get_app_secret()),
            ('mode', 'other'),
        )
        response = requests.get(url, headers=headers, params=params,
                                cookies=cookies)
        if response.status_code != 200:
            self.logger.error('Failed to get box information')
            return False
        self.config.update(response.json())
        if not self.get_box_par():
            return False
        return True

    def device_control(self, system, target):
        if not self.get_box():
            return False
        url = self.url_prefix + '/control/deviceControl'
        headers = self.get_headers(**{'Connection': 'close',
                                      'Proxy-Connection': 'close'})
        cookies = self.get_cookies()
        if not cookies:
            return False
        params = (
            ('appSecret', self.get_app_secret()),
            ('boxId', self.config['boxId']),
        )
        data = {
            'controlList': [{
                'status': [{
                    'valueBinary': {'code': self.control[system][target][1]},
                    'statusCode': 'F3',
                    'valueType': 'valueBinary'
                }],
                'deviceId': self.config['echonetData']['deviceId'],
                'echonetNode': self.config['echonetData']['echonetNode'],
                'echonetObject': self.config['echonetData']['echonetObject']
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
            self.logger.error(f'Failed to control {self.config["name"]}: '
                              f'{system} {target}. '
                              f'Status code: {response.status_code}.')
            return False
        data = response.json()
        if data['controlList'][0]['errorCode'] is not None:
            self.logger.error(f'Failed to control: {self.config["name"]} '
                              f'{system} {target}')
            return False
        self.logger.info(f'Succeeded to control {self.config["name"]}: '
                         f'{system} {target}')
        return True

    def devince_info(self, key='labelData'):
        if not self.get_box():
            return False
        self.logger.info('Device information')
        if key == 'full':
            return self.config['echonetData']
        if key in self.config['echonetData'].keys():
            return self.config['echonetData'][key]
        if key in self.config['echonetData']['labelData'].keys():
            return self.config['echonetData']['labelData'][key]
        self.logger.warning('Invalid key for device_info()')
        return False
