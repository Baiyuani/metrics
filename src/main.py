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


@logger.catch
def get_status(url):
    try:
        response = requests.get(url, headers=headers)
        return str(response.status_code)
    except:
        logger.warning("url: \"%s\" is wrong. Unable to get status_code." % url)
        pass


@logger.catch
def get_config():
    with open('/metrics/src/configuration/metrics.conf', 'r', encoding='utf-8') as file:
        return tuple(map(lambda line: line.replace("'", '').replace('"', '').strip('\n').split(': '), filter(lambda line: line != '\n' and '#' not in line, file.readlines())))


@logger.catch
def handle_data(name, url):
    global data
    code = get_status(url)
    if code is not None:
        try:
            data_row = "ketanyun_%s_status{origin=\"ketanyun\",svc=\"%s\",url=\"%s\"} %s\n" % (name, name, url, code)
            data += data_row
        except:
            logger.error("Return data is failed! because: Data splicing failed.|name: \"%s\"|url: \"%s\"|code: \"%s\"" % (name, url, code))
            pass


@logger.catch
def main():
    Parallel(n_jobs=10, backend='threading')(delayed(lambda args: handle_data(args[0], args[1]))(i) for i in config)
    return data


@app.route('/metrics')
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
    return {'version': '1.0.1'}


if __name__ == '__main__':
    config = get_config()
    # app.run(host='0.0.0.0', port=5000, debug=True)
    # app.run(host='0.0.0.0', port=5000)
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()
