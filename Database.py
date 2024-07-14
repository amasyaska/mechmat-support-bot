from __future__ import annotations
import sqlite3

class Database:
    """
    Database to store bot users ID's in order to keep them updated with delivery
    """
    def __init__(self: Database, filename: str="database.db") -> None:
        self.db_filename = filename
        self.db_connection = sqlite3.connect(self.db_filename)
        self.db_cursor = self.db_connection.cursor()
        # creating tables in database if they are not existent
        self.db_cursor.execute(f'''CREATE TABLE IF NOT EXISTS User(
                                    chat_id INT PRIMARY KEY,
                                    delivery INT
                               );''')
        self.db_connection.commit()

    def subscribe_user_delivery_by_chat_id(self: Database, chat_id) -> None:
        self.db_cursor.execute(f'''INSERT INTO User(chat_id, delivery)
                                    VALUES
                                    ({chat_id}, TRUE)
                                    ON CONFLICT(chat_id) DO UPDATE
                                     SET delivery=TRUE
                                     WHERE chat_id={chat_id};''')
        self.db_connection.commit()

    def unsubscribe_user_delivery_by_chat_id(self: Database, chat_id) -> None:
        self.db_cursor.execute(f'''INSERT INTO User(chat_id, delivery)
                                    VALUES
                                    ({chat_id}, FALSE)
                                    ON CONFLICT(chat_id) DO UPDATE
                                     SET delivery=FALSE
                                     WHERE chat_id={chat_id};''')
        self.db_connection.commit()

if __name__ == "__main__":
    db = Database()
    db.unsubscribe_user_delivery_by_chat_id(12)
