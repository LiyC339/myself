# 根据电影id去爬取对应网站的内容
import numpy as np
import requests
import pandas as pd
from bs4 import BeautifulSoup


def read_csv_values(file_path):
    # 读取 CSV 文件
    df = pd.read_csv(file_path)

    # 获取 DataFrame 的所有值
    values = df.values

    return values


def remove_brackets_from_array(arr):
    # 将数组转换为字符串
    arr_str = np.array2string(arr, separator=',')
    # 去掉方括号
    arr_str = arr_str.replace('[', '').replace(']', '')
    # 将处理后的字符串转换回数组
    cleaned_data = np.fromstring(arr_str, dtype=int, sep=',')
    return cleaned_data


def get_html(url):
    # 伪装和请求响应
    # 在要被爬取的网页 -- F12 -- Network -- all -- 4 -- header -- 找到对应信息复制粘贴过来
    # 加入headers伪装成人工操作行为，防止被网站反爬
    headers = {  # 设置header
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,\
                    image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
        'referer': 'https://piaofang.maoyan.com/',
        'Cookie': '_lxsdk_cuid=18a0220df58c8-09d9a61491c11a-7c54647e-1fa400-18a0220df58c8; \
                    uuid=18a0220df58c8-09d9a61491c11a-7c54647e-1fa400-18a0220df58c8; theme=moviepro; \
                    Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1717814735; \
                    Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1717815923; \
                    _lxsdk=18a0220df58c8-09d9a61491c11a-7c54647e-1fa400-18a0220df58c8; \
                    _lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; \
                    _lxsdk_s=18ff5b75146-7-cb0-96e%7C%7C97'
    }

    # 使用get向当前URL发送请求
    result = requests.get(url, headers=headers)  # , headers=headers

    # 如果状态码为200，表示请求成功，接着使用result.text来获取服务器返回的响应内容
    if result.status_code == 200:
        print("SUCCESS")
        return result.text
    else:
        print("ERROR")
    return


def download_all_htmls(mid):
    # 下载所有需要的html页面

    htmls = []

    # 按照id访问对应电影的详细网站
    for row in mid:
        urlm = f"https://piaofang.maoyan.com/movie/{row}"
        print("craw html:", urlm)
        result = get_html(urlm)
        htmls.append(result)
    return htmls


def parsing_one_html(html, mid):
    # 解析当html页面
    soup = BeautifulSoup(html, 'html.parser')
    datas = []

    # 电影类别
    movie_class = soup.find('p', class_='info-category')
    movie_class_text = movie_class.get_text(strip=True) if movie_class else ''

    # 电影名字
    movie_name = soup.find('span', class_='info-title-content')
    movie_name_text = movie_name.get_text(strip=True) if movie_name else ''

    # 电影评分
    movie_rank = soup.find('span', class_='rating-num')
    movie_rank_text = movie_rank.get_text(strip=True) if movie_rank else ''

    # 男性占比
    try:
        man_rate = soup.find('div', class_='persona-line-item male').find('div', class_='persona-item-value')
        man_rate_text = man_rate.get_text(strip=True) if man_rate else ''
    except AttributeError:
        man_rate_text = ''

    # 女性占比
    try:
        woman_rate = soup.find('div', class_='persona-line-item female').find('div', class_='persona-item-value')
        woman_rate_text = woman_rate.get_text(strip=True) if woman_rate else ''
    except AttributeError:
        woman_rate_text = ''

    # 出品国家
    country = soup.find('p', class_='.ellipsis-1')
    country_text = country.get_text(strip=True) if country else ''

    datas.append({
        '电影id': mid,
        '电影名称': movie_name_text,
        '出品国家': country_text,
        '电影类别': movie_class_text,
        '电影评分': movie_rank_text,
        '男性占比': man_rate_text,
        '女性占比': woman_rate_text
    })

    return datas


def save_to_csv(datas, filename):
    # 保存为csv
    df = pd.DataFrame(datas)
    df.to_csv(filename, index=False, encoding='utf-8')


def main():
    # 读取csv中的movie_id
    file_path = 'D:/WORK/大三下/影评项目预测/数据处理/movie_id.csv'
    values = read_csv_values(file_path)

    # 读取到的values属于np数组，带[]方括号，需要转换为字符串并去扩号
    cleaned_data = remove_brackets_from_array(values)

    htmls2 = download_all_htmls(cleaned_data)
    indx = 0
    for html in htmls2:
        mid = cleaned_data[indx]
        datas = parsing_one_html(html, mid)
        save_to_csv(datas, f'D:/WORK/大三下/影评项目预测/爬取到的数据/ID电影类别/movies_{mid}.csv')
        print(f'电影{mid}爬取成功')
        indx += 1


if __name__ == "__main__":
    main()
