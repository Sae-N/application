from django.db import connection
import logging
import csv
from datetime import datetime as dt

logger = logging.getLogger('development')


sql_insert = ("insert into weather_data (data_datetime, temperature, humidity, location_id, created_at, updated_at)"
    "select * from (select %s as data_datetime, %s as temperature, %s as humidity, %s as location_id, "
    "%s as created_at, %s as updated_at) as tmp "
    "where not exists (select * from weather_data wher location_id = %s and data_datetime = %s)")


def regist_data(cursor, file_path):
    try:
        file = open(file_path, newline='')
    except IOError:
        logger.warning('対象ファイルが存在しません：' + file_path)
        logger.warning('DB登録は行いません：' + file_path)
    else:
        logger.info('=== > Start DB登録 ==')
        with file:
            reader = csv.reader(file)
            header = next(reader)

            for row in reader:
                str_time = [dt.now().strftime('%Y-%m-%d %H:%M:%S')]
                add_data = []
                add_data.extend(row)
                add_data.extend(str_time)
                add_data.extend(str_time)
                add_data.append(row[3])
                add_data.append(row[0])
                logger.debug('add_data = ' + str(add_data))

                cursor.execute(sql_insert, add_data)

            logger.info("=== > End DB登録 ==")

def insert_csv_data(file_path):
    logger.info('== csvデータ登録処理開始 ==')

    with connection.cursor() as cursor:
        regist_data(cursor, file_path)

    logger.info('== csvデータ登録処理終了 ==')
