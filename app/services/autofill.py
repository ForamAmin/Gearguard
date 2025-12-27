from sqlalchemy.orm import Session
from models import Equipment, MaintenanceTeam, TeamMember, User


def autofill_maintenance_team(db: Session,equipment_id: int):
    """
    Returns the maintenance team ID assigned to the given equipment.
    """

    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()

    if not equipment:
        raise ValueError("Equipment not found")

    if not equipment.maintenance_team:
        raise ValueError("No maintenance team assigned to this equipment")

    return equipment.maintenance_team.id