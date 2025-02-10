DROP TABLE IF EXISTS inventory;

CREATE TABLE inventory(
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_title TEXT  NOT NULL,
    item_number INTEGER, /* Количество */
    item_photo TEXT,  /* путь к файлу */
    item_req TEXT,  /* login usera владельца */
    item_ur1 TEXT, /* login usera с запросом*/
    item_cond TEXT,  /* состояние предмета */
    item_school INTEGER
);


