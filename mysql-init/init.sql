CREATE DATABASE IF NOT EXISTS config_db;
CREATE DATABASE IF NOT EXISTS micro1_db;

CREATE USER IF NOT EXISTS 'config_user'@'%' IDENTIFIED BY 'config_pass';
CREATE USER IF NOT EXISTS 'micro1_user'@'%' IDENTIFIED BY 'micro1_pass';

GRANT ALL PRIVILEGES ON config_db.* TO 'config_user'@'%';
GRANT ALL PRIVILEGES ON micro1_db.* TO 'micro1_user'@'%';

FLUSH PRIVILEGES;
