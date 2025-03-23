from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from collections import Counter
import statistics

def get_price_list(book_name):
    #配置selenium需要
    service = Service('D:\chromedriver_win32\chromedriver.exe')  # 请替换为你的ChromeDriver实际路径
        # 创建Chrome浏览器实例
    driver = webdriver.Chrome(service=service)
    

    driver.get('https://www.dangdang.com/')

            # 找到搜索框并输入关键词
    search_box = driver.find_element(By.ID, 'key_S')
    search_name = change_key_word(book_name)
    search_box.send_keys(search_name)

            # 找到搜索按钮并点击
    search_button = driver.find_element(By.CSS_SELECTOR, 'input.button')
    search_button.click()

            # 等待页面加载
    time.sleep(5)
    # 定位所有 dd_name="单品标题" 的元素
    title_elements = driver.find_elements(By.CSS_SELECTOR, '[dd_name="单品标题"]')

        # 提取每个元素的 title 属性
    titles = []
    for element in title_elements:
        title = element.get_attribute('title')
        if title:
            titles.append(title)
#     print(titles)
#     print(len(titles))
    
        # 定位所有 class 为 search_now_price 的 span 元素
    price_elements = driver.find_elements(By.CSS_SELECTOR, 'span.search_now_price')

    # 提取每个元素的文本内容
    prices = []
    for element in price_elements:
        price = element.text
        if price[-1] != '起':
            prices.append(price)
#     print(prices)
#     print(len(prices))
    
    
    dic_book = {}
    for index, name in enumerate(titles):
        if name not in dic_book:
            # 如果书名不在字典中，将价格作为单个元素添加到字典中
            dic_book[name] = [prices[index]]
        else:
            # 如果书名已经在字典中，将价格添加到对应的列表中
            dic_book[name].append(prices[index])
    return dic_book


def change_key_word(input_word):
    # 每一本书的简称穷举出来,放在一个大列表里，大列表里的每一个小列表里就是这个书的所有简称
    simple_word_base = [['线代', '线性代数第六版', '线性代数', '线代第六版', '工程数学线性代数'],
                        ['高数', '高数第七版', '高数同济大学第七版', '高数同济大学'],['微积分']]

    # 每一本书搜索最准确最详细的名称
    true_word_base = [['工程数学线性代数第六版'], ['高等数学同济第七版'],['微积分田立平']]

    output_word = input_word  # 先默认输出为输入的词
    for index, name_list in enumerate(simple_word_base):
        if input_word in name_list:
            output_word = true_word_base[index][0]
            break  # 一旦找到匹配的简称，就停止循环
    return output_word


def average_price(data_dic):
# 提取所有价格数字并转换为浮点数
    try:
        all_prices = []
        for values in data_dic.values():
            for price in values:
                price = float(price.replace('¥', ''))
                all_prices.append(price)

        # 找到出现次数最多的数字段

        counter = Counter(all_prices)
        most_common = counter.most_common(1)[0][0]

        # 与中位数偏差过大的数据去除

        median = statistics.median(all_prices)
        filtered_prices = [price for price in all_prices if abs(price - median) < 2 * median]

        # 计算平均值
        average = statistics.mean(filtered_prices)
    except:
        print('请重试')

    return average


def final_price(average_num,hold_year=0,leave_year=4,integrity=1):
    final_price = (average_num*2/3)*integrity*(1+(4-leave_year)/10)*(1-(hold_year)/10)

    return final_price


def recommend(name,hold_year=0,leave_year=4,integrity=1):
    price_list1 = get_price_list(name)

    average_price1 = average_price(price_list1)
    recommend_price = final_price(average_price1,hold_year,leave_year,integrity)
    return recommend_price
    




