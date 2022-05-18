from flask import Flask
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}


"""python内置变量__name__的值是字符串__main__ 。Flask类将这个参数作为程序名称。当然这个是可以自定义的，比如app = Flask("my-app")。"""
app = Flask(__name__)
"""Flask默认使用static目录存放静态资源，templates目录存放模板，这是可以通过设置参数更改的：
app = Flask("my-app", static_folder="path1", template_folder="path2")
"""


def get_status(url):
    try:
        response = requests.get(url, headers=headers)  # 生成一个response对象
        return str(response.status_code)  # 状态码
    except:
        pass


def config():
    with open('/metrics/src/configuration/metrics.conf', 'r', encoding='utf-8') as file:
        dic = []
        for line in file.readlines():
            line = line.strip('\n')
            if line == '':  # 去除空行
                continue
            b = line.split(',')
            dic.append(b)
    return dict(dic)


@app.route('/metrics')
def metrics(response=''):
    for name, url in config().items():
        code = get_status(url)
        try:
            r = 'ketanyun_' + name + '_status{origin="ketanyun"}' + ' ' + code + '\n'
        except:
            pass
        response += r
        r = ''
    return response


if __name__ == '__main__':
    # create_app().run(host='0.0.0.0', port=5000)
    app.run(host='0.0.0.0', port=5000, debug=True)  # 调试模式
