# coding:utf-8
from __future__ import unicode_literals
from flask import *
import json
import re
import time
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import pymongo

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    read_count = 10
    read_count2 = read_count
    result_list = []
    client = pymongo.MongoClient(host="10.240.17.169", port=27017)
    #   client.admin.authenticate("root", "hitnslab")
    db = client['ip_db']
    # 在此处更改为你自己的网站名称！
    collection = db['nr6']
    keep_collection = db['nr6']
    print "??"
    # 区分不同文档（无用？）
    dict_count = 0

    big_title = "无标题"

    name_set = set()
    name_list = []

    # 复制要读取的文档数量
    temp_count = read_count

    for document in collection.find():
        # 默认无标题

        for node in document["nodes"]:
            name_set.add(node["name"])
            name_list.append(node['name'])

        read_count -= 1
        if read_count == 0:
            break
        dict_count += 1
        print "已经到了 "+str(dict_count)+" 个文件"

    t = 0
    read_count = temp_count
    for document in keep_collection.find():
        new_dict = {}
        node_list = []
        for node in document["nodes"]:
            if node["name"] in name_set:
                count = name_list.count(node["name"])
                if count > 1:
                    node["category"] = "公共"
                node["value"] = count
                if node["name"] == "我们":
                    node["name"] = "本保险公司_"
                node_list.append(node)
                if node["name"] == "本保险公司_":
                    name_set.remove("我们")
                else:
                    name_set.remove(node["name"])
                print node["name"], node["category"]

        new_dict["nodes"] = node_list
        new_dict["relations"] = document["relations"]
        result_list.append(new_dict)
        t+=1
        print t
        read_count -= 1
        if read_count == 0:
            break
    nodes = []
    links = []

    for i in result_list:
        nodes.extend(i["nodes"])
        links.extend(i["relations"])

    for index, node in enumerate(nodes):
        nodes[index]["symbolSize"] *= 2

    data1 = json.dumps(nodes)
    data2 = json.dumps(links)
    category = []
    Category = []

    for i in range(read_count2):
        temp = {}
        category.append(result_list[i]["nodes"][0]["category"])
        temp["name"] = result_list[i]["nodes"][0]["category"]
        Category.append(temp)

    data3 = json.dumps(category)
    data4 = json.dumps(Category)
    return render_template('graph.html',data1 = data1,data2 = data2,data3 = data3,data4 = data4)

if __name__ == '__main__':
    app.run(host='127.0.0.1')

