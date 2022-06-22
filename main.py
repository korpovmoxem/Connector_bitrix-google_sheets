import gspread
from fast_bitrix24 import Bitrix

# google sheets
sa = gspread.service_account(filename='bitrix24-354011-591a0295d8a1.json')  # json-file with access (get from google console)
sh = sa.open('новый отчет по лидам')    # open sheet (need to give access to service account)

wks = sh.worksheet("сд2")   # open list

cells = ''  # need to know range of cells for data list
data_l = []  # data list for writing sheet
temp_l = []  # temp data list

# Вебхук
webhook = 'https://m-union.bitrix24.ru/rest/8871/ke51119izesxw5md/'
b = Bitrix(webhook)


# Получение списка сделок по фильтру
deals = b.get_all(
    'crm.deal.list',
    params={
        'select': ['*', 'UF_*'],
        'filter': {'CLOSED': 'N'}
    })
count = 0
s = ''
temp = []
status_document = {'1396': 'ЭК', '1398': 'НЭ'}

# Создание и присваивание переменных со статистикой
for deal in deals:
    if deal['STAGE_ID'] == '5' and deal['UF_CRM_628B602C0A665'] == '11791':
        name_deal = deal['TITLE']
        ID = deal['ID']
        assigned_by_id = str(deal['ASSIGNED_BY_ID'])
        user_info = b.get_all('user.get', {"ID": assigned_by_id})
        user_name = user_info[0]['NAME'] + ' ' + user_info[0]['LAST_NAME']
        adress = deal['UF_CRM_1622808160']
        start_data = deal['UF_CRM_1619530812769'][:10].replace('-', '/')
        status = deal['UF_CRM_1545905425']
        calls = deal['UF_CRM_1606124287613']
        views = deal['UF_CRM_1580298528382']
        messages = deal['UF_CRM_1650365519']
        shows = deal['UF_CRM_1626866562']
        days_in_work = deal['UF_CRM_1580301828898']
        liquidity = deal['UF_CRM_1580302812']
        demand = deal['UF_CRM_1580302958']
        liquidity_zone = deal['UF_CRM_1580307210666']
        demand_zone = deal['UF_CRM_1580307153235']
        data_dict = {'ID': ID, 'Статус договора': status_document[status], 'Название сделки': name_deal,
                     'Адрес объекта для рассылок': adress, 'Дата начала непрерывного рекламирования': start_data,
                     'Количество дней в рекламе': days_in_work, 'Ответственный': user_name, 'Просмотры': views,
                     'Звонки': calls, 'Показы': shows, 'Ликвидность': liquidity,
                     'Зона ликвидности': liquidity_zone, 'Спрос': demand, 'Зона спроса': demand_zone}
        for i in data_dict.values():
            if i != None:
                temp_l.append(i)
            else:
                temp_l.append('0')
        data_l.append(temp_l)
        temp_l = []

        # count results
        for i in data_dict:
            if data_dict[i] == None:
                data_dict[i] = 0
        temp.append(int(ID.strip()))
        count += 1

# update cell in google sheet
count += 1
cells = 'A2:O' + str(count)
print(cells)
wks.update(cells, data_l)

# create string with ID's for Bitrix24
for i in temp:
    s += str(i) + ','

with open('Deals.txt', 'w') as file:
    file.write(s)
    file.write('\n')
    file.write(f'Сделок М-Юнион в рекламе посчитано: {count}')
