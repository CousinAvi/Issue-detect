from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    LargeBinary,
    Enum,
    ForeignKey,
    Table,
    DateTime,
    Numeric,
)

from sqlalchemy.orm import relationship


from sqlalchemy.sql import func

from . import Base

import enum


class Organization(Base):
    __tablename__ = "organizations"
    reg_number = Column(Integer, primary_key=True)
    name = Column(String)


class OrganizationPortal(Base):
    __tablename__ = "organizations_portals"

    id = Column(Integer, primary_key=True)
    organization_number = Column(Integer, ForeignKey("organizations.reg_number"))
    address = Column(String, unique=True)


class OrganizationPortalWithOrganization(OrganizationPortal):
    organization = relationship("OrganizationWithPortals", back_populates="portals")


class OrganizationWithPortals(Organization):
    portals = relationship(
        "OrganizationPortalWithOrganization", back_populates="organization"
    )


class MlEvent(Base):
    __tablename__ = "ml_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company = Column(String)
    comment = Column(String)
    service = Column(String)
    reason = Column(String)
    timestampe = Column(DateTime, server_default=func.now())