from dependency_inj.db_session import db_engine
from sqlmodel import Session, text, select, bindparam
from data_models.db_models import UserDefaults
from datetime import date, timedelta

def get_user_dict() -> dict:
    query = text("""
        SELECT id, username
        FROM Users
        ;
    """)
    with Session(db_engine) as session:
        result = session.exec(query)
    return {row.id: row.username for row in result}

def get_coffee_machine_dict(user_id : int) -> dict:
    query = text("""
        SELECT 
            e.coffee_machine_id AS id,
            CONCAT(
                m.manufacturer, ' ', 
                m.model_name, ' ', 
                m.model_name_add, ' ', 
                m.model_specification
                ) AS product
        FROM EquipmentOwnership AS e
        JOIN CoffeeMachines AS m
        ON e.coffee_machine_id = m.id
        WHERE e.user_id = :user_id
            AND e.equipment_type = 'coffee_machine'
        ;
    """).bindparams(
        bindparam("user_id", user_id)
    )
    with Session(db_engine) as session:
        result = session.exec(query)
    return {row.id: row.product for row in result}

def get_grinder_dict(user_id : int) -> dict:
    query = text("""
        SELECT 
            e.grinder_id AS id,
            CONCAT(
                g.manufacturer, ' ', 
                g.model_name, ' ', 
                g.model_name_add, ' ', 
                g.model_specification
                ) AS product
        FROM EquipmentOwnership AS e
        JOIN Grinders AS g
        ON e.grinder_id = g.id
        WHERE e.user_id = :user_id
            AND e.equipment_type = 'grinder'
        ;
    """).bindparams(
        bindparam("user_id", user_id)
    )
    with Session(db_engine) as session:
        result = session.exec(query)
    return {row.id: row.product for row in result}

def get_all_coffee_machine_manufacturers() -> list:
    query = text("""
        SELECT DISTINCT manufacturer
        FROM CoffeeMachines
        ;
    """)
    with Session(db_engine) as session:
        result = session.exec(query)
    return [row.manufacturer for row in result]

def get_all_coffee_machines_dict(manufacturers = None) -> dict:
    if manufacturers is None:
        manufacturers = get_all_coffee_machine_manufacturers()
    query = text("""
        SELECT 
            id,
            CONCAT(
                manufacturer, ' ', 
                model_name, ' ', 
                model_name_add, ' ', 
                model_specification
                ) AS product
        FROM CoffeeMachines
        WHERE manufacturer IN :manufacturers
        ;
    """).bindparams(
        bindparam("manufacturers", manufacturers, expanding = True)
    )
    with Session(db_engine) as session:
        result = session.exec(query)
    return {row.id: row.product for row in result}

def get_all_grinder_manufacturers() -> list:
    query = text("""
        SELECT DISTINCT manufacturer
        FROM Grinders
        ;
    """)
    with Session(db_engine) as session:
        result = session.exec(query)
    return [row.manufacturer for row in result]

def get_all_grinders_dict(manufacturers = None) -> dict:
    if manufacturers is None:
        manufacturers = get_all_grinder_manufacturers()
    query = text("""
        SELECT 
            id,
            CONCAT(
                manufacturer, ' ', 
                model_name, ' ', 
                model_name_add, ' ', 
                model_specification
                ) AS product
        FROM Grinders
        WHERE manufacturer IN :manufacturers
        ;
    """).bindparams(
        bindparam("manufacturers", manufacturers, expanding = True)
    )
    with Session(db_engine) as session:
        result = session.exec(query)
    return {row.id: row.product for row in result}

def get_all_equipment_sellers_list() -> list:
    query = text("""
        SELECT DISTINCT purchased_from AS seller
        FROM EquipmentOwnership
        ;
    """)
    with Session(db_engine) as session:
        result = session.exec(query)
    return [row.seller for row in result]

def get_all_producers_list() -> list:
    query = text("""
        SELECT DISTINCT producer
        FROM CoffeeBeanVarieties
        ;
        """)
    with Session(db_engine) as session:
        result = session.exec(query)
    return [row.producer for row in result]

def get_all_coffees_dict(producers : list = None) -> dict:
    if producers is None:
        producers = get_all_producers_list()
    query = text("""
        SELECT 
            id,
            CONCAT(
                producer, ' ', 
                name, ' '
                ) AS product
        FROM CoffeeBeanVarieties
        WHERE producer IN :producers
        ;
    """).bindparams(
        bindparam("producers", producers, expanding = True)
    )
    with Session(db_engine) as session:
        result = session.exec(query)
    return {row.id: row.product for row in result}

def get_all_sellers_list() -> list:
    query = text("""
        SELECT DISTINCT sorted.purchased_from AS seller
        FROM (
            SELECT purchased_from, purchase_date
            FROM CoffeeBeanPurchases
            ORDER BY id DESC
        ) AS sorted
        ;
        """)
    with Session(db_engine) as session:
        result = session.exec(query)
    return [row.seller for row in result]

def get_producer_list(user_id : int, 
    time_frame : int = 30, max_items : int = 10) -> list:
    date_threshold = date.today() - timedelta(days = time_frame)
    date_threshold = date_threshold.strftime("%Y-%m-%d")
    query = text("""
        SELECT DISTINCT v.producer AS producer
        FROM CoffeeBeanPurchases AS p
        JOIN CoffeeBeanVarieties AS v
        ON p.variety_id = v.id
        WHERE p.purchase_date >= :date_threshold
            AND p.user_id = :user_id
        LIMIT :max_items
        ;
    """).bindparams(
        bindparam("date_threshold", date_threshold),
        bindparam("user_id", user_id),
        bindparam("max_items", max_items)
    )
    with Session(db_engine) as session:
        result = session.exec(query)
    return [row.producer for row in result]

def get_purchase_dict(user_id : int, 
    time_frame : int = 30, max_items : int = 10, 
    producers : list = None) -> dict:

    date_threshold = date.today() - timedelta(days = time_frame)
    date_threshold = date_threshold.strftime("%Y-%m-%d")

    if producers is None:
        producers = get_producer_list(user_id, time_frame, max_items)
    query = text("""
        SELECT p.id AS id, CONCAT(
            v.producer, ' ', v.name, 
            ', purchased on ', 
            DATE_FORMAT(p.purchase_date, "%Y-%m-%d")
            ) AS product
        FROM CoffeeBeanPurchases AS p
        JOIN CoffeeBeanVarieties AS v
        ON p.variety_id = v.id
        WHERE p.purchase_date >= :date_threshold
            AND p.user_id = :user_id
            AND v.producer IN :producers
        ORDER BY p.id DESC
        LIMIT :max_items
        ;
    """).bindparams(
        bindparam("producers", producers, expanding = True),
        bindparam("date_threshold", date_threshold),
        bindparam("user_id", user_id),
        bindparam("max_items", max_items)
    )
    with Session(db_engine) as session:
        result = session.exec(query)
    return {row.id: row.product for row in result}

def get_user_defaults_dict(user_id : int) -> dict:
    query = select(UserDefaults).where(UserDefaults.user_id == user_id)
    with Session(db_engine) as session:
        result = session.exec(query).one()
    return result.model_dump(mode = "json")

def get_users_last_experiment(user_id : int) -> dict:
    query = text("""
        SELECT id, 
            DATE_FORMAT(
                 experiment_datetime, "%Y-%m-%d %H:%i:%S"
            ) AS experiment_datetime
        FROM EspressoExperiments
        WHERE user_id = :user_id
        ORDER BY experiment_datetime DESC
        LIMIT 1
        ;
    """).bindparams(
        bindparam("user_id", user_id)
    )
    with Session(db_engine) as session:
        result = session.exec(query).one()
    return {
        "id" : result.id,
        "experiment_datetime" : result.experiment_datetime
    }

def get_espresso_filter_default_range(user_id : int) -> dict:
    select_from = """
        SELECT
            DATE(MIN(experiment_datetime)) AS min_date,
            DATE(MAX(experiment_datetime)) AS max_date,
            MIN(grind_setting) AS min_grind_level,
            MAX(grind_setting) AS max_grind_level,
            MIN(dose_gr) AS min_dose,
            MAX(dose_gr) AS max_dose,
            MIN(extraction_time_sec) AS min_time,
            MAX(extraction_time_sec) AS max_time,
            MIN(yield_gr) AS min_yield,
            MAX(yield_gr) AS max_yield,
            MIN(ROUND(yield_gr/dose_gr, 2)) AS min_ratio,
            MAX(ROUND(yield_gr/dose_gr, 2)) AS max_ratio, 
            MIN(evaluation_general) AS min_evaluation_general,
            MAX(evaluation_general) AS max_evaluation_general, 
            MIN(evaluation_flavor) AS min_evaluation_flavor,
            MAX(evaluation_flavor) AS max_evaluation_flavor, 
            MIN(evaluation_body) AS min_evaluation_body,
            MAX(evaluation_body) AS max_evaluation_body, 
            MIN(evaluation_crema) AS min_evaluation_crema,
            MAX(evaluation_crema) AS max_evaluation_crema
        FROM EspressoExperiments
    """
    if user_id == 0:
        query = text(f"{select_from};")
    else:
        query = text(f"""
            {select_from}
            WHERE user_id = :user_id
            ;
        """).bindparams(
            bindparam("user_id", user_id)
        )

    with Session(db_engine) as session:
        result = session.exec(query).one()
    return result._asdict()  

def get_coffee_dict_from_espresso(user_id : int) -> dict:
    select_from = """
        SELECT 
            id, 
            CONCAT(
                name, " (", producer, ")"
            ) AS product
        FROM CoffeeBeanVarieties
        WHERE id IN (
            SELECT DISTINCT p.variety_id
            FROM EspressoExperiments AS e
            JOIN CoffeeBeanPurchases AS p
            ON e.coffee_bean_purchase_id = p.id
    """
    if user_id == 0:
        query = text(f"{select_from});")
    else:
        query = text(f"""
            {select_from} WHERE e.user_id = :user_id);
        """).bindparams(
            bindparam("user_id", user_id)
        )
    with Session(db_engine) as session:
        result = session.exec(query)
    return {row.id: row.product for row in result}

def get_machine_dict_from_espresso(user_id : int) -> dict:
    select_from = """
        SELECT 
            id, 
            CONCAT(
                manufacturer, ' ', 
                model_name, ' ', 
                model_name_add, ' ', 
                model_specification
            ) AS product
        FROM CoffeeMachines
        WHERE id IN (
            SELECT DISTINCT coffee_machine_id
            FROM EspressoExperiments
    """
    if user_id == 0:
        query = text(f"{select_from});")
    else:
        query = text(f"""
            {select_from} WHERE user_id = :user_id);
        """).bindparams(
            bindparam("user_id", user_id)
        )
    with Session(db_engine) as session:
        result = session.exec(query)
    return {row.id: row.product for row in result}

def get_grinder_dict_from_espresso(user_id : int) -> dict:
    select_from = """
        SELECT 
            id, 
            CONCAT(
                manufacturer, ' ', 
                model_name, ' ', 
                model_name_add, ' ', 
                model_specification
            ) AS product, 
            min_espresso_range, 
            max_espresso_range
        FROM Grinders
        WHERE id IN (
            SELECT DISTINCT grinder_id
            FROM EspressoExperiments
    """
    if user_id == 0:
        query = text(f"{select_from});")
    else:
        query = text(f"""
            {select_from} WHERE user_id = :user_id);
        """).bindparams(
            bindparam("user_id", user_id)
        )
    with Session(db_engine) as session:
        result = session.exec(query)
    return {row.id: [row.product, row.min_espresso_range, row.max_espresso_range] for row in result}

def get_selected_espresso_data(user_id : int, applied_filters : dict = None) -> dict:
    select_from = """
        SELECT *
        FROM EspressoExperiments
        WHERE user_id = :user_id
        """
    if bool(not applied_filters):
        query = text(f"{select_from};").bindparams(
            bindparam("user_id", user_id)
        )
    else:
        query = text(f"""
            {select_from}
            AND grind_setting BETWEEN :min_grind_level AND :max_grind_level
            AND dose_gr BETWEEN :min_dose AND :max_dose
            AND extraction_time_sec BETWEEN :min_time AND :max_time
            AND yield_gr BETWEEN :min_yield AND :max_yield
            AND ROUND(yield_gr/dose_gr, 2) BETWEEN :min_ratio AND :max_ratio
            AND evaluation_general BETWEEN :min_evaluation_general AND :max_evaluation_general
            AND evaluation_flavor BETWEEN :min_evaluation_flavor AND :max_evaluation_flavor
            AND evaluation_body BETWEEN :min_evaluation_body AND :max_evaluation_body
            AND evaluation_crema BETWEEN :min_evaluation_crema AND :max_evaluation_crema
            ;
        """).bindparams(
            bindparam("user_id", user_id),
            bindparam("min_grind_level", applied_filters["grind_level"][0]),
            bindparam("max_grind_level", applied_filters["grind_level"][1]),
            bindparam("min_dose", applied_filters["dose"][0]),
            bindparam("max_dose", applied_filters["dose"][1]),
            bindparam("min_time", applied_filters["extraction_time"][0]),
            bindparam("max_time", applied_filters["extraction_time"][1]),
            bindparam("min_yield", applied_filters["yield"][0]),
            bindparam("max_yield", applied_filters["yield"][1]),
            bindparam("min_ratio", applied_filters["ratio"][0]),
            bindparam("max_ratio", applied_filters["ratio"][1]),
            bindparam("min_evaluation_general", applied_filters["evaluation_general"][0]),
            bindparam("max_evaluation_general", applied_filters["evaluation_general"][1]),
            bindparam("min_evaluation_flavor", applied_filters["evaluation_flavor"][0]),
            bindparam("max_evaluation_flavor", applied_filters["evaluation_flavor"][1]),
            bindparam("min_evaluation_body", applied_filters["evaluation_body"][0]),
            bindparam("max_evaluation_body", applied_filters["evaluation_body"][1]),
            bindparam("min_evaluation_crema", applied_filters["evaluation_crema"][0]),
            bindparam("max_evaluation_crema", applied_filters["evaluation_crema"][1])
        )

    with Session(db_engine) as session:
        result = session.exec(query).fetchall()
    return {
        "columns": result[0]._fields, 
            "data": [tuple(row._asdict().values()) for row in result]
    } if result else {"columns": [], "data": []}
