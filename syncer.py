import dataclasses
import json

import psycopg2
import dotenv
import os
import converters

dotenv.load_dotenv()


@dataclasses.dataclass
class Setting:
    id: int
    knowledge_link: str
    database_link: str


def get_settings() -> list[Setting]:
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv('DB_PORT')
    )
    cur = conn.cursor()
    cur.execute(
        "SELECT id, knowledge_link, database_link FROM settings WHERE knowledge_link <> '' OR database_link <> ''")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [Setting(*row) for row in rows]


def update_database(setting_id: int, field_name: str, field_value: dict):
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()
    statement = f"UPDATE settings SET {field_name}=%s where id=%s", (json.dumps(field_value).replace('NaN', 'null'), setting_id)
    cur.execute(*statement)
    conn.commit()
    conn.close()


def sync():
    """
    1) Берет все настройки у которых есть база знаний или база данных
    2) Получает новые значения из Google таблиц
    3) Обновляет значение в базе
    """
    settings = get_settings()
    for setting in settings:
        try:
            if setting.knowledge_link != '':
                knowledge_data = converters.get_knowledge_data(setting.knowledge_link)
                update_database(setting.id, 'knowledge_data', knowledge_data)
            if setting.database_link != '':
                database_data = converters.get_database_data(setting.database_link)
                update_database(setting.id, 'database_data', database_data)
        except Exception as e:
            print('Error occured:', e)

