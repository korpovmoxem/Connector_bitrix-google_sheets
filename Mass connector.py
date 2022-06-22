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

for deal in deals:
    if deal['UF_CRM_628B602C0A665'] == '11791':
        id = deal['ID']  # ID сделки
        adress = deal['UF_CRM_1622808160']  # 0/ **адрес объекта для рассылок
        id_lead = deal['UF_CRM_1610379479']  # 0/ сквозное поле id лида
        data_start = deal['UF_CRM_5C6D1B8B434DE']  # Дата Взят в работу
        data_prepaid = deal['UF_CRM_1546943971']  # Дата внесения аванса
        data_lead_end = deal['UF_CRM_5F17C8B97CBA9']  # Дата завершения лида
        data_call_lost = deal['UF_CRM_626967A4197F3']  # Дата звонка (потеряшка)
        data_first_meeting = deal['UF_CRM_5ABA1794EF737']  # Дата и время первичной встречи
        data_change = deal['DATE_MODIFY']  # Дата изменения
        data_appointed_person = deal['UF_CRM_5E4D2DA5AFDCF']  # Дата Назначен ответственный 1
        data_begin = deal['BEGINDATE']  # Дата начала
        data_start_adv = deal['UF_CRM_1619530812769']  # Дата начала непрерывного рекламирования
        data_change_photo = deal['UF_CRM_1647865875']



count = 0
s = ''
temp = []
status_document = {'1396': 'ЭК', '1398': 'НЭ'}

# update cell in google sheet
count += 1
cells = 'A2:O' + str(len(deals) + 1)
print(cells)
wks.update(cells, data_l)

print(deals[0])

