from __future__ import annotations

import datetime
from typing import Optional, List
from pydantic import BaseModel


class Portal(BaseModel):
    id: int
    organization_number: int
    address: str

    class Config:
        orm_mode = True


class Organization(BaseModel):
    reg_number: int
    name: str
    portals: Optional[List[Portal]]

    class Config:
        orm_mode = True


class MlEvent(BaseModel):
    company: str
    service: Optional[str] = "Нет данных"
    reason: Optional[str] = "Нет данных"
    comment: str

    class Config:
        orm_mode = True

class Log(BaseModel):
    bank_name: str
    url: str
    log: str
    timestamp: datetime.datetime

    class Config:
        orm_mode = True
