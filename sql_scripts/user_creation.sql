CREATE USER 'app_connection'@'localhost' IDENTIFIED BY 'Z4r*95qTT$^SGwVV';
GRANT SELECT, INSERT, UPDATE, DELETE ON espresso_experiment_tracker.* TO 'app_connection'@'localhost';
FLUSH PRIVILEGES;