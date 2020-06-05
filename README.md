# nethserver-vpn-ui

VPN UI module for IPSec and OpenVPN

This module provides web interface to configure IPSec and OpenVPN tunnels inside cockpit.

## Custom OpenVPN mail

The `read` API can send the OpenVPN mail configuration to a given mail address.
Example:
```
echo '{"action":"mail","name":"myaccount","address":"user@nethserver.org"}' |  /usr/libexec/nethserver/api/nethserver-vpn-ui/openvpn-rw/read
```

The mail contains a default text that can be overridden by creating a file inside `/etc/nethserver/openvpn-mail.cfg`.
The configuration file must contain ASCII text, the special symbol `$name` will be replaced with actual account name.

Configuration example:
```
This is my custom mail $name account.
```

Mail result using the API invocation above:
```
This is my custom mail myaccount account.
```
