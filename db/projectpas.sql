DESCRIBE user;
ALTER TABLE user ADD COLUMN username VARCHAR(255) NOT NULL;
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    nama VARCHAR(255) NOT NULL,
    nama_toko VARCHAR(255) NOT NULL
);
INSERT INTO user (username, password, nama, nama_toko) VALUES ('jimi', '1234', 'jimi', 'js');