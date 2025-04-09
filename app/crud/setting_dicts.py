from ..dependencies.db_session import db_engine
from sqlmodel import Session, text

def get_default_setup(user_id : int) -> dict:
    query = text(f"""
        SELECT 
            e.coffee_machine_id AS machine_id,
            e.grinder_id AS grinder_id,
            e.portafilter_id AS portafilter_id,
            e.wdt_used AS wdt_used,
            e.tamping_method AS tamping_method,
            e.tamping_weight_kg AS tamping_weight_kg,
            e.leveler_used AS leveler_used,
            e.puck_screen_used AS puck_screen_used,
            e.puck_screen_thickness_mm AS puck_screen_thickness_mm
        FROM UserSettings AS u
        JOIN EquipmentSetup AS e
        ON u.default_setup_id = e.id
        WHERE u.user_id = {user_id}
        """)
    with Session(db_engine) as session:
        result = session.exec(query).one()
    
    return {
        "machine_id" : result.machine_id,
        "grinder_id" : result.grinder_id,
        "portafilter_id" : result.portafilter_id,
        "wdt_used" : result.wdt_used,
        "tamping_method" : result.tamping_method,
        "tamping_weight_kg" : result.tamping_weight_kg,
        "leveler_used" : result.leveler_used,
        "puck_screen_used" : result.puck_screen_used,
        "puck_screen_thickness_mm" : result.puck_screen_thickness_mm
    }