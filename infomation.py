import time
import datetime
import requests
import json
import re
from bs4 import BeautifulSoup

provinceDict = {
    2: '北京', 3: '安徽', 4: '福建', 5: '甘肃', 6: '广东', 7: '广西', 8: '贵州',
    9: '海南', 10: '河北', 11: '河南', 12: '黑龙江', 13: '湖北', 14: '湖南', 15: '吉林',
    16: '江苏', 17: '江西', 18: '辽宁', 19: '内蒙古', 20: '宁夏', 21: '青海', 22: '山东',
    23: '山西', 24: '陕西', 25: '上海', 26: '四川', 27: '天津', 28: '西藏', 29: '新疆',
    30: '云南', 31: '浙江', 32: '重庆', 33: '香港', 34: '澳门', 35: '台湾'
}

cityDict = {
    2: {2: '北京'},
    3: {36: '安庆', 37: '蚌埠', 38: '巢湖', 39: '池州', 40: '滁州', 41: '阜阳', 42: '淮北',
        43: '淮南', 44: '黄山', 45: '六安', 46: '马鞍山', 47: '宿州', 48: '铜陵', 49: '芜湖',
        50: '宣城', 51: '亳州', 52: '合肥'},
    4: {53: '福州', 54: '龙岩', 55: '南平', 56: '宁德', 57: '莆田', 58: '泉州', 59: '三明',
        60: '厦门', 61: '漳州'},
    5: {62: '兰州', 63: '白银', 64: '定西', 65: '甘南', 66: '嘉峪关', 67: '金昌', 68: '酒泉',
        69: '临夏', 70: '陇南', 71: '平凉', 72: '庆阳', 73: '天水', 74: '武威', 75: '张掖'},
    6: {76: '广州', 77: '深圳', 78: '潮州', 79: '东莞', 80: '佛山', 81: '河源', 82: '惠州',
        83: '江门', 84: '揭阳', 85: '茂名', 86: '梅州', 87: '清远', 88: '汕头', 89: '汕尾',
        90: '韶关', 91: '阳江', 92: '云浮', 93: '湛江', 94: '肇庆', 95: '中山', 96: '珠海'},
    7: {97: '南宁', 98: '桂林', 99: '百色', 100: '北海', 101: '崇左', 102: '防城港',
        103: '贵港', 104: '河池', 105: '贺州', 106: '来宾', 107: '柳州', 108: '钦州',
        109: '梧州', 110: '玉林'},
    8: {111: '贵阳', 112: '安顺', 113: '毕节', 114: '六盘水', 115: '黔东南', 116: '黔南',
        117: '黔西南', 118: '铜仁', 119: '遵义'},
    9: {120: '海口', 121: '三亚', 122: '白沙', 123: '保亭', 124: '昌江', 125: '澄迈县',
        126: '定安县', 127: '东方', 128: '乐东', 129: '临高县', 130: '陵水', 131: '琼海',
        132: '琼中', 133: '屯昌县', 134: '万宁', 135: '文昌', 136: '五指山', 137: '儋州'},
    10: {138: '石家庄', 139: '保定', 140: '沧州', 141: '承德', 142: '邯郸', 143: '衡水',
         144: '廊坊', 145: '秦皇岛', 146: '唐山', 147: '邢台', 148: '张家口'},
    11: {149: '郑州', 150: '洛阳', 151: '开封', 152: '安阳', 153: '鹤壁', 154: '济源',
         155: '焦作', 156: '南阳', 157: '平顶山', 158: '三门峡', 159: '商丘', 160: '新乡',
         161: '信阳', 162: '许昌', 163: '周口', 164: '驻马店', 165: '漯河', 166: '濮阳'},
    12: {167: '哈尔滨', 168: '大庆', 169: '大兴安岭', 170: '鹤岗', 171: '黑河', 172: '鸡西',
         173: '佳木斯', 174: '牡丹江', 175: '七台河', 176: '齐齐哈尔', 177: '双鸭山',
         178: '绥化', 179: '伊春'},
    13: {180: '武汉', 181: '仙桃', 182: '鄂州', 183: '黄冈', 184: '黄石', 185: '荆门',
         186: '荆州', 187: '潜江', 188: '神农架林区', 189: '十堰', 190: '随州', 191: '天门',
         192: '咸宁', 193: '襄樊', 194: '孝感', 195: '宜昌', 196: '恩施'},
    14: {197: '长沙', 198: '张家界', 199: '常德', 200: '郴州', 201: '衡阳', 202: '怀化',
         203: '娄底', 204: '邵阳', 205: '湘潭', 206: '湘西', 207: '益阳', 208: '永州',
         209: '岳阳', 210: '株洲'},
    15: {211: '长春', 212: '吉林', 213: '白城', 214: '白山', 215: '辽源', 216: '四平',
         217: '松原', 218: '通化', 219: '延边'},
    16: {220: '南京', 221: '苏州', 222: '无锡', 223: '常州', 224: '淮安', 225: '连云港',
         226: '南通', 227: '宿迁', 228: '泰州', 229: '徐州', 230: '盐城', 231: '扬州',
         232: '镇江'},
    17: {233: '南昌', 234: '抚州', 235: '赣州', 236: '吉安', 237: '景德镇', 238: '九江',
         239: '萍乡', 240: '上饶', 241: '新余', 242: '宜春', 243: '鹰潭'},
    18: {244: '沈阳', 245: '大连', 246: '鞍山', 247: '本溪', 248: '朝阳', 249: '丹东',
         250: '抚顺', 251: '阜新', 252: '葫芦岛', 253: '锦州', 254: '辽阳', 255: '盘锦',
         256: '铁岭', 257: '营口'},
    19: {258: '呼和浩特', 259: '阿拉善盟', 260: '巴彦淖尔盟', 261: '包头', 262: '赤峰',
         263: '鄂尔多斯', 264: '呼伦贝尔', 265: '通辽', 266: '乌海', 267: '乌兰察布市',
         268: '锡林郭勒盟', 269: '兴安盟'},
    20: {270: '银川', 271: '固原', 272: '石嘴山', 273: '吴忠', 274: '中卫'},
    21: {275: '西宁', 276: '果洛', 277: '海北', 278: '海东', 279: '海南', 280: '海西',
         281: '黄南', 282: '玉树'},
    22: {283: '济南', 284: '青岛', 285: '滨州', 286: '德州', 287: '东营', 288: '菏泽',
         289: '济宁', 290: '莱芜', 291: '聊城', 292: '临沂', 293: '日照', 294: '泰安',
         295: '威海', 296: '潍坊', 297: '烟台', 298: '枣庄', 299: '淄博'},
    23: {300: '太原', 301: '长治', 302: '大同', 303: '晋城', 304: '晋中', 305: '临汾',
         306: '吕梁', 307: '朔州', 308: '忻州', 309: '阳泉', 310: '运城'},
    24: {311: '西安', 312: '安康', 313: '宝鸡', 314: '汉中', 315: '商洛', 316: '铜川',
         317: '渭南', 318: '咸阳', 319: '延安', 320: '榆林'},
    25: {321: '上海'},
    26: {322: '成都', 323: '绵阳', 324: '阿坝', 325: '巴中', 326: '达州', 327: '德阳',
         328: '甘孜', 329: '广安', 330: '广元', 331: '乐山', 332: '凉山', 333: '眉山',
         334: '南充', 335: '内江', 336: '攀枝花', 337: '遂宁', 338: '雅安', 339: '宜宾',
         340: '资阳', 341: '自贡', 342: '泸州'},
    27: {343: '天津'},
    28: {344: '拉萨', 345: '阿里', 346: '昌都', 347: '林芝', 348: '那曲', 349: '日喀则',
         350: '山南'},
    29: {351: '乌鲁木齐', 352: '阿克苏', 353: '阿拉尔', 354: '巴音郭楞', 355: '博尔塔拉',
         356: '昌吉', 357: '哈密', 358: '和田', 359: '喀什', 360: '克拉玛依', 361: '克孜勒苏',
         362: '石河子', 363: '图木舒克', 364: '吐鲁番', 365: '五家渠', 366: '伊犁'},
    30: {367: '昆明', 368: '怒江', 369: '普洱', 370: '丽江', 371: '保山', 372: '楚雄',
         373: '大理', 374: '德宏', 375: '迪庆', 376: '红河', 377: '临沧', 378: '曲靖',
         379: '文山', 380: '西双版纳', 381: '玉溪', 382: '昭通'},
    31: {383: '杭州', 384: '湖州', 385: '嘉兴', 386: '金华', 387: '丽水', 388: '宁波',
         389: '绍兴', 390: '台州', 391: '温州', 392: '舟山', 393: '衢州'},
    32: {394: '重庆'},
    33: {395: '香港'},
    34: {396: '澳门'},
    35: {984: '台北', 985: '高雄', 986: '基隆', 987: '台中', 988: '台南', 989: '新竹',
         990: '嘉义', 991: '宜兰县', 992: '桃园县', 993: '苗栗县', 994: '彰化县',
         995: '南投县', 996: '云林县', 997: '屏东县', 998: '台东县', 999: '花莲县',
         1000: '澎湖县'}
}


def weather_icon_select(weather):
    """
        # 返回天气图片的文件位置
        @ weather: str 天气
        # return: str 图标路径
    """
    file_path = 'ICON/'
    weather_condition = {
        "晴": "sunny.png",
        "阴": "overcast.png",
        "多云": "cloudy.png",
        "阵雨": "shower.png",
        "小雨": "rain.png",
        "中雨": "rain.png",
        "大雨": "rainstorm.png",
        "暴雨": "rainstorm.png",
        "大暴雨": "rainstorm.png",
        "特大暴雨": "rainstorm.png",
        "雷阵雨": "thundershower.png",
        "雨夹雪": "rainandsnow.png",
        "小雪": "snow.png",
        "中雪": "snow.png",
        "大雪": "snowstorm.png",
        "暴雪": "snowstorm.png",
        "雾": "fog.png",
    }
    selection = weather_condition
    if weather in selection.keys():
        image_file = file_path + selection.get(weather)
    else:
        image_file = file_path + 'na.png'
    return image_file


def chinese_date(num):
    """
        # 将纯数字日期转为带中文字符的日期
        @ num: int 转换的星期数，0~6
        # return: str 日期
    """
    week_selection = {
        "0": "一",
        "1": "二",
        "2": "三",
        "3": "四",
        "4": "五",
        "5": "六",
        "6": "日"
    }
    week = datetime.datetime.now().weekday() + num
    if week > 6:
        week = week - 7
    else:
        week = week
    if num == 1:
        weekday = '明天'
    else:
        weekday = "星期" + week_selection.get(str(week))
    date = time.strftime("%#m{m}%#d{d}", time.localtime(
        time.time() + 3600 * 24 * num)).format(m='月', d='日')
    result = date + weekday
    return result


def calendarDatae():
    """
        # 农历日期
        # return：str 农历日期
    """
    url = 'https://www.sojson.com/open/api/lunar/json.shtml'
    headers = {
        "User-Agent": "User-Agent:Mozilla/5.0 \
         (Windows NT 10.0; Win64; x64) \
         AppleWebKit/537.36 (KHTML, like Gecko) \
         Chrome/63.0.3239.84 Safari/537.36"
    }
    response = requests.get(url=url, headers=headers)
    res = json.loads(response.content.decode(encoding='utf-8'))
    lunar_date = res["data"][0]["cnmonth"] + "月" + res["data"][0]["cnday"]
    return lunar_date


def internet_check():
    """
        # 检测网络
        # return: num 返回 0 或 1
    """
    url = 'https://www.baidu.com'
    try:
        network = requests.get(url, timeout=3)
        # print(network)
        if str(network.status_code) == "200":
            # elif str(network.status_code) == "200":
            return 1
        else:
            return 0
            # print("网络连接正常")
        # print(network)
    except Exception as NetworkERROR:
        return 0
        # print("网络连接失败")


def api_call(last_record):
    """
        # 调用API接口
        @ last_record: str 上次程序成功调用API时保存的地名
        # return: list 包含三个dist类型的列表
    """
    api_key = '6874e0c60fa74b728b9af2fa065cbc0b'
    str_normal_info_path = u'TXT\\str_normal_info.txt'
    str_aqi_info_path = u'TXT\\str_aqi_info.txt'
    str_fut_wea_info_path = u'TXT\\str_future_weather_info.txt'
    str_lunar_info_path = u'TXT\\str_lunar_info.txt'

    weather_site_1 = "https://free-api.heweather.com/s6/weather?" + \
        "location=%s&key=%s" % (last_record, api_key)

    weather_site_2 = "https://free-api.heweather.com/s6/air?" + \
        "location=%s&key=%s" % (last_record, api_key)

    weather_site_3 = "https://www.sojson.com/open/api/weather/" + \
        "json.shtml?city=%s" % (last_record)
    lunar_calendar_site = "https://www.sojson.com/open/api/lunar/json.shtml"

    headers = {
        "User-Agent": "User-Agent:Mozilla/5.0 \
        (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/63.0.3239.84 Safari/537.36"
    }
    # today weather infomation
    weather_1_info = requests.get(weather_site_1, headers=headers)
    weather_normal_info = json.loads(
        weather_1_info.content.decode(encoding='utf-8'))
    str_normal_info = json.dumps(weather_normal_info, ensure_ascii=False)
    with open(str_normal_info_path, 'w', encoding='cp936') as saved_info:
        saved_info.writelines(str_normal_info)
    # air quality infomation
    weather_2_info = requests.get(weather_site_2, headers=headers)
    aqi_info = json.loads(
        weather_2_info.content.decode(encoding='utf-8'))
    str_aqi_info = json.dumps(aqi_info, ensure_ascii=False)
    with open(str_aqi_info_path, 'w', encoding='cp936') as saved_info:
        saved_info.writelines(str_aqi_info)
    # future weather infomation
    weather_3_info = requests.get(weather_site_3, headers=headers)
    future_weather_info = json.loads(
        weather_3_info.content.decode(encoding='utf-8'))
    str_future_weather_info = json.dumps(
        future_weather_info, ensure_ascii=False)
    with open(str_fut_wea_info_path, 'w', encoding='cp936') as saved_info:
        saved_info.writelines(str_future_weather_info)
    # lunar infomation
    lunar_date_info = requests.get(lunar_calendar_site, headers=headers)
    lunar_date_data = json.loads(
        lunar_date_info.content.decode(encoding='utf-8'))
    str_lunar_date_data = json.dumps(
        lunar_date_data, ensure_ascii=False)
    with open(str_lunar_info_path, 'w', encoding='cp936') as saved_info:
        saved_info.writelines(str_lunar_date_data)

    return weather_normal_info, aqi_info, future_weather_info, lunar_date_data


def temp_color(temperature):
    """
        # 不同温度返回不同颜色
        @ temperature: int 温度值
        # return: str 颜色(#123456)
    """
    if temperature < -40:
        color = '#3C13AF'
    elif -40 <= temperature < -30:
        color = '#1A1AB2'
    elif -30 <= temperature < -20:
        color = '#133CAC'
    elif -20 <= temperature < -10:
        color = '#028E9B'
    elif temperature == 0:
        color = '#00A876'
    elif 0 <= temperature < 10:
        color = '#00BC39'
    elif 10 <= temperature < 15:
        color = '#BAF300'
    elif 15 <= temperature < 20:
        color = '#DBF900'
    elif 20 <= temperature < 25:
        color = '#FFD600'
    elif 25 <= temperature < 30:
        color = '#FF6700'
    elif 30 <= temperature < 35:
        color = '#FF3D00'
    else:
        color = '#F60018'

    return color


def ip_location():
    """
        # 获取当前IP的地理位置
        # @ none
        # return: str 中文城市名称（湛江）
    """
    response = requests.get("http://2018.ip138.com/ic.asp")
    soup = BeautifulSoup(response.content.decode("GBK"), 'lxml')
    target_strings = str(soup.center)
    try:
        string = re.findall(r'[\u4e00-\u9fa5]{5,}', target_strings)[0]
        raw_string = re.search('(.*?)(?=市)', string).group()
        sub_string = re.search('(.*?)(?=省)', string).group() + '省'
        location = re.sub(sub_string, '', raw_string)
        return location
    except IndexError as error:
        print("无法获取位置信息")
        return
