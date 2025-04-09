INSERT INTO Users (
    username, 
    first_name,
    last_name,
    date_of_birth,
    registration_datetime,
    user_type
)
VALUES
    (
        'rusen', 
        'Rusen',
        'Yasar', 
        '1987-03-03',
        '2025-04-02 12:00:00',
        'home barista'
    ), 
    (
        'app',
        '',
        '',
        NULL,
        '2025-04-02 12:00:00',
        'developer'
    );

INSERT INTO CoffeeMachines (
    manufacturer, 
    model_name,
    model_name_add,
    model_specification,
    model_serial,
    pump_pressure_bar,
    pump_type,
    water_temp_control,
    pid_control,
    boiler_type,
    portafilter_diam_mm
)
VALUES
    (
        'DeLonghi', 
        'Dedica', 
        '', 
        'Black',
        'EC685.BK', 
        15, 
        '', 
        'None', 
        '', 
        'Thermoblock', 
        51
    ), 
    (
        'Sage/Breville',
        'Barista',
        'Pro', 
        'Brushed Stainless Steel',
        'SES878BSS4EEU1', 
        15, 
        'Vibration', 
        'PID',
        'automatic',
        'Thermojet',
        54
    ), 
    (
        'Sage/Breville',
        'Oracle',
        'Touch',
        'Matte Black',
        'SES990BSS4EEU1',
        9,
        'Vibration',
        'PID',
        'programmable',
        'Dual Boiler',
        58
    );

INSERT INTO Grinders (
    manufacturer, 
    model_name,
    model_name_add,
    model_specification,
    model_serial,
    operation_type,
    burr_shape,
    burr_diameter_mm,
    burr_material,
    min_fine_setting,
    max_fine_setting,
    min_coarse_setting,
    max_coarse_setting,
    single_dose
)
VALUES
    (
        'Baratza', 
        'Encore', 
        'ESP', 
        'Black',
        '495W-230V-F', 
        'electric',
        'cone', 
        40, 
        'steel', 
        0,
        20,
        21,
        40,
        'no'
    ),
    (
        'Sage/Breville',
        'The Smart Grinder',
        'Pro',
        'Brushed Stainless Steel',
        'SCG820BSS4EEU1', 
        'electric',
        'cone',
        40, 
        'steel', 
        1, 
        30, 
        31, 
        60, 
        'no'
    ), 
    (
        'Hario', 
        'Skerton', 
        'Plus',
        'Schwarz', 
        'B01LXZACFB', 
        'manual',
        'cone', 
        38,
        'ceramic',
        NULL,
        NULL,
        NULL,
        NULL,
        'no'
    );

INSERT INTO Portafilters (
    manufacturer, 
    model_name,
    model_specification,
    model_serial,
    basket_diameter_mm,
    pressurized,
    basket_shot_size,
    spout
)
VALUES
    (
        'DeLonghi',
        'Dedica',
        'Portafilter',
        'B07337M11F',
        51,
        'yes',
        'single',
        'double'
    ), 
    (
        'DeLonghi',
        'Dedica',
        'Portafilter',
        'B07337M11F',
        51,
        'yes',
        'double',
        'double'
    ), 
    (
        'Neouza',
        'Portafilter 51mm',
        'extra part',
        'B087WM4T7J',
        51,
        'no',
        'single',
        'bottomless'
    ), 
    (
        'Neouza',
        'Portafilter 51mm',
        'default part',
        'B087WM4T7J',
        51,
        'no',
        'double',
        'bottomless'
    ), 
        (
        'Neouza',
        'Portafilter 51mm',
        'extra part',
        'B087WM4T7J',
        51,
        'no',
        'double',
        'bottomless'
    ), 
    (
        'Neouza',
        'Portafilter 51mm',
        'extra part',
        'B087WM4T7J',
        51,
        'no',
        'quadruple',
        'bottomless'
    ), 
    (
        'Sage/Breville',
        'Barista',
        'Portafilter',
        'SP0027237',
        54,
        'no',
        'double',
        'double'
    ), 
    (
        'Sage/Breville',
        'Oracle',
        'Portafilter',
        'SP0001817',
        58,
        'no',
        'double',
        'double'
    );

INSERT INTO EquipmentSetup (
    user_id, 
    coffee_machine_id,
    grinder_id,
    portafilter_id, 
    setup_name
)
VALUES
    (
        1, 
        1, 
        1, 
        4, 
        'Dedica, Baratza, bottomless#1 double'
    ), 
    (
        1, 
        1, 
        1, 
        5, 
        'Dedica, Baratza, botomless#2, double'
    ), 
    (
        2, 
        2, 
        2, 
        7, 
        'Sage Barista default, double'
    ), 
    (
        2, 
        3, 
        2, 
        8, 
        'Sage Oracle default, double'
    );

INSERT INTO CoffeeBeanVarieties (
    producer, 
    name,
    origin,
    origin_type,
    arabica_ratio,
    roast_level,
    intensity,
    acidity,
    flavor_notes,
    decaffeinated
)
VALUES
    (
        'Andraschko', 
        'Déjà vu', 
        'Latin America',
        'blend',
        1.0, 
        0.8, 
        0.75, 
        0.5,
        'fruit, chocolate, sweet', 
        'no'
    ), 
    (
        'Murnauer', 
        'San Pedro Bio', 
        'Honduras', 
        'single origin', 
        1.0, 
        0.8, 
        1.0, 
        0.25, 
        'nutty, chocolate', 
        'no'
    ), 
    (
        'Origeens', 
        'Susana',
        'Peru', 
        'single origin', 
        1.0, 
        NULL, 
        0.86, 
        NULL,
        'chocolate, nutty, fruit', 
        'no'
    ),
    (
        'Tchibo',
        'Barista Espresso', 
        'Brazil', 
        'blend', 
        1.0, 
        1.0, 
        0.83,
        0.0,
        'nutty', 
        'no'
    );

INSERT INTO CoffeeBeanPurchases (
    user_id, 
    variety_id,
    purchase_date,
    purchased_from,
    roast_date,
    weight_kg,
    price_per_kg_eur
)
VALUES
    (
        1, 
        1,
        '2025-03-22', 
        'roastmarket.de', 
        '2024-12-15', 
        0.25, 
        33.99
    ), 
    (
        1,
        2,
        '2025-03-22',
        'roastmarket.de',
        '2025-11-30', 
        0.25, 
        37.99
    ), 
    (
        1, 
        3, 
        '2025-04-01', 
        'origeens.com', 
        NULL,
        0.5, 
        28.77
    ), 
    (
        1,
        4, 
        '2025-03-15', 
        'edeka', 
        NULL, 
        1.0, 
        16.99
    ), 
    (
        1, 
        2, 
        '2025-01-10', 
        'roastmarket.de', 
        '2024-08-20', 
        0.25, 
        37.99
    ), 
    (
        2, 
        1,
        '2025-03-22', 
        'roastmarket.de', 
        '2024-12-15', 
        0.25, 
        33.99
    ), 
    (
        2, 
        2, 
        '2025-01-10', 
        'roastmarket.de', 
        '2024-08-20', 
        0.25, 
        37.99
    ), 
    (
        2,
        4, 
        '2025-03-15', 
        'edeka', 
        NULL, 
        1.0, 
        16.99
    );

INSERT INTO EspressoExperiments (
    experiment_datetime,
    user_id,
    setup_id,
    coffee_bean_purchase_id,
    grind_setting,
    dose_gr,
    wdt_used,
    leveler_used,
    puck_screen_used,
    extraction_time_sec, 
    yield_gr,
    evaluation_general,
    evaluation_flavor,
    evaluation_body,
    evaluation_crema,
    evaluation_notes
)
VALUES
    (
        '2025-04-03 10:00:00', 
        1,
        1, 
        1, 
        12, 
        18.0,
        'yes',
        'no',
        'yes', 
        27,
        30.0,
        8,
        7,
        9,
        10,
        'a little bitter, try shorter extraction or coarser grind'
    )
    