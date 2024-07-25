from __future__ import annotations
import sqlite3

class Database:
    """
    Database to store bot users ID's in order to keep them updated with delivery
    """
    def __init__(self: Database, filename: str="database.db") -> None:
        self.db_filename = filename
        self.db_connection = sqlite3.connect(self.db_filename, check_same_thread=False)
        self.db_cursor = self.db_connection.cursor()
        # creating tables in database if they are not existent
        self.db_cursor.execute(f'''CREATE TABLE IF NOT EXISTS User(
                                    chat_id INT PRIMARY KEY,
                                    state INT,
                                    delivery INT
                               );''')
        self.db_cursor.execute(f'''CREATE TABLE IF NOT EXISTS Admin(
                                    chat_id INT PRIMARY KEY,
                                    state INT,
                                    is_superadmin INT
                               );''')
        self.db_cursor.execute(f'''CREATE TABLE IF NOT EXISTS OneTimePassword(
                                    admin_chat_id INT,
                                    password CHAR
                               );''')
        self.db_connection.commit()

    # USER

    def set_user_delivery_by_chat_id(self: Database, chat_id: int, delivery: int) -> None:
        self.db_cursor.execute(f'''UPDATE User
                                    SET delivery={delivery}
                                    WHERE chat_id={chat_id}''')
        self.db_connection.commit()

    def add_user_by_chat_id(self: Database, chat_id: int) -> None:
        self.db_cursor.execute(f'''INSERT INTO User(chat_id, state, delivery)
                                    VALUES
                                    ({chat_id}, 0, FALSE)
                                    ON CONFLICT(chat_id) DO UPDATE
                                     SET state=0, delivery=FALSE
                                     WHERE chat_id={chat_id};''')
        self.db_connection.commit()

    def is_user_exists_by_chat_id(self: Database, chat_id: int) -> bool:
        return (len(self.db_cursor.execute(f'''SELECT *
                                            FROM User
                                            WHERE chat_id={chat_id};
                                            ''').fetchall()) > 0)

    def set_user_state_by_chat_id(self: Database, chat_id: int, state: int) -> None:
        self.db_cursor.execute(f'''UPDATE User
                                    SET state={state}
                                    WHERE chat_id={chat_id}''')
        self.db_connection.commit()

    def get_user_state_by_chat_id(self: Database, chat_id: int) -> int:
        return self.db_cursor.execute(f'''SELECT state
                                                FROM User
                                                WHERE chat_id={chat_id}''').fetchone()[0]

    def get_user_delivery_by_chat_id(self: Database, chat_id: int) -> int:
        return self.db_cursor.execute(f'''SELECT delivery
                                                FROM User
                                                WHERE chat_id={chat_id}''').fetchone()[0]

    def get_delivery_chat_id_list(self: Database) -> list[int]:
        # better use iterator
        return [elem[0] for elem in self.db_cursor.execute(f'''SELECT chat_id
                                    FROM User;
                               ''').fetchall()] # using list comprehension to form list of values instead of list of tuples
    
    # ADMINISTRATION
    
    def add_admin_by_chat_id(self: Database, chat_id: int) -> None:
        self.db_cursor.execute(f'''INSERT INTO Admin(chat_id, state, is_superadmin)
                                    VALUES
                                    ({chat_id}, 0, 0)
                                    ON CONFLICT(chat_id) DO UPDATE
                                     SET state=0, is_superadmin=0
                                     WHERE chat_id={chat_id};''')
        self.db_connection.commit()
    
    def set_admin_state_by_chat_id(self: Database, chat_id: int, state: int) -> None:
        self.db_cursor.execute(f'''UPDATE Admin
                                    SET state={state}
                                    WHERE chat_id={chat_id}''')
        self.db_connection.commit()

    def set_superadmin_by_chat_id(self: Database, chat_id: int, is_superadmin: int) -> None:
        self.db_cursor.execute(f'''UPDATE Admin
                                    SET is_superadmin={is_superadmin}
                                    WHERE chat_id={chat_id}''')
        self.db_connection.commit()

    def get_admin_state_by_chat_id(self: Database, chat_id: int) -> int:
        return self.db_cursor.execute(f'''SELECT state
                                                FROM Admin
                                                WHERE chat_id={chat_id}''').fetchone()[0]
    
    def is_admin_by_chat_id(self: Database, chat_id: int) -> bool:
        return (len(self.db_cursor.execute(f'''SELECT *
                                            FROM Admin
                                            WHERE chat_id={chat_id};
                                            ''').fetchall()) > 0)
    
    def is_superadmin_by_chat_id(self: Database, chat_id: int) -> bool:
        return (len(self.db_cursor.execute(f'''SELECT *
                                            FROM Admin
                                            WHERE chat_id={chat_id} AND is_superadmin=1;
                                            ''').fetchall()) > 0)
    
    def create_one_time_password(self: Database, chat_id: int, password: str) -> None:
        self.db_cursor.execute(f'''INSERT INTO OneTimePassword(admin_chat_id, password)
                                    VALUES
                                    ({chat_id}, "{password}");''')
        self.db_connection.commit()

    def delete_one_time_password(self: Database, password: str) -> None:
        self.db_cursor.execute(f'''DELETE FROM OneTimePassword
                                    WHERE
                                    password="{password}";''')
        self.db_connection.commit()

    def is_one_time_password(self: Database, password: str) -> bool:
        return (len(self.db_cursor.execute(f'''SELECT *
                                            FROM OneTimePassword
                                            WHERE password="{password}";
                                            ''').fetchall()) > 0)

if __name__ == "__main__":
    db = Database()
