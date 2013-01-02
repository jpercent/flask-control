### Overview Flask is pretty awesome, but it does not provide a
mechanism for stopping an *in-process* web service.  For example, we
wanted something like the following:
<pre> 
def start(): 
    app.run(...)

t = Thread(target=start, ...)
t.start()

  ... get down on it ...

app.stop()
</pre>
But in flask *0.9*, no such functionality is available, so we
created flask_control.py to fill the gap.  

The flask_control module consists of 2 classes: FlaskMonitor and
FlaskController.  An instance of FlaskController can be used to start
and stop a flask web service.  The FlaskController creates a
FlaskMonitor that can return the request data.  The FlaskController
creates a separate process to run the flask web service and uses
Python IPC to control and communicate with it.

An example follows.
<pre>
# Copyright 2012 James Percent <james@syndeticlogic.org>

from flask import Flask, request
from flask_control import FlaskController

# This example demonstrates how to use the flask_control module.  For more
# information see http://github.com/jpercent/flask-controller.

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
</pre>

The example starts flask in another process and waits for the 1st
request.  It stores the request data and exists after 1 request.

To execute the example file, first create 2 terminals.  In the first terminal
do the following.

<pre>
$ python example.py
</pre>

In the other terminal, do something like the following.

[tab]$ cat <<EOF >out
[tab]> We'll create a text file, then use curl to transfer it to the 
[tab]> in-process web server we started in the other terminal. 
[tab]> 
[tab]> EOF
[tab]$ curl -T out http://localhost:5000/example-put
