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

def get_setup_dict(user_id : int) -> dict:
    query = text(f"""
        SELECT id, setup_name
        FROM EquipmentSetup
        WHERE user_id = {user_id}
        ORDER BY id DESC
        LIMIT 10
        ;
    """)
    with Session(db_engine) as session:
        result = session.exec(query)
    return {row.id: row.setup_name for row in result}

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