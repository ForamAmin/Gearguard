from sqlalchemy import Column, Integer, String, DateTime,ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import enum

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    base_currency = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    users = relationship("User", back_populates="company")
    equipment = relationship("Equipment", back_populates="company")


class UserRole(enum.Enum):
    EMPLOYEE = "employee"
    MANAGER = "manager"
    TECHNICIAN = "technician"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(Enum(UserRole), nullable=False)

    company_id = Column(Integer, ForeignKey("companies.id"))

    company = relationship("Company", back_populates="users")

    # Relationships
    assigned_requests = relationship("MaintenanceRequest", back_populates="technician")
    created_requests = relationship("MaintenanceRequest", back_populates="created_by")

class MaintenanceTeam(Base):
    __tablename__ = "maintenance_teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    members = relationship("TeamMember", back_populates="team")
    equipment = relationship("Equipment", back_populates="maintenance_team")

class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey("maintenance_teams.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    team = relationship("MaintenanceTeam", back_populates="members")
    user = relationship("User")

class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    serial_number = Column(String, unique=True)
    location = Column(String)
    purchase_date = Column(DateTime)
    warranty_expiry = Column(DateTime)

    company_id = Column(Integer, ForeignKey("companies.id"))
    maintenance_team_id = Column(Integer, ForeignKey("maintenance_teams.id"))

    company = relationship("Company", back_populates="equipment")
    maintenance_team = relationship("MaintenanceTeam", back_populates="equipment")

    maintenance_requests = relationship("MaintenanceRequest", back_populates="equipment")

from sqlalchemy import DateTime, Text, Enum
import enum

class RequestStatus(enum.Enum):
    NEW = "New"
    IN_PROGRESS = "In Progress"
    REPAIRED = "Repaired"
    SCRAP = "Scrap"

class RequestType(enum.Enum):
    CORRECTIVE = "Corrective"
    PREVENTIVE = "Preventive"

class MaintenanceRequest(Base):
    __tablename__ = "maintenance_requests"

    id = Column(Integer, primary_key=True)
    subject = Column(String, nullable=False)
    description = Column(Text)

    equipment_id = Column(Integer, ForeignKey("equipment.id"))
    created_by_id = Column(Integer, ForeignKey("users.id"))
    assigned_technician_id = Column(Integer, ForeignKey("users.id"))

    request_type = Column(Enum(RequestType))
    status = Column(Enum(RequestStatus), default=RequestStatus.NEW)

    scheduled_date = Column(DateTime)
    duration_hours = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)

    equipment = relationship("Equipment", back_populates="maintenance_requests")
    created_by = relationship("User", foreign_keys=[created_by_id])
    technician = relationship("User", foreign_keys=[assigned_technician_id])
