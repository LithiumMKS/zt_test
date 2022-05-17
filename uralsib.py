# -*- coding: utf-8 -*-
#! /usr/bin/python
import MySQLdb
import csv
import datetime


encoding = "utf-8"
"""
Раз месяц необходимо Уралсибу отправить актуальный список абонентов
Данный скрипт подготавливает txt файл в кодировке ansi
"""


def convert(input_list):
    """
    Форматируем выгрузку:
     удаляем лишние слова: улица, проспект, переулок, бульвар, шоссе, проезд
     и тд и тп
     Принимаем список, возвращаем список
    """
    #1 Перегенерируем список в 4 столбца
    result = []
    for row in input_list:
        rows2 = str(row[1] + ',' + row[2]).replace(", ",",").replace("улица,","").replace("проспект,","").replace("переулок,","").replace("бульвар,","").replace("шоссе,","").replace("проезд,","")
        #row[1] + ',' + row[2]
        result.append([row[0],rows2,row[3], '0.00',''])

    return result


start_time = datetime.datetime.now()
result = []
MyDB1 = MySQLdb.connect(host='10.100.100.2', user='aminev', passwd='aminev123', db='UTM5')
MyDB1.set_character_set('utf8')
cursor1 = MyDB1.cursor()

sql1 = ("SELECT users.full_name, gu.gw_house_address, "
       "users.flat_number, "
       "users.basic_account  from "
       "UTM5.account_tariff_link AS atl INNER JOIN "
       "UTM5.tariffs ON tariffs.id=atl.tariff_id INNER JOIN "
       "UTM5.users AS users ON atl.account_id=users.basic_account INNER JOIN "
       "gw.users AS gu ON gu.id=users.id INNER JOIN "
       "UTM5.accounts as ua ON ua.id=users.basic_account LEFT OUTER JOIN "
       "UTM5.blocks_info AS bl ON bl.account_id=users.basic_account "
       "WHERE "
       "users.is_juridical=0 and "
       "atl.is_deleted=0 "
       "AND ((bl.is_deleted=0 AND ((UNIX_TIMESTAMP(CURRENT_DATE)-(bl.start_date))/2592000 < 2)) "
       "OR "
       "(bl.is_deleted=1 AND bl.account_id NOT IN "
       "(SELECT account_id FROM blocks_info WHERE blocks_info.is_deleted=0 ))"
       "OR bl.is_deleted is NULL) "
       "group BY users.basic_account ")

try:
    cursor1.execute(sql1)
    results1 = cursor1.fetchall()
    if results1 == ():
        pass
    else:
        for row in results1:
            result.append(row)
except:
    print("Error: not exists string")
MyDB1.close()


date1 = datetime.date.today().strftime("-20%y-%m-%d")

with open ("уралсиб{}.txt".format(date1),'w') as f:
    writer1 = csv.writer(f)#,quoting=csv.QUOTE_NONE)
    #writer1.writerow([u'#FILESUM 0.00']),u'#TYPE 17',u'#SERVICE 7217',u'#NOTE'])
    writer1.writerow([u'#FILESUM 0.00'])
    writer1.writerow([u'#TYPE 17'])
    writer1.writerow([u'#SERVICE 7217'])
    writer1.writerow([u'#NOTE'])

    writer = csv.writer(f, delimiter=';')#,quoting=csv.QUOTE_NONE, escapechar=' ')

    writer.writerows(convert(result))
    writer.writerows(result)

print(datetime.datetime.now()-start_time)
