import json
import requests
from requests.auth import HTTPBasicAuth
import sqlite3
from sqlite3.dbapi2 import Error

# if hashMap.get("listener") == "btn_run":
username = 'usr'
password = ""  # 'hashMap.get("WS_PASS")'
# url = 'http://192.168.1.107:80/Base/hs/simplewms'  # hashMap.get("WS_URL")
url = 'http://109.173.108.124:6792/1cbase/hs/simplewms'
android_id = '43'  # ''OID_ID")

r = requests.get(url + '/get_start_data?android_id=' + android_id, auth=HTTPBasicAuth(username, password, ),
                 headers={'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'})
print(r.status_code)
# print(r.text)
if r.status_code == 200:

    conn = sqlite3.connect(
        'C:\PythonProjects\SQLiteStudio\DataBases/1.db')  # ('//data/data/ru.travelfood.simple_ui/databases/SimpleWMS')

    try:
        cursor1 = conn.cursor()
        cursor1.executescript('DROP INDEX IF EXISTS goods_index') #Удаляем индексы таблиц и серий перед
        cursor1.executescript('DROP INDEX IF EXISTS Series_index')# загрузкой большого объема данных
    except sqlite3.Error as err:
        raise ValueError(err)

    r.encoding = 'utf-8'
    jdata = json.loads(r.text.encode("utf-8"))
    for sql_r in jdata:
        # print(sql_r['sql'])

        # r = requests.get(url + '/set_ticket?android_id=' + android_id + "&uuid=" + sql_r['uuid'],
        #                 auth=HTTPBasicAuth(username, password, ),
        #                 headers={'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'})
        print(sql_r['sql'])
        try:
            #  cursor1 = conn.cursor()
            cursor1.executescript(sql_r['sql'])
            conn.commit()
        except sqlite3.Error as err:
            raise ValueError(err)
    print('Создаем индексы')
    # Возвращаем индексы обратно
    cursor1.executescript('CREATE INDEX goods_index ON px_goods (Code COLLATE RTRIM ASC)')
    cursor1.executescript('CREATE INDEX Series_index ON px_series (NomCode COLLATE RTRIM ASC,Code COLLATE RTRIM ASC)')
    conn.close()
    print('Финиш')