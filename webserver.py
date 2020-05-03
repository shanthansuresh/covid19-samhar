from flask import Flask, render_template
import os

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
app.config['TEMPLATES_AUTO_RELOAD'] = True

# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response

@app.route('/')
def hello():
    return render_template('hello.html')

def webserver_run():
    app.run(host='0.0.0.0', port=1234, debug=True)

