from flask import Flask
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}
app = Flask(__name__)


def get_status(url):
    try:
        response = requests.get(url, headers=headers)
        return str(response.status_code)
    except:
        pass


def config():
    with open('/metrics/src/configuration/metrics.conf', 'r', encoding='utf-8') as file:
        dic = []
        for line in file.readlines():
            line = line.strip('\n')
            if line == '':
                continue
            b = line.split(',')
            dic.append(b)
    return dict(dic)


@app.route('/metrics')
def metrics(response=''):
    for name, url in config().items():
        code = get_status(url)
        try:
            r = 'ketanyun_' + name + '_status{origin="ketanyun",svc="' + name + '",url="' + url + '"}' + ' ' + code + '\n'
        except:
            pass
        response += r
        r = ''
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
