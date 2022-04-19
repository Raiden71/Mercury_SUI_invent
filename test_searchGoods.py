import json
import sqlite3
from datetime import datetime


conn = sqlite3.connect(
    'C:\PythonProjects\SQLiteStudio\DataBases/1.db')  # ('//data/data/ru.travelfood.simple_ui/databases/SimpleWMS')
cursor1 = conn.cursor()
# --- отладочная часть, будет работать через Hashmap
i=0
CellCode=''
EmptyCode=''

while i<10:
    i+=1
    print(i)
    barcode=input('введите QR: ')
    if barcode=='':
        continue


    if barcode[0] == 'Н':  #Обработка QR номенклатуры
        barcodeList=barcode.split('&')


        GoodsCode=barcodeList[1]
        SeriesCode=barcodeList[2]
        EdIzmCode=barcodeList[3]
        Qtty=barcodeList[4]


        #GoodsCode = input('Код товара')
        #SeriesCode = input('Код серии')

        try:

            QueryText = """\
                select px_goods.Code, 
                px_goods.Name,
                Date,
                px_series.SerialNum,
                px_series.Code as SeriesCode,
                px_edizm.Qtty,
                px_pallet.Qtty as RealQtty
                 from px_goods
                Left Join px_series ON px_goods.Code=px_series.NomCode
                Left Join px_edizm ON px_edizm.NomCode=px_goods.Code
                Left Join px_pallet ON px_pallet.seriesCode=px_series.Code
                where px_goods.Code=? and px_series.Code=?
                """
            cursor1.execute(QueryText,(GoodsCode,SeriesCode))  #
        except sqlite3.Error as err:
            raise ValueError(err)
        a = cursor1.fetchall()
        # ----------  Надо добавить запись в приход товара
        # ----------- Сначала ищем подходящую ячейку в таблице, куда можно положить найденный товар
           #Создаем новую строку
        QueryText = """\
            INSERT into px_movement(CellWhere, WhereQtty,Goods,Series,PalletQtty,Sent)
            Values (:arg0,:arg1,:arg2,:arg3,:arg4,:arg5)
            """
        try:
            cursor1.execute(QueryText, (CellCode,Qtty,GoodsCode,SeriesCode,a[0][7],False))
            conn.commit()

        except sqlite3.Error as err:
            raise ValueError(err)

        #RzDate=datetime.strptime(a[0][2], '%d.%m.%Y') #, '%d-%m-%Y %H:%M:%S %f'

     #   print(RzDate)
     #   print(a)
     #    if a.__len__()>0:
     #        sklNum=input('Веедите код склада:')
     #        if sklNum[0] == 'С':
     #            sklNumList=sklNum.split('&')




    elif barcode[0]=='С': #обработка QR склада
        CellCode=barcode.split('&')[1]
        #print(barcode)
        QueryText = """\
        UPDATE
        px_movement
        set
        CellWhere =:CellCode
        WHERE
        px_movement.CellWhere =:EmptyCode
        """
        try:
            cursor1.execute(QueryText, (CellCode,EmptyCode))
        except sqlite3.Error as err:
            raise ValueError(err)
        conn.commit()

conn.close()