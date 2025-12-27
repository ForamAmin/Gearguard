from models import (
    User,
    Equipment,
    MaintenanceRequest,
    RequestStatus,
    RequestType,
    UserRole
)
from services.autofill import autofill_maintenance_team
from models import User, UserRole 
from security import hash_password
from security import verify_password

def create_maintenance_request(
    db,
    employee_id: int,
    subject: str,
    equipment_id: int,
    request_type: RequestType,
    description: str = None,
    scheduled_date=None
):
    employee = db.query(User).filter(User.id == employee_id).first()
    if not employee or employee.role != UserRole.EMPLOYEE:
        raise Exception("Only employees can create maintenance requests")

    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not equipment:
        raise Exception("Invalid equipment")

    technician_id = autofill_maintenance_team(db,equipment_id)

    new_request = MaintenanceRequest(
        subject=subject,
        description=description,
        equipment_id=equipment_id,
        created_by_id=employee_id,
        assigned_technician_id=technician_id,
        request_type=request_type,
        status=RequestStatus.NEW,
        scheduled_date=scheduled_date
    )

    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return new_request


def signup_user(db, name: str, email: str, password: str, role: UserRole):
    if db.query(User).filter(User.email == email).first():
        raise Exception("Email already registered")

    hashed_password = hash_password(password)

    user = User(
        name=name,
        email=email,
        password=hashed_password,
        role=role
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def login_user(
    db,
    email: str,
    password: str
):
    """
    Authenticates an existing user.
    """

    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password):
        raise Exception("Invalid email or password")

    return user