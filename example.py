#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2012 James Percent <james@syndeticlogic.org>
#
import sys
from flask import Flask, request
from time import sleep
from flask_control import FlaskController
#
# This module demonstrates how to use the flask_control module. For more
# information see http://github.com/jpercent/flask-control
#
app = Flask(__name__)
        
@app.route("/example-put", methods=['PUT'])
def exput():
    return 'OK'

@app.route("/example-get", methods=['GET'])
def exget():
    return 'OK'

def get_app():
    return app

def start():
    eb = FlaskController(get_app, True)
    eb.start()
    request_data = eb.next()
    print request_data
    eb.stop()
    eb.await()

if __name__ == '__main__':
    start()
