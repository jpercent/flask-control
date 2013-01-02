### Overview 

Flask is pretty awesome, but out of the box it does not provide a
mechanism for stopping the web service.  As example, we wanted
something like the following:

<pre> 
def start(): 
    app.run(...)

t = Thread(target=start, ...)
t.start()

  ... get down on it ...

app.stop()
</pre>

But in the current version of flask, which is *0.9*, this is not
possible.  When running *in-process* this can be painful because the
entire process needs to be externally killed to restart the web
service.

To work around this, we built the flask_control module.  It consists
of 2 classes: FlaskMonitor and FlaskController.  An instance of
FlaskController can be used to start and stop a flask web service.
The FlaskController creates a FlaskMonitor that can return the request
data.  The FlaskController creates a separate process to run the flask
web service and uses Python IPC to control it.

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
    fc = FlaskController(get_app, True)
    fc.start()
    request_data = fc.next()
    print request_data
    fc.stop()
    fc.await()

if __name__ == '__main__':
    start()
</pre>

The example creates a FlaskController parameterized with a function to
get the flask application context and request_data_sync set to true.
Setting the request_data_sync to true tells the FlaskController to
intercept and record the body of each request.  Next the example
starts the flask web service in separate process, waits for the first
request to complete and gracefully stops flask.

To execute the example file, first create 2 terminals.  In the first terminal
do the following.

<pre>
$ python example.py
</pre>

In the other terminal, do something like the following.

``
$ cat <<EOF >out
> We'll create a text file, then use curl to transfer it to the 
> in-process web server we started in the other terminal. 
> 
> EOF
$ curl -T out http://localhost:5000/example-put
``
