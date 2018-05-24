#encoding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from pyquery import  PyQuery as pq
import random
import re
import requests
import csv
import codecs
import time
from selenium import webdriver
import os
from xpinyin import Pinyin
from HTMLParser import HTMLParser


#######函数作用：写入csv
def csv_write(list,file_path):
    csvFile2 = open(file_path, 'ab')  # 设置newline，否则两行之间会空一行
    csvFile2.write(codecs.BOM_UTF8)
    ####将文章title和html写入csv文件
    writer = csv.writer(csvFile2)
    #####写入csv文件
    writer.writerow(list)
    csvFile2.close()




if __name__ == '__main__':
    ###############动态加载相应地区网页
    city_names = raw_input("请输入地区名字（比如成都、北京）：")
    city_name_lists = city_names.split("、")
    city_non_data = []

    for city_name in city_name_lists:
        #############将地区名字转为拼音作为csv名字
        p = Pinyin()
        csv_name = p.get_pinyin(city_name.decode()) + ".csv"

     #########网站首页地址
        web_url = "https://www.aqistudy.cn/historydata/"
        abspath = os.path.abspath(r"D:\Install_exe\chromedriver\chromedriver_win32\chromedriver.exe")
        driver = webdriver.Chrome(abspath)
        driver.get(web_url)
        ############找到name为city的输入框
        name = driver.find_element_by_name('city')
        ##########中文要解码为unicode
        name.send_keys(city_name.decode())
        ############找到提交框
        submit = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/form/button")
        submit.click()
        time.sleep(2)
        ##########得到网页源码
        city_page_source = driver.page_source.encode('utf-8')
        driver.close()


    #####判断该地区有无天气数据###########
        ########地区首页表格
        string = re.findall("<tbody>(.*?)</tbody>",city_page_source,re.S)[0]
        ###########判断地区首页是否有天气数据
        url_lists = re.findall('<td(.*?)</td>',string,re.S)
        page_exit_tag = 0
        if len(url_lists) == 0:
            # print "该地区没有天气数据"
            city_non_data.append(city_name)
        else:
            page_exit_tag = 1

        #########网站url前缀
        ex_url = 'https://www.aqistudy.cn/historydata/'

        if page_exit_tag == 1:
            ######提取出地区网页所有不同的月份网页url
            string = re.findall("unstyled1(.*?)</div>",city_page_source,re.S)[0]
            url_lists = re.findall('href="(.*?)">',string,re.S)
            month_url_list = []
            for i in url_lists:

                month_url = ex_url + HTMLParser().unescape(i)
                # print month_url
                month_url_list.append(month_url)
            # print month_url_list
            ################test################

            ####################动态加载某个城市的天气表格
            tag = 0
            for month_url in month_url_list:
                logo = "下载" + city_name + "的数据。。。。"
                print logo
                abspath = os.path.abspath(r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
                driver = webdriver.Chrome(abspath)
                #########加载入口地址
                driver.get(month_url)
                time.sleep(3)
                page_source = driver.page_source
                driver.close()
                ###################匹配出表格部分
                table_sec = re.findall("<tbody>(.*?)</tbody>",page_source,re.S)[0]
                ################匹配出表格标题
                doc_th = pq( table_sec)
                th = doc_th('th').items()

                #########将表格题目存入列表
                th_list = []
                for i in th:
                    th_text = i.text()
                    th_list.append(th_text)
                print th_list
                if tag == 0:
                    csv_write(th_list, csv_name)
                ##############匹配出表格内容
                doc_td = pq(table_sec)
                td = doc_td('tr td').items()
                ##############将表格按行存入列表
                td_list = []
                j = 0
                k = 2
                for i in td:
                    if j < 9:
                        td_list.append(i.text())

                        if j == 8:
                            csv_write(td_list, csv_name)

                            print td_list
                        j += 1

                    else:
                        td_list = []
                        td_list.append(i.text())
                        j = 1
                tag += 1

    print "以下地区没有天气数据:"
    for i in city_non_data:
        print i


