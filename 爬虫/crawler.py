# 爬取猫眼专业版网站的数据，获取对应的数据
import requests
import csv


import decoder as de

# 指定爬取月份并给上该月的天数
month, day = 4, 30


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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
                        Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
        'referer': 'https://piaofang.maoyan.com/dashboard',
        'Cookie': '_lxsdk_cuid=18a0220df58c8-09d9a61491c11a-7c54647e-1fa400-18a0220df58c8; \
                    uuid=18a0220df58c8-09d9a61491c11a-7c54647e-1fa400-18a0220df58c8; theme=moviepro; \
                    Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1717814735; \
                    Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1717815923; \
                    _lxsdk=18a0220df58c8-09d9a61491c11a-7c54647e-1fa400-18a0220df58c8; \
                    _lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; \
                    _lxsdk_s=18ff5b75146-7-cb0-96e%7C%7C97'
    }

    # 使用get向当前URL发送请求
    result = requests.get(url, headers=headers)

    # 如果状态码为200，表示请求成功，接着使用result.text来获取服务器返回的响应内容
    if result.status_code == 200:
        print("SUCCESS")
        return result.json()
    else:
        print("ERROR")
    return


def download_all_htmls():
    # 下载所有需要的html页面
    # 下载2024年五月份每日的数据
    htmls = []
    for idx in range(1, day+1):
        month_tmp = '{:02d}'.format(month)
        day_tmp = '{:02d}'.format(idx)
        urlm = f"https://piaofang.maoyan.com/dashboard-ajax/movie?showDate=2024{month_tmp}{day_tmp}"
        print("craw html:", urlm)
        result = get_html(urlm)
        htmls.append(result)
    return htmls


def to_csv(html, count, this_month):
    # 将找到的信息存储到csv文件中
    with open(f'D:/WORK/大三下/影评项目预测/爬取到的数据/cvs缓存/movies_{month}月{count}.csv', mode='w', newline='', encoding='utf-8') \
            as file:
        writer = csv.writer(file)
        # 写入csv文件第一行数据，作为标题
        writer.writerow(["日期", "上座率", "场均人次", "票房占比", "电影ID", "电影名字", "已上映天数", "排片场次",
                         "排片占比", "当日票房", "当日总出票", "当日总场次"])
        # 按照标题给每行写入对应数据
        print(html)
        try:
            for movie in html['movieList']['list']:
                movie_info = movie['movieInfo']
                num_info = movie['boxSplitUnit']
                writer.writerow([(str(this_month) + str('{:02d}'.format(count))), movie['avgSeatView'],
                                movie['avgShowView'], movie['boxRate'], movie_info['movieId'],
                                movie_info['movieName'], movie_info['releaseInfo'], movie['showCount'],
                                movie['showCountRate'], de.decode_html_entities(num_info['num']),
                                 html['movieList']['nationBoxInfo']['viewCountDesc'],
                                 html['movieList']['nationBoxInfo']['showCountDesc']])  # 调用解码器，直接解码票房直接写入
        except KeyError:
            writer.writerow('')


def main():

    htmls1 = download_all_htmls()
    count = 1
    for html in htmls1:
        # 处理数据并生成CSV文件
        to_csv(html, count, month)
        print(f"{month}月{count}号的数据已经爬取成功")
        count += 1


if __name__ == "__main__":
    main()
