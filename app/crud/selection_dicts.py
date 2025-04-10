from ..dependencies.db_session import db_engine
from sqlmodel import Session, text
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
    query = text(f"""
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
        WHERE e.user_id = {user_id}
            AND e.equipment_type = 'coffee machine'
        ;
    """)
    with Session(db_engine) as session:
        result = session.exec(query)
    return {row.id: row.product for row in result}

def get_grinder_dict(user_id : int) -> dict:
    query = text(f"""
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
        WHERE e.user_id = {user_id}
            AND e.equipment_type = 'grinder'
        ;
    """)
    with Session(db_engine) as session:
        result = session.exec(query)
    return {row.id: row.product for row in result}

def get_portafilter_dict(user_id : int) -> dict:
    query = text(f"""
        SELECT 
            e.portafilter_id AS id,
            CONCAT(
                p.manufacturer, ' ', 
                p.model_name, ' ', 
                p.model_specification, ' ',
                p.basket_shot_size
                ) AS product
        FROM EquipmentOwnership AS e
        JOIN Portafilters AS p
        ON e.portafilter_id = p.id
        WHERE e.user_id = {user_id}
            AND e.equipment_type = 'portafilter'
        ;
    """)
    with Session(db_engine) as session:
        result = session.exec(query)
    return {row.id: row.product for row in result}

def get_purchase_dict(user_id : int, 
    time_frame : int = 30, max_items : int = 10) -> dict:
    date_threshold = date.today() - timedelta(days = time_frame)
    date_threshold = date_threshold.strftime("%Y-%m-%d")
    query = text(f"""
        SELECT p.id AS id, CONCAT(
            v.producer, ' ', v.name, 
            ', purchased on ', 
            DATE_FORMAT(p.purchase_date, '%Y-%m-%d')
            ) AS product
        FROM CoffeeBeanPurchases AS p
        JOIN CoffeeBeanVarieties AS v
        ON p.variety_id = v.id
        WHERE p.purchase_date >= {date_threshold}
            AND p.user_id = {user_id}
        ORDER BY p.purchase_date DESC
        LIMIT {max_items}
        ;
    """)
    with Session(db_engine) as session:
        result = session.exec(query)
    return {row.id: row.product for row in result}