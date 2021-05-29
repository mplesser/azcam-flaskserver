"""
Configure and start Flask web server.
Import this after all configuration has been completed.
URL example: "http://locahost:2402/api/instrument/set_filter?filter=1&filter_id=2"
"""

import logging
import os
import sys
import threading

from flask import Flask, render_template, request, send_from_directory

import azcam


class WebServer(object):
    """
    AzCam web server.
    """

    def __init__(self):

        self.templates_folder = ""
        self.index = "index.html"
        self.upload_folder = ""

        self.logcommands = 0
        self.logstatus = 0

        # port for webserver
        self.port = None

        self.is_running = 0

        azcam.db.webserver = self

    def initialize(self):
        """
        Initialize flask application.
        """

        # create flask app
        app = Flask(__name__, template_folder=self.templates_folder)
        self.app = app

        @app.route("/", methods=["GET"])
        def home():
            return render_template(self.index)

        @app.route("/favicon.ico")
        def favicon():
            return send_from_directory(
                os.path.join(app.root_path, "static"),
                "favicon.ico",
                mimetype="image/vnd.microsoft.icon",
            )

        # ******************************************************************************
        # API commands - .../api/tool/command
        # ******************************************************************************
        @app.route("/api/<path:command>", methods=["GET"])
        def api(command):
            """
            Remote web api commands. such as: /api/expose or /api/exposure/reset
            """

            url = request.url
            if self.logcommands:
                azcam.log(url, prefix="Web-> ")

            reply = azcam.db.api.web_command(url)

            if self.logcommands:
                azcam.log(reply, prefix="Web->   ")

            return reply

    def stop(self):
        """
        Stops command server running in thread.
        """

        azcam.log("Stopping the webserver is not supported")

        return

    def start(self):
        """
        Start web server.
        """

        self.initialize()

        if self.port is None:
            self.port = azcam.db.cmdserver.port + 1

        azcam.log(f"Starting webserver - listening on port {self.port}")

        # turn off development server warning
        cli = sys.modules["flask.cli"]
        cli.show_server_banner = lambda *x: None

        if 1:
            log1 = logging.getLogger("werkzeug")
            log1.setLevel(logging.ERROR)

        # 0 => threaded for command line use (when imported)
        if 0:
            self.app.jinja_env.auto_reload = True
            self.app.config["TEMPLATES_AUTO_RELOAD"] = True
            self.app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False
            self.app.config["UPLOAD_FOLDER"] = self.upload_folder
            self.app.run(debug=True, threaded=False, host="0.0.0.0", port=self.port)
        else:
            self.app.jinja_env.auto_reload = True
            self.app.config["TEMPLATES_AUTO_RELOAD"] = True
            self.app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
            self.app.config["UPLOAD_FOLDER"] = self.upload_folder
            self.webthread = threading.Thread(
                target=self.app.run,
                kwargs={
                    "debug": False,
                    "threaded": True,
                    "host": "0.0.0.0",
                    "port": self.port,
                },
            )
            self.webthread.daemon = True  # terminates when main process exits
            self.webthread.start()
            self.is_running = 1

        return
