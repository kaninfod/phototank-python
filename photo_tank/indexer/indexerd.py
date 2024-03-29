#! /usr/bin/env python

__author__ = 'hingem'
import sys

from photo_tank.bin.daemon import Daemon
from photo_tank.indexer.files_watcher import file_watcher
from photo_tank.indexer.location_watcher import location_watcher
from photo_tank.indexer.dropbox_watcher import dropbox_watcher
from photo_tank.app import app
from time import sleep

class MyDaemon(Daemon):

    def run(self):

        while True:
            app.logger.debug("starting new watcher cycle")

            if app.config["WATCHER_FILES"]:
                app.logger.debug("Running file watcher")
                file_watcher()

            if app.config["WATCHER_LOCATION"]:
                app.logger.debug("Running location watcher")
                location_watcher()

            if app.config["WATCHER_DROPBOX"]:
                app.logger.debug("Running Dropbox watcher")
                dropbox_watcher()
            if app.config["RUN_ONCE"]:
                break

            sleep(app.config["WATCHER_INTERVAL"])


if __name__ == "__main__":
    daemon = MyDaemon('/tmp/idx.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
            app.logger.debug("Indexer started.")
        elif 'stop' == sys.argv[1]:
            daemon.stop()
            app.logger.debug("Indexer stopped.")
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)







