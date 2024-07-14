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
                                    delivery INT
                               );''')
        self.db_cursor.execute(f'''CREATE TABLE IF NOT EXISTS Admin(
                                    chat_id INT PRIMARY KEY,
                                    is_delivering INT
                               );''')
        self.db_connection.commit()

    def subscribe_user_delivery_by_chat_id(self: Database, chat_id: int) -> None:
        self.db_cursor.execute(f'''INSERT INTO User(chat_id, delivery)
                                    VALUES
                                    ({chat_id}, TRUE)
                                    ON CONFLICT(chat_id) DO UPDATE
                                     SET delivery=TRUE
                                     WHERE chat_id={chat_id};''')
        self.db_connection.commit()

    def unsubscribe_user_delivery_by_chat_id(self: Database, chat_id: int) -> None:
        self.db_cursor.execute(f'''INSERT INTO User(chat_id, delivery)
                                    VALUES
                                    ({chat_id}, FALSE)
                                    ON CONFLICT(chat_id) DO UPDATE
                                     SET delivery=FALSE
                                     WHERE chat_id={chat_id};''')
        self.db_connection.commit()

    def get_delivery_chat_id_list(self: Database) -> list[int]:
        return [elem[0] for elem in self.db_cursor.execute(f'''SELECT chat_id
                                    FROM User;
                               ''').fetchall()] # using list comprehension to form list of values instead of list of tuples
    
    def add_admin_by_chat_id(self: Database, chat_id: int) -> None:
        self.db_cursor.execute(f'''INSERT INTO Admin(chat_id, is_delivering)
                                    VALUES
                                    ({chat_id}, FALSE)
                                    ON CONFLICT(chat_id) DO UPDATE
                                     SET is_delivering=FALSE
                                     WHERE chat_id={chat_id};''')
        self.db_connection.commit()
    
    def set_admin_to_delivering_by_chat_id(self: Database, chat_id: int) -> None:
        self.db_cursor.execute(f'''UPDATE Admin
                                    SET is_delivering=TRUE
                                    WHERE chat_id={chat_id}''')
        self.db_connection.commit()

    def unset_admin_to_delivering_by_chat_id(self: Database, chat_id: int) -> None:
        self.db_cursor.execute(f'''UPDATE Admin
                                    SET is_delivering=FALSE
                                    WHERE chat_id={chat_id}''')
        self.db_connection.commit()

    def is_admin_delivering_by_chat_id(self: Database, chat_id: int) -> bool:
        return bool(self.db_cursor.execute(f'''SELECT is_delivering
                                                FROM Admin
                                                WHERE chat_id={chat_id}''').fetchone()[0])
    
    def is_authorized_chat_id(self: Database, chat_id: int) -> bool:
        return (chat_id in [elem[0] for elem in self.db_cursor.execute(f'''SELECT chat_id
                                    FROM Admin;
                               ''').fetchall()]) # using list comprehension to form list of values instead of list of tuples

if __name__ == "__main__":
    db = Database()
