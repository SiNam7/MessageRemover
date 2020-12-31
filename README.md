# MessageRemover

This bot only does its function in the #music channel.
Only the member who has 'administrator' permission or 'Dev' role can execute the commands below.

# Commands (prefix: !)

* ping

pong!

* active

Active auto-remove message function.
All messages in the #music channel will be removed when the specified time elapsed.
(default: 30 seconds)

* inactive

Deactivate auto-remove message function.

* delay _seconds_

Set auto-remove message period to _seconds_ (default: 30 sec)

* purge [amount=50]

Purge [amount] non-pinned messages in its channel before this command has been executed.
type "confirm" to confirm purge operation.
