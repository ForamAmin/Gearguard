from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

# Define Enums to match the DB (Frontend sends strings)
class RequestTypeEnum(str, Enum):
    CORRECTIVE = "Corrective"
    PREVENTIVE = "Preventive"

class RequestStatusEnum(str, Enum):
    NEW = "New"
    IN_PROGRESS = "In Progress"
    REPAIRED = "Repaired"
    SCRAP = "Scrap"

# --- 1. AUTO-FILL RESPONSE ---
# All for employees to see equipment and its team
class EquipmentInfo(BaseModel):
    id: int
    name: str
    serial_number: str
    location: str
    team_name: str  # We will fetch this from the relationship via Equipment -> MaintenanceTeam
    team_id: int

# --- 2. CREATE REQUEST INPUT ---
#For both managers and employees
class RequestCreate(BaseModel):
    equipment_id: int
    created_by_id: int          # Changed from 'created_by'
    request_type: RequestTypeEnum
    subject: str
    description: Optional[str] = None
    scheduled_date: Optional[datetime] = None

# --- 3. RESPONSE AFTER SAVING ---
#showing after creating a request
class RequestResponse(BaseModel):
    id: int
    status: str
    message: str