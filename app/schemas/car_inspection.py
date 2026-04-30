from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CarInspectionSchema(BaseModel):
    fullName: str
    phoneNumber: str
    carName: str
    carModel: str
    chassisNumber: str
    plateNumber: str
    inspectionDate: datetime
    expertDescription: Optional[str] = None

    frontBumper: Optional[bool] = None
    hood: Optional[bool] = None
    frontRightFender: Optional[bool] = None
    frontRightDoor: Optional[bool] = None
    rearRightDoor: Optional[bool] = None
    rearRightFender: Optional[bool] = None
    trunk: Optional[bool] = None
    rearLeftFender: Optional[bool] = None
    rearLeftDoor: Optional[bool] = None
    frontLeftDoor: Optional[bool] = None
    frontLeftFender: Optional[bool] = None
    roof: Optional[bool] = None
    rearBumper: Optional[bool] = None
    chassis: Optional[bool] = None
