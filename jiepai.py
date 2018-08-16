import requests, re, json, os
from urllib import request, parse


def down(search, url):
    # 判断文件夹是否存在,如果存在,则不创建,如果不存在,则创建
    if not os.path.exists(search):
        os.mkdir(search)

    filename = search+'/' + url.split('/')[-1] + '.jpg'
    # 下载图片
    request.urlretrieve(url, filename)
    print('正在下载%s'%filename)


# 传入爬取页数, 输入要抓取的内容
def jinri(page, search):
    url = 'https://www.toutiao.com/search_content/?offset={}&format=json&{}&autoload=true&count=20&cur_tab=1&from=search_tab'
    # 通过分析URL 发现keyword 是进行url加密的 所以调用parse 对其进行urlencode加密
    data = {
        'keyword': search
    }
    data_str = parse.urlencode(data)
    data_bytes = data_str.encode('utf-8').decode('utf-8')
    # print(data_bytes)
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }

    for i in range(page):
        # 通过对比分析出 url 的变量是offset 所以猜测是分页, 经过测试 确实是 
        i *= 20
        # 对URL 进行拼接
        full_url = url.format(i, data_bytes)
        html = requests.get(full_url, headers=headers)
        # 调用requests包中的json()方法 将其转成dict格式
        json_list = html.json()
        # 通过分析json数据得出 列表中的第1条数据没有 所以进行一个切片处理
        for j in json_list[1:]:
            # 由于数据的不完整性, 有的数据没有article_url 会导致程序报错, 故进行异常捕获 也可以用if 语句判断
            try:
                dict_url = j['article_url']
                html = requests.get(dict_url, headers=headers).text
                # 通过得到的 url 进入详情页, 利用正则匹配出想要的 img 链接
                html_req = re.compile(r'gallery: JSON.parse\((.*)\)')
                html_res = html_req.search(html).group(1)
                # print(html_res)
                # 通过json转码后发现还是str格式 所以进行二次json解码 直到想要的dict 格式
                html_info = json.loads(html_res)
                html_dict = json.loads(html_info)
                img_info = html_dict['sub_images']
                for img in img_info:
                    # 找到img url 调用down函数
                    down(search, img['url'])
                    # print()
                # print(type(html_dict), html_dict)
            except KeyError as e:
                pass
if __name__ == '__main__':
    serch = input('请输入想要爬取得内容:')
    page = int(input('请输入爬取页数:'))
    jinri(page, serch)