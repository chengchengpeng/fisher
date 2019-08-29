# 一个函数的最后，return这个函数正常返回的结果，前面的if return可以看做正常情况下的一个分支，这样可以简化代码的逻辑复杂性
# requests这个需要下载的包，提供了很人性化的api来获取数据，大多数api用的都是restful,都要求返回json格式的数据
import requests


class HTTP:
    @staticmethod
    def get(url, return_json=True):
        # 获取数据
        r = requests.get(url)
        if r.status_code != 200:
            return {} if return_json else ''
        return r.json() if return_json else r.text
