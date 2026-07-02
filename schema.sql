CREATE DATABASE IF NOT EXISTS security_test;
USE security_test;

DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id VARCHAR(50) NOT NULL,
    username VARCHAR(50) NOT NULL,
    pw VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

INSERT INTO users (id, username, pw) VALUES ('admin', 'Administrator', 'admin1234');
INSERT INTO users (id, username, pw) VALUES ('guest', 'GuestUser', 'guest1234');