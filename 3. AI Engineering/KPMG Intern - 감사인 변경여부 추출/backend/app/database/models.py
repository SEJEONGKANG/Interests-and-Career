from sqlalchemy import Column, ForeignKey, Integer, String, Text, LargeBinary, Index, BigInteger
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import relationship
from app.database.session import Base

class Corp(Base):
    __tablename__ = "corp"
    corp_code  = Column(String(8),   primary_key = True, index=True)
    corp_name  = Column(String(255), nullable    = True, index=True)
    stock_code = Column(String(10) , nullable    = True)
    corp_cls   = Column(String(10) , nullable    = True)
    flr_nm     = Column(String(255), nullable    = True)
    rm         = Column(String(255), nullable    = True)
    
    reports = relationship("Report", back_populates="corp")
    assigned = relationship("Assigned", back_populates="corp")
    user_interests = relationship("UserInterest", back_populates="corp")

class Report(Base):
    __tablename__ = "report"
    rcept_no                    = Column(String(14),  primary_key = True,           index=True)
    report_nm                   = Column(String(255), nullable    = True)
    rcept_dt                    = Column(Integer,     nullable    = True)
    corp_code                   = Column(String(8),   ForeignKey("corp.corp_code"), index=True)
    is_changed                  = Column(String(255), nullable    = True)
    auditor_now                 = Column(String(255), nullable    = True)
    auditor_prior               = Column(String(255), nullable    = True)
    auditor_two_years_ago       = Column(String(255), nullable    = True)
    auditor_payed               = Column(String(255), nullable    = True)
    audit_contents              = Column(LONGTEXT,    nullable    = True)
    earnings_actual             = Column(String(255), nullable    = True)
    worktime_actual             = Column(String(255), nullable    = True)
    earnings_contract           = Column(String(255), nullable    = True)
    worktime_contract           = Column(String(255), nullable    = True)
    unit                        = Column(LONGTEXT,    nullable    = True)
    earnings_actual_unit        = Column(BigInteger,  nullable    = True)
    earnings_contract_unit      = Column(BigInteger,  nullable    = True)
    auditor_in_heads            = Column(LONGTEXT,    nullable    = True)
    xml_content                 = Column(LargeBinary(length=(2**32)-1), nullable    = True)
    is_audit_currently_assigned = Column(String(255), nullable    = True)
    description                 = Column(LONGTEXT,        nullable    = True)

    corp = relationship("Corp", back_populates="reports", cascade="all")

class User(Base):
    __tablename__ = "user"
    user_id   = Column(String(255), primary_key = True, index=True)
    password  = Column(String(255)                                )

    user_interests = relationship("UserInterest", back_populates="user")

class UserInterest(Base):
    __tablename__ = "user_interest"
    user_id     = Column(String(255), ForeignKey("user.user_id"),   primary_key = True, index=True)
    corp_code   = Column(String(255), ForeignKey("corp.corp_code"), primary_key = True, index=True)
    __table_args__ = (Index("ix_user_interest_user_id_corp_code", "user_id", "corp_code"),)

    user = relationship("User", back_populates="user_interests")
    corp = relationship("Corp", back_populates="user_interests")

class Assigned(Base):
    __tablename__ = "assigned"
    corp_code     = Column(String(255), ForeignKey("corp.corp_code"), primary_key = True, index=True )
    assigned_year = Column(Integer,                                   primary_key = True, index=True )
    description   = Column(Text,                                      nullable    = True)
    __table_args__ = (Index("ix_assigned_corp_code_assigned_year", "corp_code", "assigned_year"),)

    corp = relationship("Corp", back_populates="assigned")