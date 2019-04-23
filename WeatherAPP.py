import json
import re
import time
from tkinter import *
from tkinter import ttk

import PIL
import PIL.Image
from PIL import ImageTk

import infomation
from infomation import ip_location

provinceDict = infomation.provinceDict
cityDict = infomation.cityDict
record_file_path = u'TXT\\last_record_city.txt'

# TODO
'''
未完成：
    语音播报
    7日天气预报
    图库
 完成：
    增加数据库存放本次调用成功的数据, 为下次程序在无网格情况下无法调用API时使用
    增加根据本地IP地址获取本地地理位置，在打开程序时自动获取当地天气信息
    完善程序在有网情况下打开后突然断网后再调用API报错的问题
    修复最高温度为零下时由于多出负号遮盖分隔符的bug
    修复点击关闭按钮程序还在后台执行的bug
'''


class WeatherAPP:

    def __init__(self):
        self.window = Tk()
        self.window.title('看,天气')
        self.window.resizable(width=False, height=False)
        self.window.geometry('300x630')
        self.topCanvas = Canvas(self.window, bg='white')
        self.topCanvas.place(x=0, y=0, width=300, height=40)
        self.Icon = Canvas(self.window, bg='white')
        self.Icon.place(x=0, y=430, width=300, height=200)
        self.city_combo = ttk.Combobox(
            self.window, height=10, width=13, font=('汉仪楷体S', 12))
        self.province_combo = ttk.Combobox(
            self.window, height=10, width=13, font=('汉仪楷体S', 12))
        # 读取上次储存的城市名
        if infomation.internet_check() and ip_location() is not None:
            self.last_record = ip_location()
        else:
            with open(record_file_path, 'r', encoding='cp936') as content:
                self.last_record = content.read()
        self.city_combo.set(self.last_record)
        for index in cityDict.keys():
            if self.last_record in cityDict[index].values():
                self.province_combo.set(provinceDict[index])
                self.city_combo['values'] = tuple(cityDict[index].values())
        # fixed icons
        self.cityIcon = ImageTk.PhotoImage(PIL.Image.open("ICON/city32.png"))
        self.weatherIcon = ImageTk.PhotoImage(
            PIL.Image.open('ICON/weather.png'))
        self.windIcon = ImageTk.PhotoImage(PIL.Image.open('ICON/wind32.png'))
        self.humilityIcon = ImageTk.PhotoImage(
            PIL.Image.open('ICON/humility32.png'))
        self.rainIcon = ImageTk.PhotoImage(PIL.Image.open('ICON/may_rain.png'))
        self.noRainIcon = ImageTk.PhotoImage(PIL.Image.open(
            'ICON/no_rain.png'))
        self.aqiIcon = ImageTk.PhotoImage(PIL.Image.open('ICON/AQI.png'))
        self.airPressureIcon = ImageTk.PhotoImage(
            PIL.Image.open('ICON/airpressure32.png'))
        self.temperatureIcon = ImageTk.PhotoImage(
            PIL.Image.open('ICON/circle.png'))
        self.networkAvailableIcon = ImageTk.PhotoImage(
            PIL.Image.open('ICON/available.png'))
        self.networkUnavailableIcon = ImageTk.PhotoImage(
            PIL.Image.open('ICON/unavailable.png'))

        self.province_select()
        self.info_display()
        self.window.mainloop()

    def selected_city_confirm(self):
        if infomation.internet_check():
            self.last_record = self.city
        # 存储本次调用的城市名,供下次初始化使用
            with open(record_file_path, 'w') as record:
                record.write(self.city)
        else:
            # print("网络不可用")
            pass
        self.info_display()

    def province_select(self):
        self.confirm_button = Button(
            self.window, text='确定', width=5, height=1, bg='white',
            font=('汉仪楷体S', 9), command=self.selected_city_confirm)
        self.confirm_button.grid(row=0, column=2)
        self.confirm_button.config(state='disabled')
        # self.province_combo.set('选择省份')
        self.province_combo.config(state='readonly')
        self.city_combo.config(state='readonly')
        # self.city_combo.set('选择城市')
        self.province_combo['values'] = tuple(provinceDict.values())
        # print(tuple(provinceDict.keys()))
        self.province_combo.grid(row=0, column=0)
        self.city_combo.grid(row=0, column=1)
        self.province_combo.bind(
            "<<ComboboxSelected>>", self.button_status_judge)
        self.city_combo.bind("<<ComboboxSelected>>", self.city_select)

    def button_status_judge(self, event):
        self.city_combo.set('选择城市')
        self.var_Selected = self.province_combo.current()
        self.var2_Selected = self.city_combo.current()
        if self.var2_Selected == -1:
            self.confirm_button.config(state='disabled')
        else:
            self.confirm_button.config(state='active')
        index = self.var_Selected + 2
        self.city_combo['values'] = tuple(cityDict[index].values())

    def city_select(self, event):
        self.var_Selected = self.province_combo.current()
        index = self.var_Selected + 2
        self.var2_Selected = self.city_combo.current()
        if self.var2_Selected == -1:
            self.confirm_button.config(state='disabled')
        else:
            self.confirm_button.config(state='active')
        self.city_combo['values'] = tuple(cityDict[index].values())
        place = tuple(cityDict[index].values())
        # print(place, type(place))
        self.city = place[self.var2_Selected]
        # print(self.city, type(self.city))

    def info_display(self):
        str_normal_info_path = u'TXT\\str_normal_info.txt'
        str_aqi_info_path = u'TXT\\str_aqi_info.txt'
        str_future_weather_info_path = u'TXT\\str_future_weather_info.txt'
        str_lunar_info_path = u'TXT\\str_lunar_info.txt'

        if infomation.internet_check():
            network_icon = self.networkAvailableIcon
            print('网络通畅,调用API')
            # 调用API
            print(self.last_record)
            combination_info = infomation.api_call(self.last_record)
            weather_normal_info = combination_info[0]
            aqi_info = combination_info[1]
            future_weather_info = combination_info[2]
            lunar_date_data = combination_info[3]
        else:
            # 网络不可用,调用本地数据
            print("网络不可用,调用本地数据")
            network_icon = self.networkUnavailableIcon  # 网络不可用图标

            with open(str_normal_info_path, 'r', encoding='cp936') as content:
                weather_normal_info = json.loads(content.read())

            with open(str_aqi_info_path, 'r', encoding='cp936') as content:
                aqi_info = json.loads(content.read())

            with open(str_future_weather_info_path, 'r',
                      encoding='cp936') as content:
                future_weather_info = json.loads(content.read())

            with open(str_lunar_info_path, 'r', encoding='cp936') as content:
                lunar_date_data = json.loads(content.read())

        self.backgroundCanvas = Canvas(self.window, bg='white')
        self.backgroundCanvas.place(x=0, y=30, width=300, height=400)

        # 城市
        self.cityName = weather_normal_info[
            "HeWeather6"][0]["basic"]["location"]
        # self.backgroundCanvas.create_image(
        #     20, 40, anchor='nw', image=self.cityIcon)
        if len(self.cityName) == 4:
            x_pos = 10
        elif len(self.cityName) == 3:
            x_pos = 20
        elif len(self.cityName) == 2:
            x_pos = 30
        Label(self.window, bg='white', text=self.cityName, fg='DarkRed',
              font=("微软雅黑", 14, "bold")).place(x=x_pos, y=90)

        # 天气
        self.weather = weather_normal_info[
            "HeWeather6"][0]["now"]["cond_txt"]
        # self.backgroundCanvas.create_image(
        #     220, 60, anchor='nw', image=self.weatherIcon)
        Label(self.window, bg='white', text=self.weather, fg='DeepSkyBlue',
              font=("Source Code Pro", 16, "bold")).place(x=230, y=90)
        weather_today_image = infomation.weather_icon_select(self.weather)
        self.weatherImage = ImageTk.PhotoImage(
            PIL.Image.open(weather_today_image))
        self.backgroundCanvas.create_image(
            100, 30, anchor='nw', image=self.weatherImage)

        # 湿度
        self.humility = weather_normal_info[
            "HeWeather6"][0]["now"]["hum"] + '%'
        self.backgroundCanvas.create_image(
            190, 260, anchor='nw', image=self.humilityIcon)
        Label(self.window, bg='white', text=self.humility, fg='CornflowerBlue',
              font=("微软雅黑", 16, "bold")).place(x=225, y=290)

        # 降雨
        self.rain_probability = weather_normal_info[
            "HeWeather6"][0]["daily_forecast"][0]["pop"]
        if self.rain_probability is '0':
            self.rain_probability = ''
            rain_label_x = 240
            self.rain_probability_icon = self.noRainIcon
        else:
            self.rain_probability = self.rain_probability + '%'
            rain_label_x = 230
            self.rain_probability_icon = self.rainIcon
        self.backgroundCanvas.create_image(
            240, 170, anchor='nw', image=self.rain_probability_icon)
        Label(self.window, text=self.rain_probability, fg='SlateGrey',
              bg='white', font=("微软雅黑", 16, "bold")).place(
            x=rain_label_x, y=240)

        # 空气质量指数
        self.pm10 = aqi_info["HeWeather6"][0]["air_now_city"]["pm10"]
        self.so2 = aqi_info["HeWeather6"][0]["air_now_city"]["so2"]
        self.o3 = aqi_info["HeWeather6"][0]["air_now_city"]["o3"]
        self.co = aqi_info["HeWeather6"][0]["air_now_city"]["co"]
        self.no2 = aqi_info["HeWeather6"][0]["air_now_city"]["no2"]
        self.pm2_5 = aqi_info["HeWeather6"][0]["air_now_city"]["pm25"]
        self.backgroundCanvas.create_image(
            3, 160 + 20, anchor='nw', image=self.aqiIcon)
        Label(self.window, bg='white', text=self.pm10, fg='Plum',
              font=("微软雅黑", 9, "bold")).place(x=42, y=210)
        Label(self.window, bg='white', text=self.so2, fg='Violet',
              font=("微软雅黑", 9, "bold")).place(x=37, y=228)
        Label(self.window, bg='white', text=self.o3, fg='Orchid',
              font=("微软雅黑", 9, "bold")).place(x=34, y=246)
        Label(self.window, bg='white', text=self.co, fg='MediumOrchid',
              font=("微软雅黑", 9, "bold")).place(x=34, y=264)
        Label(self.window, bg='white', text=self.no2, fg='DarkOrchid',
              font=("微软雅黑", 9, "bold")).place(x=37, y=282)
        Label(self.window, bg='white', text=self.pm2_5, fg='DarkViolet',
              font=("微软雅黑", 9, "bold")).place(x=45, y=299)

        # 气压
        self.airPressure = weather_normal_info["HeWeather6"][
            0]["daily_forecast"][0]["pres"] + 'mb'
        self.backgroundCanvas.create_image(
            2, 305, anchor='nw', image=self.airPressureIcon)
        Label(self.window, bg='white', text=self.airPressure,
              fg='DarkGreen',
              font=("Source Code Pro", 13, "bold")).place(x=35, y=337)

        # 风况
        self.wind = weather_normal_info["HeWeather6"][0]["now"]["wind_dir"] + \
            weather_normal_info["HeWeather6"][0]["now"][
            "wind_sc"] + '级'
        self.backgroundCanvas.create_image(
            175, 305, anchor='nw', image=self.windIcon)
        Label(self.window, bg='white', text=self.wind, fg='RoyalBlue',
              font=("Source Code Pro", 12, "bold")).place(x=210, y=337)

        # 温度
        self.minTemp = weather_normal_info["HeWeather6"][
            0]["daily_forecast"][0]["tmp_min"]
        tempMinColor = infomation.temp_color(int(self.minTemp))
        self.maxTemp = weather_normal_info["HeWeather6"][
            0]["daily_forecast"][0]["tmp_max"]
        tempMaxColor = infomation.temp_color(int(self.maxTemp))
        self.curTemp = weather_normal_info["HeWeather6"][0]["now"]["tmp"]
        temp_now_color = infomation.temp_color(int(self.curTemp))

        # 最低温度
        minTempLength = len(self.minTemp)
        minTempNum = re.search(r'[\d]{1,2}', self.minTemp).group()

        if minTempLength == 3:
            minTempX = 102
            Label(self.window, bg='white', text='℃', fg=tempMinColor,
                  font=("Arial Rounded MT Bold", 8, "bold")).place(x=130,
                                                                   y=220)
            Label(self.window, bg='white', text='-', fg=tempMinColor,
                  font=("Arial Rounded MT Bold", 10, "bold")).place(x=93,
                                                                    y=230)
        elif minTempLength == 2:
            Label(self.window, bg='white', text='℃', fg=tempMinColor,
                  font=("Arial Rounded MT Bold", 8, "bold")).place(x=130,
                                                                   y=220)
            if re.search(r'([-])?', self.minTemp).group() is '-':
                minTempX = 113
                Label(self.window, bg='white', text='-', fg=tempMinColor,
                      font=("Arial Rounded MT Bold", 10, "bold")).place(x=100,
                                                                        y=230)
            else:
                minTempX = 100

        elif minTempLength == 1:
            minTempX = 112
            Label(self.window, bg='white', text='℃', fg=tempMinColor,
                  font=("Arial Rounded MT Bold", 8, "bold")).place(x=130,
                                                                   y=220)

        Label(self.window, bg='white', text=minTempNum, fg=tempMinColor,
              font=("Arial Rounded MT Bold", 18, "bold")).place(x=minTempX,
                                                                y=220)

        # 温度分割线
        self.backgroundCanvas.create_line(
            150, 192, 150, 217, width=3, fill='DimGrey')

        # 最高温度
        maxTempLength = len(self.maxTemp)
        maxTempNum = re.search(r'[\d]{1,2}', self.maxTemp).group()
        if maxTempLength == 3:
            maxTempX = 160
            Label(self.window, bg='white', text='℃', fg=tempMaxColor,
                  font=("Arial Rounded MT Bold", 8, "bold")).place(x=188,
                                                                   y=220)
            Label(self.window, bg='white', text='-', fg=tempMaxColor,
                  font=("Arial Rounded MT Bold", 10, "bold")).place(x=152,
                                                                    y=230)
        elif maxTempLength == 2:
            if re.search(r'([-])?', self.minTemp).group() is '-':
                maxTempX = 160
                Label(self.window, bg='white', text='-', fg=tempMaxColor,
                      font=("Arial Rounded MT Bold", 10, "bold")).place(x=152,
                                                                        y=230)
                Label(self.window, bg='white', text='℃', fg=tempMaxColor,
                      font=("Arial Rounded MT Bold", 8, "bold")).place(x=180,
                                                                       y=220)
            else:
                maxTempX = 157
                Label(self.window, bg='white', text='℃', fg=tempMaxColor,
                      font=("Arial Rounded MT Bold", 8, "bold")).place(x=188,
                                                                       y=220)

        elif maxTempLength == 1:
            maxTempX = 160
            Label(self.window, bg='white', text='℃', fg=tempMaxColor,
                  font=("Arial Rounded MT Bold", 8, "bold")).place(x=180,
                                                                   y=220)

        Label(self.window, bg='white', text=maxTempNum, fg=tempMaxColor,
              font=("Arial Rounded MT Bold", 18, "bold")).place(x=maxTempX,
                                                                y=220)
        # 体感温度
        nowTempLength = len(self.curTemp)
        if re.search(r'([-])?', self.curTemp).group() is '-':
            if nowTempLength == 3:  # -25
                label_x = 100
                degLabelX = 175
            elif nowTempLength == 2:  # 15
                label_x = 113
                degLabelX = 160
        else:
            if nowTempLength == 1:  # 5
                label_x = 135
                degLabelX = 160
            else:  # 25
                label_x = 120
                degLabelX = 170
        Label(self.window, bg='white', text=self.curTemp, fg=temp_now_color,
              font=("Arial Rounded MT Bold", 34, "bold")).place(x=label_x,
                                                                y=255)
        Label(self.window, bg='white', text='℃', fg='HotPink',
              font=("Arial Rounded MT Bold", 18, 'bold')).place(x=degLabelX,
                                                                y=260)

        self.backgroundCanvas.create_image(
            75, 155, anchor='nw', image=self.temperatureIcon)

        # lifestyle
        self.dress_suggestion = weather_normal_info[
            "HeWeather6"][0]["lifestyle"][1]["txt"]
        Label(self.window, bg='white', text=self.dress_suggestion,
              fg='DimGrey', wraplength=300, justify='left',
              font=('黑体', 10)).place(x=3, y=380)

        # 未来三天天气
        self.Icon.create_line(0, 2, 300, 2, fill='Maroon', width=2)
        self.Icon.create_line(0, 27, 300, 27, fill='LightSkyBlue', width=2)
        self.Icon.create_line(0, 133, 300, 133, fill='Navy', width=2)
        self.Icon.create_line(0, 165, 300, 165, fill='SaddleBrown', width=2)
        self.Icon.create_line(3, 0, 3, 165, fill='Turquoise', width=2)
        self.Icon.create_line(100, 0, 100, 165, fill='ForestGreen', width=2)
        self.Icon.create_line(200, 0, 200, 165, fill='Violet', width=2)
        self.Icon.create_line(297, 0, 297, 165, fill='OrangeRed', width=2)
        self.date_Tomorrow = infomation.chinese_date(1)
        self.weather_Tomorrow = future_weather_info[
            "data"]["forecast"][1]["type"]
        self.weatherTomorrowImage = infomation.weather_icon_select(
            self.weather_Tomorrow)
        self.temp_min_Tomorrow = re.search(r'([-])?(\d+)',
                                           future_weather_info["data"][
                                               "forecast"][1]["low"]).group()
        self.temp_max_Tomorrow = re.search(r'(-)?(\d+)',
                                           future_weather_info["data"][
                                               "forecast"][1]["high"]).group()
        self.temp_tomorrow = self.temp_min_Tomorrow + '/' + \
            self.temp_max_Tomorrow + '℃'

        self.date_TwoDatOfNow = infomation.chinese_date(2)
        self.weather_TwoDayOfNow = future_weather_info[
            "data"]["forecast"][2]["type"]
        self.weatherTwoDayOfNowImage = infomation.weather_icon_select(
            self.weather_TwoDayOfNow)
        self.temp_min_TwoDayOfNow = re.search(r"(-)?(\d+)",
                                              future_weather_info["data"][
                                                  "forecast"][2][
                                                  "low"]).group()
        self.temp_max_TwoDayOfNow = re.search(r'(-)?(\d+)',
                                              future_weather_info["data"][
                                                  "forecast"][2][
                                                  "high"]).group()
        self.temp_twodays = self.temp_min_TwoDayOfNow + \
            '/' + self.temp_max_TwoDayOfNow + '℃'

        self.date_ThreeDayOfNow = infomation.chinese_date(3)
        self.weather_ThreeDayOfNow = future_weather_info[
            "data"]["forecast"][3]["type"]
        self.weatherThreeDayOfNowImage = infomation.weather_icon_select(
            self.weather_ThreeDayOfNow)
        self.temp_min_ThreeDayOfNow = re.search(r'(-)?(\d+)',
                                                future_weather_info["data"][
                                                    "forecast"][3][
                                                    "low"]).group()
        self.temp_max_ThreeDayOfNow = re.search(r'(-)?(\d+)',
                                                future_weather_info["data"][
                                                    "forecast"][3][
                                                    "high"]).group()
        self.temp_threedays = self.temp_min_ThreeDayOfNow + \
            '/' + self.temp_max_ThreeDayOfNow + '℃'

        Label(self.window, bg='white', text=self.date_Tomorrow,
              fg='SteelBlue',
              font=("微软雅黑", 9, "bold")).place(x=9, y=433)
        self.Icon_1_Image = ImageTk.PhotoImage(
            PIL.Image.open(self.weatherTomorrowImage))
        self.Icon.create_image(0, 30, anchor='nw', image=self.Icon_1_Image)
        Label(self.window, bg='white', text=self.temp_tomorrow,
              fg='Maroon',
              font=("微软雅黑", 12, "bold")).place(x=15, y=565)

        Label(self.window, bg='white', text=self.date_TwoDatOfNow,
              fg='#00B36A',
              font=("微软雅黑", 9, "bold")).place(x=103, y=433)
        self.Icon_2_Image = ImageTk.PhotoImage(
            PIL.Image.open(self.weatherTwoDayOfNowImage))
        self.Icon.create_image(100, 30, anchor='nw',
                               image=self.Icon_2_Image)
        Label(self.window, bg='white', text=self.temp_twodays,
              fg='Maroon',
              font=("微软雅黑", 12, "bold")).place(x=115, y=565)

        Label(self.window, bg='white', text=self.date_ThreeDayOfNow,
              fg='OrangeRed',
              font=("微软雅黑", 9, "bold")).place(x=203, y=433)
        self.Icon_3_Image = ImageTk.PhotoImage(
            PIL.Image.open(self.weatherThreeDayOfNowImage))
        self.Icon.create_image(200, 30, anchor='nw',
                               image=self.Icon_3_Image)
        Label(self.window, bg='white', text=self.temp_threedays,
              fg='Maroon',
              font=("微软雅黑", 12, "bold")).place(x=215, y=565)

        # 农历和国历
        solar_date = time.strftime("%#m{m}%#d{d}", time.localtime(
            time.time())).format(m='月', d='日')
        lunarDate = lunar_date_data["data"]["cnmonth"] + "月" + lunar_date_data[
            "data"]["cnday"]
        Label(self.window, bg='white', fg='blue',
              text=solar_date + ' 农历' + lunarDate,
              font=("汉仪楷体S", 13)).place(x=50, y=602)

        # 更新时间
        self.refresh_time = weather_normal_info[
            "HeWeather6"][0]["update"]["loc"][11:]
        Label(self.window, bg='white', text='更新时间:', fg='blue',
              font=("汉仪楷体S", 8)).place(x=195, y=413)
        Label(self.window, bg='white', text=self.refresh_time, fg='blue',
              font=("汉仪楷体S", 9)).place(x=250, y=412)

        # 网络状况
        self.Icon.create_image(265, 167, anchor='nw', image=network_icon)


if __name__ == '__main__':
    try:
        WeatherAPP()
        # time.sleep(1800)
    except KeyboardInterrupt:
        exit(0)
    finally:
        pass
    # while 1:
    #     WeatherAPP()
    #     time.sleep(1800)
