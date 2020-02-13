import requests
import json
import folium
import pprint

def baidu_map(address):
    ak = 'LEQMFQFSwhybaLhS9gIAZWL4llzY0M7o'  # ak需要去百度地图申请
    url = 'http://api.map.baidu.com/geocoding/v3/?address={inputAddress}&output=json&ak={myAk}'.format(
                    inputAddress=address, myAk=ak)
    res = requests.get(url)
    json_data = json.loads(res.text)
    if(json_data["status"]==0):
        pprint.pprint(json_data)  # 美观打印数据结构
        lat = json_data['result']['location']['lat']  # 经度
        lng = json_data['result']['location']['lng']  # 纬度

        san_map = folium.Map(location=[lat,lng], zoom_start=12)
        san_map.save('templates/test.html')
        return json_data
    else:
        return 0

#baidu_map('河北师范大学')
