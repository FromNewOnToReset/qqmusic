import random
import urllib
import urllib.request
import requests
import json

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5509.400 QQBrowser/10.1.1601.400"
]


# 随机头
def random_header():
    headers = {
        "User-Agent": random.choice(USER_AGENTS)
    }
    return headers


# 搜索歌曲名
def search_music_name():
    return input("请输入歌曲名：")


data_search = {
    "ct": "24",
    "qqmusic_ver": "1298",
    "new_json": "1",
    'remoteplace': 'txt.yqq.center',
    "searchid": "71552798001734829",
    "t": "0",
    "aggr": "1",
    "cr": "1",
    "catZhida": "1",
    "lossless": "0",
    "flag_qc": "1",
    "p": "1",
    "n": "50",
    "w": search_music_name(),
    "g_tk": "5381",
    "loginUin": "0",
    "hostUin": "0",
    "format": "jsonp",
    "inCharset": " utf8",
    "outCharset": " utf-8",
    "notice": " 0",
    'platform': 'yqq',
    "needNewCode": " 0"
}
url_search = r"http://c.y.qq.com/soso/fcgi-bin/client_search_cp?"
search_api = requests.get(url_search, params=data_search, headers=random_header())
search_api = search_api.text.replace("callback(", '')[:-1]
music_info = json.loads(search_api)
music_list = music_info["data"]["song"]["list"]


# 获取歌曲时长
def get_sing_time(time):
    m = time // 60
    s = time % 60
    return str(m) + ":" + str(s)


k = 0
for index in range(len(music_list)):
    sing_info = music_list[index]['name']
    singer_name = music_list[index]["singer"][0]["name"]
    albumname = music_list[index]["album"]["name"]
    sing_time = music_list[index]["interval"]
    sing_time = get_sing_time(sing_time)
    k += 1
    print(str(k) + " : " + sing_info + "   歌手：" + singer_name + "     专辑：" + albumname + "   时长：" + sing_time)
num = int(input('请选择你要下载的歌曲：'))

songmid = music_list[num - 1]["file"]["media_mid"]
singName=music_list[num-1]["name"]
singer_name = music_list[num-1]["singer"][0]["name"]
# 获取真正的key
key_url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?callback=getplaysongvkey626277975566637&g_tk=5381&jsonpCallback=getplaysongvkey626277975566637&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&data={"req":{"module":"CDN.SrfCdnDispatchServer","method":"GetCdnDispatch","param":{"guid":"552068528","calltype":0,"userip":""}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"552068528","songmid":["'+songmid+'"],"songtype":[0],"uin":"0","loginflag":1,"platform":"20"}},"comm":{"uin":0,"format":"json","ct":20,"cv":0}}'

key = requests.get(key_url)
key_api = key.text.replace(r"getplaysongvkey626277975566637(", "")[:-1]
key_api = json.loads(key_api)
vkey = key_api["req_0"]["data"]["midurlinfo"][0]["vkey"]
url_ape = "http://183.222.96.19/amobile.music.tc.qq.com/A000"+songmid+".ape?guid=552068528&vkey="+vkey+"&uin=0&fromtag=91&.ape"
url_flac = "http://183.222.96.19/amobile.music.tc.qq.com/F000"+songmid+".flac?guid=552068528&vkey="+vkey+"&uin=0&fromtag=91&.flac"
url_m4a = "http://dl.stream.qqmusic.qq.com/C400"+songmid+".m4a?guid=552068528&vkey="+vkey+"&uin=0&fromtag=66"

# 获取mp3和mpe
get_temp_url = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?'
temp_form = {
    "g_tk": "191874193",
    "loginUin": "1069486284",
    "hostUin": "0",
    "format": "json",
    "inCharset": "utf8",
    "outCharset": "utf-8",
    "notice": "0",
    "platform": "yqq",
    "needNewCode": "0",
    "cid": "205361747",
    "uin": "1069486284",
    "songmid": songmid,
    "filename": "M500" + songmid + ".mp3",
    "guid": "2057046240"
}
temp_link = requests.get(get_temp_url, params=temp_form, headers=random_header())
temp_link = temp_link.json()
temp_link = temp_link["data"]["items"][0]
url_mp3 = "http://dl.stream.qqmusic.qq.com/" + temp_link["filename"] + "?guid=2057046240&vkey=" + temp_link[
    "vkey"] + "&uin=0&fromtag=88"
print("1.flac:     "+url_flac)
print("2.ape:      "+url_ape)
print("3.mp3:      "+url_mp3)
print("4.m4a:      "+url_m4a)

choice={
    "1":url_flac,
    "2":url_ape,
    "3":url_mp3,
    "4":url_m4a
}
type={
    "1": ".flac",
    "2": ".ape",
    "3": ".mp3",
    "4": ".m4a"
}
n = int(input('请选择：'))

print(choice[str(n)])
try:
    urllib.request.urlretrieve(choice[str(n)],singName+"-"+singer_name+type[str(n)])
    print("下载完成")
except:
    print("下载失败")
