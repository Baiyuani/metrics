from flask import Flask
from gevent import pywsgi
import requests
from joblib import Parallel, delayed
from loguru import logger

# logger.add('/metrics/logs/metrics.log')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}
app = Flask(__name__)
data = ''


def get_status(url):
    try:
        response = requests.get(url, headers=headers)
        return str(response.status_code)
    except:
        logger.error("url: \"%s\" is wrong. Unable to get status_code" % url)
        pass


def get_config():
    with open('./configuration/metrics.conf', 'r', encoding='utf-8') as file:
        dic = []
        for line in file.readlines():
            line = line.strip('\n')
            if '#' in line or line == '':
                continue
            dic.append(line.split(','))
    return tuple(dic)


def fork(args):
    handle_data(args[0], args[1])


def handle_data(name, url):
    global data
    code = get_status(url)
    try:
        r = "ketanyun_%s_status{origin=\"ketanyun\",svc=\"%s\",url=\"%s\"} %s\n" % (name, name, url, code)
        data += r
    except:
        pass


@logger.catch
def post():
    Parallel(n_jobs=10, backend='threading')(delayed(fork)(i) for i in config)
    return data


@app.route('/metrics')
@app.route('/live')
@app.route('/ready')
def metrics():
    global data
    res = post()
    data = ''
    return res


@app.route('/')
@app.route('/start')
def main():
    return {'version': '0.1.3'}


if __name__ == '__main__':
    config = get_config()
    # app.run(host='0.0.0.0', port=5000, debug=True)
    # app.run(host='0.0.0.0', port=5000)
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()

