from __future__ import annotations
import os
import psycopg2

from dotenv import load_dotenv, dotenv_values

load_dotenv()

DB_NAME = os.getenv("DB_NAME");
DB_HOST = os.getenv("DB_HOST");
DB_USER = os.getenv("DB_USER");
DB_PASSWORD = os.getenv("DB_PASSWORD");
DB_PORT = os.getenv("DB_PORT");


class Database:
    """
    Database to store bot users ID's in order to keep them updated with delivery
    """
    def __init__(self: Database, db_name: str=DB_NAME, db_host=DB_HOST, db_user=DB_USER, db_password=DB_PASSWORD, db_port=DB_PORT) -> None:
        self.db_name = db_name
        self.db_host = db_host
        self.db_user = db_user
        self.db_password = db_password
        self.db_port = db_port

        self.db_connection = psycopg2.connect(database=self.db_name,
                                                host=self.db_host,
                                                user=self.db_user,
                                                password=self.db_password,
                                                port=self.db_port)
        self.db_cursor = self.db_connection.cursor()
        # creating tables in database if they are not existent
        self.db_cursor.execute(f'''CREATE TABLE IF NOT EXISTS mechmatsupportbotuser(
                                    chat_id INT PRIMARY KEY,
                                    state INT,
                                    delivery BOOLEAN
                               );''')
        self.db_cursor.execute(f'''CREATE TABLE IF NOT EXISTS admin(
                                    chat_id INT PRIMARY KEY,
                                    state INT,
                                    is_superadmin BOOLEAN
                               );''')
        self.db_cursor.execute(f'''CREATE TABLE IF NOT EXISTS onetimepassword(
                                    admin_chat_id INT,
                                    password TEXT
                               );''')
        self.db_cursor.execute(f'''CREATE TABLE IF NOT EXISTS feedbackmessage(
                                    number INT PRIMARY KEY,
                                    chat_id INT,
                                    content TEXT,
                                    state INT,   -- 0 - unanswered, 1 - answered, 2 - closed
                                    admin_to_close_chat_id INT  -- -1 ~ no admin
                               );''')
        self.db_connection.commit()

    # USER

    def set_user_delivery_by_chat_id(self: Database, chat_id: int, delivery: bool) -> None:
        self.db_cursor.execute(f'''UPDATE mechmatsupportbotuser
                                    SET delivery={delivery}
                                    WHERE chat_id={chat_id}''')
        self.db_connection.commit()

    def add_user_by_chat_id(self: Database, chat_id: int) -> None:
        self.db_cursor.execute(f'''INSERT INTO mechmatsupportbotuser(chat_id, state, delivery)
                                    VALUES
                                    ({chat_id}, 0, FALSE);''')
        self.db_connection.commit()

    def is_user_exists_by_chat_id(self: Database, chat_id: int) -> bool:
        self.db_cursor.execute(f'''SELECT *
                                            FROM mechmatsupportbotuser
                                            WHERE chat_id={chat_id};
                                            ''')
        return (len(self.db_cursor.fetchall()) > 0)

    def set_user_state_by_chat_id(self: Database, chat_id: int, state: int) -> None:
        self.db_cursor.execute(f'''UPDATE mechmatsupportbotuser
                                    SET state={state}
                                    WHERE chat_id={chat_id}''')
        self.db_connection.commit()

    def get_user_state_by_chat_id(self: Database, chat_id: int) -> int:
        self.db_cursor.execute(f'''SELECT state
                                                FROM mechmatsupportbotuser
                                                WHERE chat_id={chat_id}''')
        return self.db_cursor.fetchone()[0]

    def get_user_delivery_by_chat_id(self: Database, chat_id: int) -> int:
        self.db_cursor.execute(f'''SELECT delivery
                                                FROM mechmatsupportbotuser
                                                WHERE chat_id={chat_id}''')
        return self.db_cursor.fetchone()[0]
    
    # ADMINISTRATION
    
    def add_admin_by_chat_id(self: Database, chat_id: int) -> None:
        self.db_cursor.execute(f'''INSERT INTO admin(chat_id, state, is_superadmin)
                                    VALUES
                                    ({chat_id}, 0, FALSE);''')
        self.db_connection.commit()
    
    def set_admin_state_by_chat_id(self: Database, chat_id: int, state: int) -> None:
        self.db_cursor.execute(f'''UPDATE admin
                                    SET state={state}
                                    WHERE chat_id={chat_id}''')
        self.db_connection.commit()

    def set_superadmin_by_chat_id(self: Database, chat_id: int, is_superadmin: int) -> None:
        self.db_cursor.execute(f'''UPDATE admin
                                    SET is_superadmin={is_superadmin}
                                    WHERE chat_id={chat_id}''')
        self.db_connection.commit()

    def get_admin_state_by_chat_id(self: Database, chat_id: int) -> int:
        self.db_cursor.execute(f'''SELECT state
                                                FROM admin
                                                WHERE chat_id={chat_id}''')
        return self.db_cursor.fetchall()[0][0]
    
    def is_admin_by_chat_id(self: Database, chat_id: int) -> bool:
        self.db_cursor.execute(f'''SELECT *
                                            FROM admin
                                            WHERE chat_id={chat_id};
                                            ''')
        return (len(self.db_cursor.fetchall()) > 0)
    
    def is_superadmin_by_chat_id(self: Database, chat_id: int) -> bool:
        self.db_cursor.execute(f'''SELECT *
                                            FROM admin
                                            WHERE chat_id={chat_id} AND is_superadmin=1;
                                            ''')
        return (len(self.db_cursor.fetchall()) > 0)
    
    def create_one_time_password(self: Database, chat_id: int, password: str) -> None:
        self.db_cursor.execute(f'''INSERT INTO onetimepassword(admin_chat_id, password)
                                    VALUES
                                    ({chat_id}, '{password}');''')
        self.db_connection.commit()

    def delete_one_time_password(self: Database, password: str) -> None:
        self.db_cursor.execute(f'''DELETE FROM onetimepassword
                                    WHERE
                                    password='{password}';''')
        self.db_connection.commit()

    def is_one_time_password(self: Database, password: str) -> bool:
        self.db_cursor.execute(f'''SELECT *
                                            FROM onetimepassword
                                            WHERE password='{password}';
                                            ''')
        return (len(self.db_cursor.fetchall()) > 0)
    
    # FEEDBACK

    def add_feedback_message_by_chat_id(self: Database, chat_id: int, content: int):
        # get number of rows
        self.db_cursor.execute(f'''SELECT
                                    COUNT (*)
                                    FROM
                                    feedbackmessage
                                    ''')
        number_of_rows = self.db_cursor.fetchone()[0]
        print(number_of_rows)
        self.db_cursor.execute(f'''INSERT INTO feedbackmessage(number, chat_id, content, state, admin_to_close_chat_id)
                                    VALUES
                                    ({number_of_rows}, {chat_id}, '{content}', 0, -1);''')
        self.db_connection.commit()

if __name__ == "__main__":
    db = Database()
