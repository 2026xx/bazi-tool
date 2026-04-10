#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
import os
from lunar_python import Lunar, Solar

CITY_LONGITUDE = {
    "安康": 109.0, "安庆": 117.1, "安顺": 105.9, "安阳": 114.4, "鞍山": 123.0, "澳门": 113.5,
    "阿勒泰": 88.1, "阿克苏": 80.3, "阿里": 80.1, "阿拉善盟": 105.7,
    "白城": 122.8, "白山": 126.4, "白银": 104.1, "百色": 106.6, "保定": 115.5, "保山": 99.2,
    "宝鸡": 107.1, "北京": 116.4, "北海": 109.1, "本溪": 123.8, "毕节": 105.3,
    "滨州": 118.0, "亳州": 115.8, "巴中": 106.8, "巴彦淖尔": 107.4, "包头": 110.0,
    "博尔塔拉": 82.1, "巴音郭楞": 86.1,
    "沧州": 116.8, "长春": 125.3, "长沙": 113.0, "长治": 113.1, "常德": 111.7, "常州": 119.9,
    "承德": 117.9, "成都": 104.1, "赤峰": 118.9, "重庆": 106.5, "崇左": 107.4, "池州": 117.5,
    "楚雄": 101.5, "滁州": 118.3, "昌都": 97.2, "朝阳": 120.5,
    "达州": 107.5, "大连": 121.6, "大庆": 125.0, "大同": 113.3, "大理": 100.2, "丹东": 124.4,
    "德宏": 98.6, "德州": 116.3, "德阳": 104.4, "迪庆": 99.7, "定西": 104.6,
    "东莞": 113.7, "东营": 118.7, "大兴安岭": 124.1,
    "鄂尔多斯": 109.8, "鄂州": 114.9, "恩施": 109.5,
    "防城港": 108.4, "佛山": 113.1, "福州": 119.3, "抚顺": 123.9, "抚州": 116.4,
    "阜新": 121.7, "阜阳": 115.8,
    "赣州": 114.9, "高雄": 120.3, "固原": 106.3, "广安": 106.6, "广元": 105.8, "广州": 113.3,
    "贵港": 109.6, "贵阳": 106.7, "桂林": 110.3, "甘南": 102.9, "甘孜": 101.9, "果洛": 100.2,
    "哈密": 93.5, "哈尔滨": 126.5, "海口": 110.3, "海东": 102.4, "海北": 100.9,
    "海南州": 100.6, "海西": 97.4, "邯郸": 114.5, "汉中": 107.0, "杭州": 120.2,
    "合肥": 117.3, "河池": 108.1, "河源": 114.7, "贺州": 111.6, "黑河": 127.5,
    "衡水": 115.7, "衡阳": 112.6, "红河": 103.4, "葫芦岛": 120.8,
    "呼和浩特": 111.7, "呼伦贝尔": 119.7, "湖州": 120.1, "怀化": 110.0,
    "黄冈": 114.9, "黄南": 102.0, "黄山": 118.3, "黄石": 115.0, "惠州": 114.4,
    "和田": 79.9, "香港": 114.2,
    "吉安": 114.9, "吉林": 126.6, "济南": 117.0, "济宁": 116.6, "嘉兴": 120.8,
    "嘉峪关": 98.3, "江门": 113.1, "焦作": 113.2, "金昌": 102.2, "金华": 119.6,
    "锦州": 121.1, "晋城": 112.8, "晋中": 112.7, "荆门": 112.2, "荆州": 112.2,
    "景德镇": 117.2, "九江": 116.0, "酒泉": 98.5, "基隆": 121.7,
    "喀什": 75.9, "开封": 114.3, "克拉玛依": 84.9, "昆明": 102.7, "克孜勒苏": 76.2,
    "来宾": 109.2, "兰州": 103.8, "廊坊": 116.7, "乐山": 103.8, "丽江": 100.2, "丽水": 119.9,
    "连云港": 119.2, "凉山": 102.3, "辽阳": 123.2, "辽源": 125.1, "临沧": 100.1,
    "临汾": 111.5, "临沂": 118.4, "临夏": 103.2, "柳州": 109.4, "六安": 116.5,
    "六盘水": 104.8, "龙岩": 117.0, "娄底": 112.0, "泸州": 105.4, "吕梁": 111.1,
    "林芝": 94.4, "拉萨": 91.1,
    "马鞍山": 118.5, "茂名": 110.9, "梅州": 116.1, "绵阳": 104.7, "牡丹江": 129.6, "莆田": 119.0,
    "南昌": 115.9, "南充": 106.1, "南京": 118.8, "南宁": 108.4, "南平": 118.2,
    "南通": 120.9, "南阳": 112.5, "那曲": 92.1, "宁波": 121.6, "宁德": 119.5, "怒江": 98.9,
    "盘锦": 122.1, "萍乡": 113.9, "普洱": 100.9, "濮阳": 115.0, "平凉": 106.7,
    "平顶山": 113.3, "屏东": 120.5,
    "钦州": 108.6, "秦皇岛": 119.6, "青岛": 120.4, "庆阳": 107.6, "曲靖": 103.8,
    "衢州": 118.9, "泉州": 118.7, "黔东南": 107.9, "黔南": 107.5, "黔西南": 104.9,
    "日喀则": 88.9, "日照": 119.5,
    "三亚": 109.5, "三明": 117.6, "三门峡": 111.2, "商洛": 109.9, "商丘": 115.7,
    "上海": 121.5, "上饶": 117.9, "绍兴": 120.6, "韶关": 113.6, "深圳": 114.1,
    "沈阳": 123.4, "石家庄": 114.5, "石嘴山": 106.4, "朔州": 112.4, "松原": 124.8,
    "遂宁": 105.6, "宿迁": 118.3, "宿州": 116.9, "随州": 113.4, "绥化": 126.9, "山南": 91.8,
    "台北": 121.5, "台中": 120.7, "台南": 120.2, "台州": 121.4, "台东": 121.1,
    "太原": 112.5, "泰安": 117.1, "泰州": 119.9, "唐山": 118.2, "天津": 117.2,
    "天水": 105.7, "铁岭": 123.8, "通辽": 122.3, "通化": 125.9, "铜川": 109.1,
    "铜仁": 109.2, "铜陵": 117.8, "吐鲁番": 89.2, "塔城": 82.9,
    "温州": 120.7, "梧州": 111.3, "武汉": 114.3, "武威": 102.6, "吴忠": 106.2,
    "乌鲁木齐": 87.6, "乌海": 106.8, "乌兰察布": 113.1,
    "西安": 108.9, "西宁": 101.8, "西双版纳": 100.8, "厦门": 118.1, "湘潭": 112.9,
    "湘西": 109.7, "忻州": 112.7, "信阳": 114.1, "兴安盟": 122.1, "邢台": 114.5,
    "徐州": 117.2, "许昌": 113.8, "宣城": 118.8, "锡林郭勒盟": 116.1, "新竹": 121.0, "新余": 114.9,
    "烟台": 121.4, "延安": 109.5, "延边": 129.5, "盐城": 120.2, "扬州": 119.4,
    "阳江": 111.9, "阳泉": 113.6, "鹰潭": 117.1, "营口": 122.2, "玉林": 110.2,
    "玉溪": 102.5, "玉树": 97.0, "运城": 111.0, "伊犁": 81.3, "宜春": 114.4,
    "宜宾": 104.6, "宜昌": 111.3, "益阳": 112.4, "岳阳": 113.1, "嘉义": 120.4,
    "枣庄": 117.6, "张家界": 110.5, "张家口": 114.9, "张掖": 100.4, "漳州": 117.6,
    "肇庆": 112.5, "镇江": 119.4, "郑州": 113.6, "中卫": 105.2, "中山": 113.4,
    "舟山": 122.1, "珠海": 113.6, "株洲": 113.1, "遵义": 106.9, "资阳": 104.6,
    "自贡": 104.8, "昭通": 103.7,
}

class BaziHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bazi_tool.html')
            with open(html_path, 'rb') as f:
                self.wfile.write(f.read())
        elif self.path == '/cities':
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            cities = sorted(CITY_LONGITUDE.keys())
            self.wfile.write(json.dumps(cities, ensure_ascii=False).encode('utf-8'))
        elif self.path.startswith('/calc'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            try:
                name = params.get('name', [''])[0]
                year = int(params.get('year', [0])[0])
                month = int(params.get('month', [0])[0])
                day = int(params.get('day', [0])[0])
                hour = int(params.get('hour', [0])[0])
                minute = int(params.get('minute', [0])[0])
                city = params.get('city', ['上海'])[0]
                gender = params.get('gender', ['女'])[0]

                lng = CITY_LONGITUDE.get(city, 120.0)
                offset_minutes = (lng - 120) * 4
                total_minutes = hour * 60 + minute + offset_minutes
                real_hour = int(total_minutes // 60)
                real_minute = int(total_minutes % 60)
                if real_hour < 0:
                    real_hour += 24
                elif real_hour >= 24:
                    real_hour -= 24

                # 子时换日：真太阳时23:00后，日柱归次日
                calc_day = day
                calc_month = month
                calc_year = year
                if real_hour >= 23:
                    # 次日
                    import datetime
                    next_day = datetime.date(year, month, day) + datetime.timedelta(days=1)
                    calc_year = next_day.year
                    calc_month = next_day.month
                    calc_day = next_day.day

                solar = Solar.fromYmdHms(calc_year, calc_month, calc_day, real_hour, real_minute, 0)
                lunar = solar.getLunar()
                bazi = lunar.getEightChar()

                # 性别：0=女，1=男
                gender_int = 1 if gender == '男' else 0

                # 大运
                yun = bazi.getYun(gender_int, solar.getYear())
                da_yun_list = []
                for dy in yun.getDaYun()[:10]:
                    da_yun_list.append({
                        "gz": dy.getGanZhi(),
                        "start_age": dy.getStartAge(),
                        "end_age": dy.getEndAge(),
                        "start_year": dy.getStartYear()
                    })

                # 五行统计（手动计算）
                wx_map = {
                    '甲':'木','乙':'木','丙':'火','丁':'火','戊':'土',
                    '己':'土','庚':'金','辛':'金','壬':'水','癸':'水',
                    '子':'水','丑':'土','寅':'木','卯':'木','辰':'土',
                    '巳':'火','午':'火','未':'土','申':'金','酉':'金',
                    '戌':'土','亥':'水'
                }
                wx = {'木':0,'火':0,'土':0,'金':0,'水':0}
                for gz in [bazi.getYear(), bazi.getMonth(), bazi.getDay(), bazi.getTime()]:
                    for char in gz:
                        if char in wx_map:
                            wx[wx_map[char]] += 1

                result = {
                    "name": name,
                    "gender": gender,
                    "solar": f"{year}年{month}月{day}日 {hour:02d}:{minute:02d}",
                    "real_time": f"{real_hour:02d}:{real_minute:02d}（真太阳时）",
                    "offset": f"{offset_minutes:+.1f}分钟",
                    "city": city,
                    "longitude": lng,
                    "lunar_date": f"{lunar.getYearInChinese()}年{lunar.getMonthInChinese()}月{lunar.getDayInChinese()}",
                    "shichen": get_shichen(real_hour),
                    # 四柱天干地支
                    "year_gz": bazi.getYear(),
                    "month_gz": bazi.getMonth(),
                    "day_gz": bazi.getDay(),
                    "hour_gz": bazi.getTime(),
                    "year_gan": bazi.getYear()[0],
                    "year_zhi": bazi.getYear()[1],
                    "month_gan": bazi.getMonth()[0],
                    "month_zhi": bazi.getMonth()[1],
                    "day_gan": bazi.getDay()[0],
                    "day_zhi": bazi.getDay()[1],
                    "hour_gan": bazi.getTime()[0],
                    "hour_zhi": bazi.getTime()[1],
                    # 十神
                    "year_gan_ss": bazi.getYearShiShenGan(),
                    "month_gan_ss": bazi.getMonthShiShenGan(),
                    "hour_gan_ss": bazi.getTimeShiShenGan(),
                    "year_zhi_ss": bazi.getYearShiShenZhi(),
                    "month_zhi_ss": bazi.getMonthShiShenZhi(),
                    "day_zhi_ss": bazi.getDayShiShenZhi(),
                    "hour_zhi_ss": bazi.getTimeShiShenZhi(),
                    # 藏干
                    "year_hide": bazi.getYearHideGan(),
                    "month_hide": bazi.getMonthHideGan(),
                    "day_hide": bazi.getDayHideGan(),
                    "hour_hide": bazi.getTimeHideGan(),
                    # 五行
                    "wuxing": wx,
                    # 大运
                    "yun_start_year": yun.getStartYear(),
                    "da_yun": da_yun_list,
                }
                self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.wfile.write(json.dumps({"error": str(e)}, ensure_ascii=False).encode('utf-8'))

    def log_message(self, format, *args):
        pass

def get_shichen(hour):
    shichen = ["子", "丑", "丑", "寅", "寅", "卯", "卯", "辰", "辰", "巳", "巳", "午",
               "午", "未", "未", "申", "申", "酉", "酉", "戌", "戌", "亥", "亥", "子"]
    return shichen[hour] + "时"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8888))
    server = HTTPServer(('0.0.0.0', port), BaziHandler)
    print(f"八字排盘工具已启动，端口：{port}")
    server.serve_forever()
