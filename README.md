# cocoro

[![PyPI version](https://badge.fury.io/py/cocoro.svg)](https://badge.fury.io/py/cocoro)
[![COCORO test](https://github.com/rcmdnk/cocoro/actions/workflows/cocoro-test.yml/badge.svg)](https://github.com/rcmdnk/cocoro/actions/workflows/cocoro-test.yml)

Tools for COCORO API (SHARP products).

## Install and Usage

### Using pip

    $ pip install cocoro

### Using source code

Use poetry to setup the environment.

    $ pip install poetry
    $ git clone https://github.com/rcmdnk/cocoro.git
    $ cd cocoro
    $ poetry install

## Appliances

API commands were taken for Sharp, KI-JS50 (humidifying air purifier, [KI-JS50 加湿空気清浄機/空気清浄機：シャープ](https://jp.sharp/kuusei/products/kijs50/)).

It may work for other (humidifying) air purifiers.

## Requirement

You need to get `appSecret` and `terminalAppIdKey` to control appliances.

To get them, you can use [mitmproxy](https://mitmproxy.org/).

By using mitmproxy, you will see following `POST` command while you are controlling COCORO in your smart phone:


    POST https://hms.cloudlabs.sharp.co.jp/hems/pfApi/ta/setting/login/?appSecret=XXXXXXXXX…
           ← 200 application/json 38b 308ms

Open this command and you will see following in `Request tab:


    2021-02-21 21:55:40 POST https://hms.cloudlabs.sharp.co.jp/hems/pfApi/ta/setting/login/?app
                             Secret=<*************appSecret**********************>&serviceName=
                             iClub
                             ← 200 OK application/json 38b 308ms
                Request                         Response                        Detail
    Host:             hms.cloudlabs.sharp.co.jp
    Content-Type:     application/json; charset=utf-8
    Connection:       keep-alive
    Accept:           */*
    User-Agent:       smartlink_v200i Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X)
                      AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148
    Content-Length:   110
    Accept-Language:  ja-jp
    Accept-Encoding:  gzip, deflate, br
    JSON                                                                                  [m:auto]
    {
        "terminalAppId":
    "https://db.cloudlabs.sharp.co.jp/clpf/key/<************terminalAppIdKey*************>"
    }

Find `appSecret` and `terminalAppIdKey` values from above details.

Then, make following configuration file as **~/.config/cocoro/config.yml**:

```yml
---
appSecret: <*************appSecret**********************>
terminalAppIdKey: <************terminalAppIdKey*************>
```

## Usage

If you installed cocoro by `pip`, do:

    $ cocoro <cmd> [options]

If you installed from source code, go to cocoro directory, then do:

    $ poetry run cocoro <cmd> [options]

Available commands (`<cmd>`) are:

* `switch <target>`: Control switch. Available targets: `on`, `off`.
* `humidification <target>`: Control humidification. Available targets: `on`, `off`.
* `humi <target>`  : Alias of humidification.
* `mode <target>`  : Control mode. Available targets: `auto`, `sleep`, `pollen`,
                     `quiet`, `medium`, `high`, `recommendation`, `effective`
* `info [key]      : Show the appliance information. The available keys are:
                     `full`(full echonetData), `labelData`, `maker`, `model`,
                     `deviceType`, `name`, `place`, `yomi`, `zipCd`
                     If no key is give, labelData is shown.
* `version`: Show   version.
* `help`: Show help.

Other options:

* `--config_file <file>`: Set configuration file. Default file path is `~/.config/cocoro/config.yml`.
* `--appSecret <appSecret>`: Set appSecret (overwrite the value of config_file).
* `--terminalAppIdKey <terminalAppIdKey>`: Set terminalAppIdKey (overwrite the value of config_file).
* `--name <name>`: Set name of the device. If no name is given, the first device is used.
* `--log_level <level>`: Set log level. The available levels are: `debug`, `info`, `warning` `fatal`.


## Examples

    $ poetry run cocoro switch on
    [INFO][Cocoro] Succeeded to control js50: switch on
    $ poetry run cocoro humi off
    [INFO][Cocoro] Succeeded to control js50: humidification off
    $ poetry run cocoro mode auto
    [INFO][Cocoro] Succeeded to control js50: mode auto


    $ cocoro info
    [INFO][Cocoro] Device information
    {'id': 123456, 'place': 'リビング', 'name': 'my js50', 'deviceType': 'AIR_CLEANER', 'zipCd': '7890123', 'yomi': '', 'lSubInfo': '{"room_data":{"size": 10.0, "struct": "prefab", "unit": "tatami"}}'}
    $ cocoro info model --log_level=warning
    KIJS50
    $ cocoro info maker --log_level=warning
    SHARP
