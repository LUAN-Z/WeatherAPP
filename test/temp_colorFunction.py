def temp_color(temp: int):
    # print("temp %d" % temp)
    '''
    {-40: '#3C13AF', -30: '#1A1AB2', -20: '#133CAC', -10: '#028E9B',
     0: '#00A876', 10: '#00BC39', 15: '#BAF300', 20: '#DBF900',
     25: '#FFD600', 30: '#FF6700', 35: '#FF3D00', 40: '#F60018'}
    '''
    tempList = []
    colorDict = {'#3C13AF': -40, '#1A1AB2': -30, '#133CAC': -20,
                 '#028E9B': -10, '#00A876': 0, '#00BC39': 10,
                 '#BAF300': 15, '#DBF900': 20, '#FFD600': 25,
                 '#FF6700': 30, '#FF3D00': 35, '#F60018': 40}
    for i in colorDict:
        # print(colorDict[i])
        if temp <= colorDict[i]:
            tempList.append(colorDict[i])
    if tempList:
        for index in colorDict.keys():
            if colorDict[index] == tempList[0]:
                return index
    else:
        # None of value of colorDict can bigger than given value
        return '#F60018'


'''
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
'''


if __name__ == '__main__':
    for i in range(50, -50, -5):
        res = temp_color(i)
        print(i, res)
