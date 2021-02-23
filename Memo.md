## Weather information

It needs X-Client-Id and another Cookie and appSecret.

X-Client-Id and appSecret can be found by mitmproxy (they are fixed, I think),
but the cookie like `route=.....` is suddenly appeared.

The cookie will be changed so that it should be obtained from API.

It could be the validity period of the cookie for the weather information
is so long that the app does not send the post to get new cookie during the test.

## Status of appliance

There are no direct information about the current status of the appliance,
if the switch is on or off, the humidification is on or off, what is the mode.

Only after the command to change the status is sent,
the information to confirm the result is given.
