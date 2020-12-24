import json
from collections import OrderedDict
# 读取json文件内容,返回字典格式
def readconfig():
    with open('./config.json','r',encoding='utf8')as fp:
        # 保持原有顺序
        json_data = json.load(fp,object_pairs_hook=OrderedDict)
        # print('这是文件中的json数据：',json_data)
        return json_data
        
        # print(json_data.keys())
        # print(json_data['showType'])

if __name__ == "__main__":
    readconfig()