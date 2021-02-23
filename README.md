# cocoro
Tools for COCORO API (SHARP products).

## Appliances

API commands were taken for Sharp, KI-JS50 (humidifying air purifier, [KI-JS50 加湿空気清浄機/空気清浄機：シャープ](https://jp.sharp/kuusei/products/kijs50/)).

It may work for other (humidifying) air purifiers.

## Requirement

You need to get `appSecret` and `terminalAppIdKey` to control appliances.

To get them, you can use [mitmproxy](https://mitmproxy.org/).

By using mitmproxy, you will see following `POST` command while you are controlling COCORO in your smart phone:


    POST https://hms.cloudlabs.sharp.co.jp/hems/pfApi/ta/setting/login/?appSecret=XXXXXXXXX…
           ← 200 application/json 38b 308ms

Open this command and you will see:


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
appSecret: <*************appSecret**********************>
terminalAppIdKey: <************terminalAppIdKey*************>
```

## Install

### Using pip

    $ pip install cocoro
    $ cocoro <cmd>

### Using source code

Use poetry to setup the environment.

    $ pip install poetry
    $ git clone https://github.com/rcmdnk/cocoro.git
    $ cd cocoro
    $ poetry install
    $ poetry run cocoro <cmd>

## How to use

    $ cocoro <cmd>

Available commands are:

* `on`: Switch on
* `off`: Switch off
* `humi_on`: Humidification on
* `humi_off`: Humidification off
* `mode_auto`: Set mode: Auto
* `mode_sleep`: Set mode: Sleep
* `mode_pollen`: Set mode: Pollen
* `mode_quiet`: Set mode: Quiet
* `mode_medium`: Set mode: Medium
* `mode_high`: Set mode: High
* `mode_recommendation`: Set mode: Recommendation
* `mode_effective`: Set mode: Effective
* `version`: Show version
