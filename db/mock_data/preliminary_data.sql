INSERT INTO Users (
    username, 
    registration_datetime,
    user_type
)
VALUES
    ("test_user_1", "2025-04-01 12:00:00", "test"), 
    ("test_user_2", "2025-04-01 12:00:00", "test"), 
    ("test_user_3", "2025-04-01 12:00:00", "test"), 
    ("test_user_4", "2025-04-01 12:00:00", "test"), 
    ("test_user_5", "2025-04-01 12:00:00", "test"), 
    ("test_user_6", "2025-04-01 12:00:00", "test"), 
    ("test_user_7", "2025-04-01 12:00:00", "test"), 
    ("test_user_8", "2025-04-01 12:00:00", "test"), 
    ("test_user_9", "2025-04-01 12:00:00", "test"), 
    ("test_user_10", "2025-04-01 12:00:00", "test"), 
    ("test_user_11", "2025-04-01 12:00:00", "test"), 
    ("test_user_12", "2025-04-01 12:00:00", "test");

INSERT INTO CoffeeMachines (
    manufacturer, 
    model_name,
    model_name_add,
    model_specification,
    product_identifier,
    pump_pressure_bar,
    portafilter_diam_mm
)
VALUES
    ('DeLonghi', 'Dedica', '', 'Black', 'EC685.BK', 15, 51), 
    ('Sage/Breville', 'Barista', 'Pro', 'Brushed Stainless Steel', 'SES878BSS4EEU1', 15, 54), 
    ('Sage/Breville', 'Oracle', 'Touch', 'Matte Black', 'SES990BSS4EEU1', 9, 58), 
    ('Lelit', 'Bianca', '', 'Steel', 'LE-PL162T V3', 10, 58), 
    ('DeLonghi', 'La Specialista', 'Arte', 'Yellow', 'EC9155.YE', 15, 51), 
    ('Sage/Breville', 'Barista', 'Express', 'Black truffle', 'SES875BTR2EEU1', 9, 54);

INSERT INTO Grinders (
    manufacturer, 
    model_name,
    model_name_add,
    model_specification,
    product_identifier,
    operation_type,
    min_setting,
    max_setting, 
    min_espresso_range,
    max_espresso_range
)
VALUES
    ('Baratza', 'Encore', 'ESP', 'Black', '495W-230V-F', 'electric', 0, 40, 0, 20), 
    ('Sage/Breville', 'The Smart Grinder', 'Pro', 'Brushed Stainless Steel', 'SCG820BSS4EEU1', 'electric', 1, 60, 1, 30), 
    ('Eureka', 'Mignon', 'Oro', 'Black', 'EAN 8059519339448', 'electric', 0, 30, 0, 8), 
    ('Hario', 'Skerton', 'Plus', 'Schwarz', 'B01LXZACFB', 'manual', NULL, NULL, NULL, NULL), 
    ('DeLonghi', 'Dedica', 'Grinder', 'Steel, Silver ', 'KG520.M', 'electric', 1, 18, NULL, NULL);

INSERT INTO EquipmentOwnership (
    user_id, 
    equipment_type,
    coffee_machine_id,
    grinder_id
)
VALUES
    (1, 'coffee_machine', 1, NULL), 
    (2, 'coffee_machine', 1, NULL),
    (3, 'coffee_machine', 2, NULL), 
    (4, 'coffee_machine', 2, NULL), 
    (5, 'coffee_machine', 3, NULL), 
    (6, 'coffee_machine', 3, NULL), 
    (7, 'coffee_machine', 4, NULL),
    (8, 'coffee_machine', 4, NULL), 
    (9, 'coffee_machine', 5, NULL), 
    (10, 'coffee_machine', 5, NULL), 
    (11, 'coffee_machine', 6, NULL), 
    (12, 'coffee_machine', 6, NULL), 
    (1, 'grinder', NULL, 1), 
    (2, 'grinder', NULL, 2), 
    (3, 'grinder', NULL, 3), 
    (4, 'grinder', NULL, 1),
    (5, 'grinder', NULL, 2), 
    (6, 'grinder', NULL, 3), 
    (7, 'grinder', NULL, 1), 
    (8, 'grinder', NULL, 2), 
    (9, 'grinder', NULL, 3), 
    (10, 'grinder', NULL, 1), 
    (11, 'grinder', NULL, 2), 
    (12, 'grinder', NULL, 3);

INSERT INTO UserDefaults (
    user_id, 
    coffee_machine_id,
    grinder_id,
    basket_pressurized, 
    basket_shot_size, 
    portafilter_spout,
    wdt_used,
    tamping_method,
    leveler_used,
    puck_screen_used,
    setup_name
)
VALUES
    (1, 1, 1, 'no', 'double', 'bottomless', 'no', 'manual', 'no', 'no', 'testuser1sdefault'), 
    (2, 1, 2, 'no', 'double', 'bottomless', 'yes', 'manual', 'no', 'yes', 'testuser2sdefault'), 
    (3, 2, 3, 'no', 'double', 'double', 'yes', 'manual', 'no', 'no', 'testuser3sdefault'), 
    (4, 2, 1, 'no', 'double', 'double', 'no', 'manual', 'no', 'yes', 'testuser4sdefault'), 
    (5, 3, 2, 'no', 'double', 'double', 'no', 'manual', 'no', 'no', 'testuser5sdefault'), 
    (6, 3, 3, 'no', 'double', 'double', 'yes', 'manual', 'no', 'yes', 'testuser6sdefault'),
    (7, 4, 1, 'no', 'double', 'double', 'yes', 'manual', 'no', 'no', 'testuser7sdefault'),
    (8, 4, 2, 'no', 'double', 'double', 'no', 'manual', 'no', 'yes', 'testuser8sdefault'),
    (9, 5, 3, 'no', 'double', 'double', 'no', 'manual', 'no', 'no', 'testuser9sdefault'),
    (10, 5, 1, 'no', 'double', 'double', 'yes', 'manual', 'no', 'yes', 'testuser10sdefault'),
    (11, 6, 2, 'no', 'double', 'bottomless', 'yes', 'manual', 'no', 'no', 'testuser11sdefault'),
    (12, 6, 3, 'no', 'double', 'bottomless', 'no', 'manual', 'no', 'yes', 'testuser12sdefault');