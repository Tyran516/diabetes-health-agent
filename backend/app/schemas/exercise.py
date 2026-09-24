from fastapi import status
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ExerciseBase(BaseModel):
    exercise_type: str
    duration_min: int
    intensity: Optional[str] = "中等"
    calories_burned: Optional[float] = None
    performed_at: datetime
    blood_sugar_before: Optional[float] = None
    blood_sugar_after: Optional[float] = None
    note: Optional[str] = None


class ExerciseCreate(ExerciseBase):
    patient_id: int


class ExerciseUpdate(ExerciseBase):
    exercise_type: Optional[str] = None
    duration_min: Optional[int] = None
    intensity: Optional[str] = None
    calories_burned: Optional[float] = None
    performed_at: Optional[datetime] = None
    blood_sugar_before: Optional[float] = None
    blood_sugar_after: Optional[float] = None
    note: Optional[str] = None


class ExerciseResponse(ExerciseBase):
    id: int
    patient_id: int
    bs_change: Optional[float] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
