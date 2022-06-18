import yaml
import requests
from joblib import Parallel, delayed
from loguru import logger

data = ''


# logger.add('/metrics/logs/metrics.log')
@logger.catch
def get_urls(namespace, ex_labels):
    name_list = []
    try:
        with open('urls.yaml', 'r', encoding='utf-8') as file:
            # return tuple(map(lambda line: line.replace("'", '').replace('"', '').strip('\n').split(': '),
            #                  filter(lambda line: line != '\n' and '#' not in line,
            #                         file.readlines()
            #                         )
            #                  ))
            yaml_data = yaml.load(file, Loader=yaml.FullLoader)["urls"]
            names = yaml_data.keys()
            urls = yaml_data.values()
            for obj in list(zip(names, urls)):
                if ex_labels is None:
                    name = '%s_web_status{origin=\"%s\",svc=\"%s\",url=\"%s\"}' % (namespace, namespace, obj[0], obj[1])
                    name_list.append(name)
                else:
                    ex_labels = ex_labels.strip('{').strip('}')
                    name = "%s_web_status{origin=\"%s\",svc=\"%s\",url=\"%s\",%s}" % (namespace, namespace, obj[0], obj[1], ex_labels)
                    name_list.append(name)

            return list(zip(name_list, urls))
    except:
        logger.error("file:urls.yaml read faild.")
        exit()


def after():
    global data
    data = ''


@logger.catch
class Metrics:
    def __init__(self, headers, threading_num, urls):
        self.headers = headers
        self.threading_num = threading_num
        self.urls = urls

    def get_status(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            return response.status_code
        except:
            logger.warning("url: \"%s\" is wrong. Unable to get status_code." % url)
            pass

    def main(self, data_label, url):
        global data
        code = self.get_status(url)
        try:
            data_row = "%s %d\n" % (data_label, code)
            data += data_row
        except:
            logger.error("Return data is failed! because: Data splicing failed. --> url: \"%s\". status_code: \"%s\"" % (url, code))
            pass

    def __call__(self):
        Parallel(n_jobs=int(self.threading_num), backend='threading')(
            delayed(lambda args: self.main(args[0], args[1]))(i) for i in self.urls
        )
        return data
