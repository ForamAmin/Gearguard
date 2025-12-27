from models import (
    User,
    Equipment,
    MaintenanceRequest,
    RequestStatus,
    RequestType,
    UserRole
)
from autofill import autofill_technician_for_request


def create_maintenance_request(
    db,
    employee_id: int,
    subject: str,
    equipment_id: int,
    request_type: RequestType,
    description: str = None,
    scheduled_date=None
):
    """
    Employee creates a maintenance request.
    """

    # 1️⃣ Validate employee
    employee = db.query(User).filter(User.id == employee_id).first()
    if not employee or employee.role != UserRole.EMPLOYEE:
        raise Exception("Only employees can create maintenance requests")

    # 2️⃣ Validate equipment
    equipment = db.query(Equipment).filter(
        Equipment.id == equipment_id
    ).first()

    if not equipment:
        raise Exception("Invalid equipment selected")

    # 3️⃣ Auto-fill technician
    technician_id = autofill_technician_for_request(db, equipment_id)

    # 4️⃣ Create request
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

    # 5️⃣ Save to DB
    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return new_request
from models import User, UserRole
from security import hash_password

def signup_user(
    db,
    name: str,
    email: str,
    password: str,
    role: UserRole,
    company_id: int
):
    """
    Registers a new user.
    """

    # Check if email already exists
    if db.query(User).filter(User.email == email).first():
        raise Exception("Email already registered")

    # Hash password BEFORE storing
    hashed_password = hash_password(password)

    # Create user
    user = User(
        name=name,
        email=email,
        password=hashed_password,
        role=role,
        company_id=company_id
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
from models import User
from security import verify_password

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