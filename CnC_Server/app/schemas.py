from __future__ import annotations
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
    service: str
    reason: str
    comment: str
