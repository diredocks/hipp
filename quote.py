import csv
import os
import random
from uuid import uuid4
from datetime import datetime

# 管理员鉴权
admin_token = str(uuid4())
print(admin_token)

# 定义CSV文件的字段名
fieldnames = ['quote_type', 'source', 'author', 'quote', 'length', 'add_time', 'uuid']

# CSV文件路径
csv_file = 'quotes.csv'

# 如果文件不存在，则创建并写入字段名
def check_exists():
    if not os.path.exists(csv_file):
        with open(csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

# 添加名言
def add_quote(quote_type, source, author, quote, token):
    check_exists()
    if token == admin_token:
        with open(csv_file, 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
            writer.writerow({
                'quote_type': quote_type,
                'source': source,
                'author': author,
                'quote': quote,
                'length': len(quote),
                'add_time': datetime.now().strftime('%Y-%m-%d_%H:%M:%S'),
                'uuid': str(uuid4())
            })
        return 200
    else:
        return 401

def fetch_quote(quote_type):
    results = search_quote(quote_type, "quote_type")['results']
    if len(results) > 0 :
        #print(random.choice(results))
        return random.choice(results)
    else:
        return 404

# 查找名言
def search_quote(keyword, fieldnames):
    check_exists()
    results = []
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                #if keyword in row[fieldnames]:
                if keyword == row[fieldnames]:
                    results.append(row)
            except KeyError:
                print('KeyError and Please check!')
                return 400
    results = {
        'count': len(results),
        'results': results
    }
    #print(results)
    return results

# 删除名言
def delete_quote(uuid):
    check_exists()
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        quotes = list(csv.DictReader(file))
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for quote in quotes:
            if uuid not in quote['uuid']:
                writer.writerow(quote)
                print('Successfully deleted quote')
                return 204
    print('Quote not found!')
    return 404

# 测试
add_quote('d', '《论语》', '孔子', '学而时习之，不亦说乎？', admin_token)
add_quote('d', '《哈姆雷特》', '莎士比亚', 'To be or not to be, that is a question.', admin_token)
add_quote('d', '《战争与和平》', '列夫·托尔斯泰', '历史是由一连串单个事件组成的。', admin_token)
#search_quote('孔子', 'author')
#delete_quote('莎士比亚')

