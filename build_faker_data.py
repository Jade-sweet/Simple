import os
import random
import sqlite3

from faker import Faker
import time

threads_maximum = 1  # 表数量: 和执行线程数绑定,建议小于150
commit_maximum = 1  # 每次提交数据量
table_name = "houseInfo"  # 表名
data_size = 1000  # 每张表插入数据量

fake = Faker("zh-CN")


def create_data():
    conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'db.sqlite3'))
    cursor = conn.cursor()
    for i in range(1, 1001):
        c = (fake.msisdn(), fake.company_prefix() + '区', fake.street_name(), fake.street_name()+'小区', random.randint(3000, 100000), random.randint(40, 200), 'https://:'+fake.ssn())
        print(f'正在生成{i}条', end='\r\n')
        # cursor.execute("""insert into ? (house_id, county, street, xiaoqu, price, area, detail_link) values (?,?,?,?,?,?,?)""", c)
        cursor.execute("""insert into houseInfo (house_id, county, street, xiaoqu, price, area, detail_link) values (?,?,?,?,?,?,?)""", c)
        conn.commit()
    print('结束...')
    cursor.close()
    conn.close()


if __name__ == "__main__":
    create_data()