from flask import Flask
from gevent import pywsgi
import requests
from joblib import Parallel, delayed
from loguru import logger
from __init__ import __version__
import os
import yaml


env = os.environ.get('WM_ENV', 'prod')
if env == 'prod':
    from settings_prod import *
else:
    from settings_dev import *
host = app_config["host"]
port = app_config["port"]
context_path = app_config["context_path"]
threading_num = app_config["threading_num"]
namespace = app_config["namespace"]
ex_labels = app_config["ex_labels"]
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}
app = Flask(__name__)
data = ''


# logger.add('/metrics/logs/metrics.log')
@logger.catch
def get_status(url):
    try:
        response = requests.get(url, headers=headers)
        return response.status_code
    except:
        logger.warning("url: \"%s\" is wrong. Unable to get status_code." % url)
        pass


@logger.catch
def get_urls():
    try:
        with open('urls.yaml', 'r', encoding='utf-8') as file:
            # return tuple(map(lambda line: line.replace("'", '').replace('"', '').strip('\n').split(': '), filter(lambda line: line != '\n' and '#' not in line, file.readlines())))
            yaml_data = yaml.load(file, Loader=yaml.FullLoader)["urls"]
            return list(zip(yaml_data.keys(), yaml_data.values()))
    except:
        logger.error("file:urls.yaml read faild.")
        exit()


@logger.catch
def handle_data(name, url):
    global data, ex_labels
    code = get_status(url)
    if code is not None:
        try:
            data_head = "%s_%s_status" % (namespace, name)
            if not ex_labels:
                data_label = "{origin=\"%s\",svc=\"%s\",url=\"%s\"}" % (namespace, name, url)
            else:
                ex_labels = ex_labels.strip('{').strip('}')
                data_label = "{origin=\"%s\",svc=\"%s\",url=\"%s\",%s}" % (namespace, name, url, ex_labels)
            data_row = "%s%s %d\n" % (data_head, data_label, code)
            data += data_row
        except:
            logger.error("Return data is failed! because: Data splicing failed.|name: \"%s\"|url: \"%s\"|code: \"%s\"" % (name, url, code))
            pass


@logger.catch
def main():
    Parallel(n_jobs=int(threading_num), backend='threading')(delayed(lambda args: handle_data(args[0], args[1]))(i) for i in urls)
    return data


@app.route(context_path)
@app.route('/live')
@app.route('/ready')
def metrics():
    global data
    res = main()
    data = ''
    return res


@app.route('/')
@app.route('/start')
def root():
    return {'version': __version__}


if __name__ == '__main__':
    urls = get_urls()
    # app.run(host=host, port=int(port), debug=True)
    server = pywsgi.WSGIServer((host, int(port)), app)
    server.serve_forever()
