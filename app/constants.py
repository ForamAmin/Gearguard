from enum import Enum

class RequestStage(str, Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    REPAIRED = "REPAIRED"
    SCRAP = "SCRAP"

class RequestType(str, Enum):
    CORRECTIVE = "CORRECTIVE"
    PREVENTIVE = "PREVENTIVE"

class UserRole(str, Enum):
    USER = "USER"
    TECHNICIAN = "TECHNICIAN"
    MANAGER = "MANAGER"
