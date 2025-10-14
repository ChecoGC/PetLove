la bd:

CREATE DATABASE petlove CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
CREATE USER 'jovannylg'@'localhost' IDENTIFIED BY 'lupita123';
GRANT ALL PRIVILEGES ON petlove.* TO 'jovannylg'@'localhost';
FLUSH PRIVILEGES;
EXIT;

