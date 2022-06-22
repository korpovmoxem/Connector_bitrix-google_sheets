import gspread
from fast_bitrix24 import Bitrix

# google sheets
sa = gspread.service_account(filename='bitrix24-354011-591a0295d8a1.json')  # json-file with access (get from google console)
sh = sa.open('Connector_bitrix')    # open sheet (need to give access to service account)

wks = sh.worksheet("deals")   # open list

wks.clear()  # clear worksheet

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

print(len(deals[0]))

# update cell in google sheet
count += 1
cells = 'A2:O' + str(len(deals) + 1)
print(cells)
wks.update(cells, data_l)

