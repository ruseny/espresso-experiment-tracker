CREATE TABLE IF NOT EXISTS Users (
    id INT AUTO_INCREMENT NOT NULL, 
    username VARCHAR(255) NOT NULL,
    -- password_hash VARCHAR(255) NOT NULL,
    -- email VARCHAR(255) NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    date_of_birth DATE,
    registration_date DATE NOT NULL,
    user_type ENUM('home barrista', 'professional barrista', 'developer') NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS CoffeeMachines (
    id INT AUTO_INCREMENT NOT NULL, 
    manufacturer VARCHAR(255) NOT NULL,
    model_series VARCHAR(255) NOT NULL,
    model_name VARCHAR(255),
    model_specification VARCHAR(255),
    model_serial VARCHAR(255) NOT NULL,
    pump_pressure_bar SMALLINT NOT NULL,
    pump_type VARCHAR(255),
    water_temp_control VARCHAR(255),
    boiler_type VARCHAR(255),
    portafilter_diam_mm SMALLINT NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS Grinders (
    id INT AUTO_INCREMENT NOT NULL, 
    manufacturer VARCHAR(255) NOT NULL,
    model_series VARCHAR(255) NOT NULL,
    model_name VARCHAR(255),
    model_specification VARCHAR(255),
    model_serial VARCHAR(255) NOT NULL,
    operation_type ENUM('manual', 'electric') NOT NULL,
    burr_shape VARCHAR(255),
    burr_diameter_mm SMALLINT,
    burr_material VARCHAR(255),
    min_fine_setting SMALLINT NOT NULL,
    max_fine_setting SMALLINT NOT NULL,
    min_coarse_setting SMALLINT,
    max_coarse_setting SMALLINT,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS Portafilters (
    id INT AUTO_INCREMENT NOT NULL, 
    manufacturer VARCHAR(255) NOT NULL,
    model_name VARCHAR(255) NOT NULL,
    model_specification VARCHAR(255),
    model_serial VARCHAR(255) NOT NULL,
    basket_diameter_mm SMALLINT NOT NULL,
    basket_depth_mm SMALLINT,
    pressurized ENUM('yes', 'no') NOT NULL,
    basket_shot_size ENUM('single', 'double', 'triple') NOT NULL,
    spout ENUM('single', 'double', 'bottomless') NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS EquipmentSetup (
    id INT AUTO_INCREMENT NOT NULL, 
    user_id INT NOT NULL,
    coffee_machine_id INT NOT NULL,
    grinder_id INT NOT NULL,
    portafilter_id INT,
    PRIMARY KEY (id),
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
    arabica_ratio DECIMAL(1,2),
    roast_level DECIMAL(1,2),
    intensity DECIMAL(1,2),
    acidity DECIMAL(1,2),
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
    roast_date DATE,
    weight_kg DECIMAL(2,2) NOT NULL,
    price_per_kg_eur DECIMAL(3,2) NOT NULL,
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
    experiment_date DATE NOT NULL,
    setup_id INT NOT NULL,
    coffee_bean_id INT NOT NULL,
    grind_setting SMALLINT NOT NULL,
    dose_gr DECIMAL(2,2) NOT NULL,
    wdt_used ENUM('yes', 'no') NOT NULL,
    -- tamping_method ENUM('manual', 'machine') NOT NULL,
    -- tamping_pressure_kg SMALLINT,
    leveler_used ENUM('yes', 'no') NOT NULL,
    puck_screen_used ENUM('yes', 'no') NOT NULL,
    -- puck_screen_type VARCHAR(255),
    extraction_time_sec SMALLINT NOT NULL,
    water_temp_c SMALLINT DEFAULT 93, 
    yield_gr DECIMAL(2,2) NOT NULL,
    evaluation_general SMALLINT,
    evaluation_flavor SMALLINT,
    evaluation_body SMALLINT,
    evaluation_crema SMALLINT,
    evaluation_notes VARCHAR(255),
    PRIMARY KEY (id),
    FOREIGN KEY (setup_id) REFERENCES EquipmentSetup(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (coffee_bean_id) REFERENCES CoffeeBeanPurchases(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);