-- DROP TABLE IF EXISTS userlist;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS tobuylist;

-- CREATE TABLE userlist(
-- 	user_id INTEGER PRIMARY KEY AUTOINCREMENT,
--     user_login TEXT UNIQUE NOT NULL,
--     user_password TEXT NOT NULL,
--     user_role TEXT, /* "admin" or "user" */
--     user_school INTEGER,
--     user_request_inv TEXT  /* id запрошенного инв, id статуса заявки, количество  */
-- );

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

CREATE TABLE tobuylist(
    buy_id INTEGER PRIMARY KEY AUTOINCREMENT,
    buy_title TEXT UNIQUE NOT NULL,
    buy_cost INTEGER, 
    -- цена в рублях
    buy_from TEXT,
    -- поставщик
    buy_cond TEXT
    -- Статус - ожидание / куплено
);

