CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    active INTEGER DEFAULT 1,
    rfid CHARACTER(16),
    balance FLOAT DEFAULT 0
);

CREATE TABLE operation (
    id INTEGER PRIMARY KEY,
    user_id INT NOT NULL,
    amount FLOAT NOT NULL,
    date DATETIME NOT NULL
);
