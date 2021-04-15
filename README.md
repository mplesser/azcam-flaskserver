# azcam-flaskserver

*azcam-flaskserver* is an *azcam* extension which adds support for a flask-based web server.

## Installation

`pip install azcam-flaskserver`

or download from github: https://github.com/mplesser/azcam-flaskserver.git.

## Uage Example

```python
from azcam_flaskserver.flask_server import WebServer
webserver = WebServer()
webserver.templates_folder = azcam.db.systemfolder
webserver.index = f"index_mysystem.html"
webserver.start()

# options
azcam_exptool.load()
azcam_status.load()
azcam_observe.webobs.load()
```
