# CrowdQ

CrowdQ is a webapp (hosted on a local server) used to crowdsource questions at a live conference, panel discussion or event. After running the server, anyone on the local Wi-Fi network can connect to the server IP and send in questions which can be managed by an admin and pushed to a display screen.

### Installation

CrowdQ requires Flask to run.

To install requirements:

```sh
$ pip install requirements.txt
```

To run the local server
```sh
$ sudo python app.py
```

To send in questions connect to:
```HTTP://SERVER-IP/ ```

To log into the admin interface connect to:
```HTTP://SERVER-IP/admin ```

To log into the display interface connect to:
```HTTP://SERVER-IP/display ```

License
----
Apache License