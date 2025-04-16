/*
    This script creates the database structure for the Espresso Experiment Tracker.
    It includes tables for users, coffee machines, grinders, portafilters, equipment setups,
    coffee bean varieties, coffee bean purchases, and espresso experiments.
    The file can be used in the MySQL shell with `source path/to/this/file.sql`, 
    or from the command line with `mysql [-u username -p] < path/to/this/file.sql`.
*/

CREATE DATABASE IF NOT EXISTS espresso_experiment_tracker;
USE espresso_experiment_tracker;

CREATE TABLE IF NOT EXISTS Users (
    id INT AUTO_INCREMENT NOT NULL, 
    username VARCHAR(255) NOT NULL,
    -- password_hash VARCHAR(255) NOT NULL,
    -- email VARCHAR(255) NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    date_of_birth DATE,
    registration_datetime DATETIME NOT NULL,
    user_type ENUM('home barista', 'professional barista', 'developer') NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS CoffeeMachines (
    id INT AUTO_INCREMENT NOT NULL, 
    manufacturer VARCHAR(255) NOT NULL,
    model_name VARCHAR(255) NOT NULL,
    model_name_add VARCHAR(255),
    model_specification VARCHAR(255),
    model_serial VARCHAR(255) NOT NULL,
    pump_pressure_bar SMALLINT NOT NULL,
    pump_type VARCHAR(255),
    water_temp_control VARCHAR(255),
    pid_control ENUM('automatic', 'programmable', ''),
    boiler_type VARCHAR(255),
    portafilter_diam_mm SMALLINT NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS Grinders (
    id INT AUTO_INCREMENT NOT NULL, 
    manufacturer VARCHAR(255) NOT NULL,
    model_name VARCHAR(255) NOT NULL,
    model_name_add VARCHAR(255),
    model_specification VARCHAR(255),
    model_serial VARCHAR(255) NOT NULL,
    operation_type ENUM('manual', 'electric') NOT NULL,
    burr_shape VARCHAR(255),
    burr_diameter_mm SMALLINT,
    burr_material VARCHAR(255),
    min_fine_setting SMALLINT,
    max_fine_setting SMALLINT,
    min_coarse_setting SMALLINT,
    max_coarse_setting SMALLINT, 
    single_dose ENUM('yes', 'no'),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS Portafilters (
    id INT AUTO_INCREMENT NOT NULL, 
    manufacturer VARCHAR(255) NOT NULL,
    model_name VARCHAR(255) NOT NULL,
    model_specification VARCHAR(255),
    model_serial VARCHAR(255) NOT NULL,
    basket_diameter_mm SMALLINT NOT NULL,
    pressurized ENUM('yes', 'no') NOT NULL,
    basket_shot_size ENUM('single', 'double', 'triple', 'quadruple') NOT NULL,
    spout ENUM('single', 'double', 'bottomless') NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS EquipmentOwnership (
    id INT AUTO_INCREMENT NOT NULL,
    user_id INT NOT NULL, 
    equipment_type ENUM('coffee_machine', 'grinder', 'portafilter') NOT NULL,
    coffee_machine_id INT,
    grinder_id INT,
    portafilter_id INT,
    purchase_date DATE,
    purchased_from VARCHAR(255),
    purchase_price_eur DECIMAL(7,2),
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES Users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (coffee_machine_id) REFERENCES CoffeeMachines(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (grinder_id) REFERENCES Grinders(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (portafilter_id) REFERENCES Portafilters(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS UserDefaults (
    user_id INT NOT NULL,
    coffee_machine_id INT NOT NULL,
    grinder_id INT NOT NULL,
    portafilter_id INT NOT NULL,
    wdt_used ENUM('yes', 'no') NOT NULL,
    tamping_method ENUM('manual', 'electric') NOT NULL,
    tamping_weight_kg SMALLINT,
    leveler_used ENUM('yes', 'no') NOT NULL,
    puck_screen_used ENUM('yes', 'no') NOT NULL,
    puck_screen_thickness_mm DECIMAL(5, 2),
    water_temp_c SMALLINT DEFAULT 93,
    setup_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (user_id),
    FOREIGN KEY (coffee_machine_id) REFERENCES CoffeeMachines(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (grinder_id) REFERENCES Grinders(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (portafilter_id) REFERENCES Portafilters(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS CoffeeBeanVarieties (
    id INT AUTO_INCREMENT NOT NULL, 
    producer VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    origin VARCHAR(255),
    origin_type ENUM('single origin', 'blend') NOT NULL,
    arabica_ratio DECIMAL(3,2),
    roast_level DECIMAL(3,2),
    intensity DECIMAL(3,2),
    acidity DECIMAL(3,2),
    flavor_notes VARCHAR(255),
    decaffeinated ENUM('yes', 'no') NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS CoffeeBeanPurchases (
    id INT AUTO_INCREMENT NOT NULL, 
    user_id INT NOT NULL,
    variety_id INT NOT NULL,
    purchase_date DATE NOT NULL,
    purchased_from VARCHAR(255) NOT NULL,
    roast_date DATE DEFAULT NULL,
    weight_kg DECIMAL(5,2) NOT NULL,
    price_per_kg_eur DECIMAL(5,2) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (variety_id) REFERENCES CoffeeBeanVarieties(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS EspressoExperiments (
    id INT AUTO_INCREMENT NOT NULL, 
    user_id INT NOT NULL DEFAULT 2,
    experiment_datetime DATETIME NOT NULL,
    coffee_machine_id INT NOT NULL,
    grinder_id INT NOT NULL,
    portafilter_id INT NOT NULL,
    wdt_used ENUM('yes', 'no') NOT NULL,
    tamping_method ENUM('manual', 'electric') NOT NULL,
    tamping_weight_kg SMALLINT,
    leveler_used ENUM('yes', 'no') NOT NULL,
    puck_screen_used ENUM('yes', 'no') NOT NULL,
    puck_screen_thickness_mm DECIMAL(5, 2),
    coffee_bean_purchase_id INT NOT NULL,
    grind_setting SMALLINT NOT NULL,
    dose_gr DECIMAL(5,2) NOT NULL,
    water_temp_c SMALLINT DEFAULT 93, 
    extraction_time_sec SMALLINT NOT NULL,
    yield_gr DECIMAL(5,2) NOT NULL,
    evaluation_general SMALLINT,
    evaluation_flavor SMALLINT,
    evaluation_body SMALLINT,
    evaluation_crema SMALLINT,
    evaluation_notes VARCHAR(255),
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES Users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (coffee_machine_id) REFERENCES CoffeeMachines(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (grinder_id) REFERENCES Grinders(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (portafilter_id) REFERENCES Portafilters(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (coffee_bean_purchase_id) REFERENCES CoffeeBeanPurchases(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE, 
    CONSTRAINT eval_range CHECK(
        (evaluation_general IS NULL OR evaluation_general BETWEEN 1 AND 10) AND
        (evaluation_flavor IS NULL OR evaluation_flavor BETWEEN 1 AND 10) AND
        (evaluation_body IS NULL OR evaluation_body BETWEEN 1 AND 10) AND
        (evaluation_crema IS NULL OR evaluation_crema BETWEEN 1 AND 10)
    )
);