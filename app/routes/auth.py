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

