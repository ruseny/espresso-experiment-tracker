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