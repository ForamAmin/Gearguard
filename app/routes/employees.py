from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from datetime import datetime

router = APIRouter()

# --- ENDPOINT 1: AUTO-FILL DATA ---
# Logic: Find the Equipment -> Find the Team -> Return Team Name
@router.get("/equipment/{id}/autofill", response_model=schemas.EquipmentInfo)
def get_autofill_data(id: int, db: Session = Depends(get_db)):
    # 1. Get Equipment with the Team relationship
    equip = db.query(models.Equipment).filter(models.Equipment.id == id).first()
    
    if not equip:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    # 2. Handle missing team gracefully (Prevent crash if team is None)
    team_name = "Unassigned"
    team_id = 0
    if equip.maintenance_team:
        team_name = equip.maintenance_team.name
        team_id = equip.maintenance_team.id

    return {
        "id": equip.id,
        "name": equip.name,
        "serial_number": equip.serial_number or "N/A",
        "location": equip.location or "Unknown",
        "team_name": team_name,
        "team_id": team_id
    }

# --- ENDPOINT 2: CREATE REQUEST ---
# Logic: Save using the Enums and new column names
@router.post("/create", response_model=schemas.RequestResponse)
def create_request(data: schemas.RequestCreate, db: Session = Depends(get_db)):
    
    # 1. Create the DB Object
    new_request = models.MaintenanceRequest(
        subject=data.subject,
        description=data.description,
        equipment_id=data.equipment_id,
        created_by_id=data.created_by_id,  # Matches new column
        request_type=models.RequestType(data.request_type), # Convert str to Enum
        status=models.RequestStatus.NEW,    # Default to NEW
        scheduled_date=data.scheduled_date,
        created_at=datetime.utcnow()
    )

    # 2. Commit
    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return {
        "id": new_request.id,
        "status": new_request.status.value, # Extract string from Enum
        "message": "Request created successfully"
    }