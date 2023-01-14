from flask import Flask
from gevent import pywsgi
from __init__ import __version__
import common as c
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}

environment = os.environ.get('WM_ENV', 'prod')
if environment == 'prod':
    from settings_prod import *
else:
    from settings_dev import *
host = app_config["host"]
port = app_config["port"]
context_path = app_config["context_path"]
threading_num = app_config["threading_num"]
namespace = app_config["namespace"]
ex_labels = app_config["ex_labels"]

app = Flask(__name__)
urls = c.get_urls(namespace, ex_labels)
call = c.Metrics(headers, threading_num, urls)


@app.route(context_path)
@app.route('/live')
@app.route('/ready')
def metrics():
    res = call()
    c.after()
    return res


@app.route('/')
@app.route('/start')
def root():
    return {'version': __version__}


if __name__ == '__main__':
    server = pywsgi.WSGIServer(
        (host, int(port)),
        app
    )
    server.serve_forever()
    # app.run(host=host, port=int(port), debug=True)
