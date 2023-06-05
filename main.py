import asyncio
import psutil
import sqlite3 as sl
import datetime


async def main():
    db = db_load()
    asyncio.create_task(processor_load(db))


async def processor_load(connection):
    while True:
        db_insert_cpu_load(connection, psutil.cpu_percent(interval=5))


def db_insert_cpu_load(connection, value):
    try:
        cursor = connection.cursor()
        query = f"""INSERT INTO procLoadHistory
                            (percent, dateTime)
                            VALUES
                            ({value},'{datetime.datetime.now()}');"""
        cursor.execute(query)
        connection.commit()
        print(f"Запись [{value}] добавлена в таблицу [procLoadHistory]")
        cursor.close()
    except sl.Error as error:
        print("Ошибка при работе с SQLite", error)


def db_load():
    connection = sl.connect('webMonitor/database.sqlite3')
    with connection:
        data = connection.execute("select count(*) from sqlite_master where type='table' and name='procLoadHistory'")
        for row in data:
            if row[0] == 0:
                with connection:
                    connection.execute("""
                        CREATE TABLE procLoadHistory (
                            id INTEGER PRIMARY KEY,
                            percent FLOAT,
                            dateTime timestamp
                        );
                    """)
    return connection


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except asyncio.TimeoutError:
        print('Done')
