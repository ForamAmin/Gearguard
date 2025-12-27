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


from sqlalchemy.orm import Session
from models import User, MaintenanceRequest, UserRole, TeamMember


def get_user_by_email(db: Session, email: str):
    # 1. Get user by email
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise Exception("User not found")

    # 2. EMPLOYEE → only own requests
    if user.role == UserRole.EMPLOYEE:
        requests = db.query(MaintenanceRequest).filter(
            MaintenanceRequest.created_by_id == user.id
        ).all()

    # 3. TECHNICIAN → assigned requests
    elif user.role == UserRole.TECHNICIAN:
        requests = db.query(MaintenanceRequest).filter(
            MaintenanceRequest.assigned_technician_id == user.id
        ).all()

    # 4. MANAGER → requests of their team
    elif user.role == UserRole.MANAGER:
        # Get all team IDs for this manager
        team_ids = (
            db.query(TeamMember.team_id)
            .filter(TeamMember.user_id == user.id)
            .all()
        )
        team_ids = [t[0] for t in team_ids]

        # Get all users in those teams
        user_ids = (
            db.query(User.id)
            .join(TeamMember, TeamMember.user_id == User.id)
            .filter(TeamMember.team_id.in_(team_ids))
            .all()
        )
        user_ids = [u[0] for u in user_ids]

        # Get requests created by those users
        requests = db.query(MaintenanceRequest).filter(
            MaintenanceRequest.created_by_id.in_(user_ids)
        ).all()

    else:
        requests = []

    return {
        "user": user,
        "requests": requests
    }
