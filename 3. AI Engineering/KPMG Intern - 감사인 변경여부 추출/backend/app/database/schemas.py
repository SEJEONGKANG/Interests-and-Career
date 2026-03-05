from pydantic import BaseModel, AnyUrl
from typing import List, Optional

class CorpBase(BaseModel):
    corp_code   : str
    corp_name   : Optional[str] = None
    stock_code  : Optional[str] = None
    corp_cls    : Optional[str] = None
    flr_nm      : Optional[str] = None
    rm          : Optional[str] = None

class Corp(CorpBase):
    reports: List["Report"] = []  # Report instances 리스트

    class Config:
        orm_mode = True           # dict 아니어도 data 읽을 수 있음 (corp['reports'] 대신 corp.reports 가능)

class ReportBase(BaseModel):
    rcept_n                     : str
    report_n                    : Optional[str]   = None
    rcept_dt                    : Optional[int]   = None
    corp_code                   : str
    is_changed                  : Optional[str]   = None
    auditor_now                 : Optional[str]   = None
    auditor_prior               : Optional[str]   = None
    auditor_two_years_ago       : Optional[str]   = None
    auditor_payed               : Optional[str]   = None
    audit_contents              : Optional[str]   = None
    earnings_actual             : Optional[str]   = None
    worktime_actual             : Optional[str]   = None
    earnings_contract           : Optional[str]   = None
    worktime_contract           : Optional[str]   = None
    unit                        : Optional[str]   = None
    earnings_actual_unit        : Optional[int]   = None
    earnings_contract_unit      : Optional[int]   = None
    auditor_in_heads            : Optional[str]   = None
    xml_content                 : Optional[bytes] = None
    is_audit_currently_assigned : Optional[str]   = None
    description                 : Optional[str]   = None


class Report(ReportBase):
    corp: Corp

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    user_id: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    user_interests: List["UserInterest"] = [] 

    class Config:
        orm_mode = True

class UserInterestBase(BaseModel):
    user_id  : str
    corp_code: str

class UserInterest(UserInterestBase):
    user: User  
    corp: Corp  

    class Config:
        orm_mode = True

class AssignedBase(BaseModel):
    corp_code    : str
    assigned_year: int


class Assigned(AssignedBase):
    corp: Corp 

    class Config:
        orm_mode = True


class EarningTimeStatsResponse(BaseModel):
    auditor: str
    year   : str
    avgCost: float
    totCost: float
    avgTime: float
    totTime: int
    count  : int

class CorpContactInfoResponse(BaseModel):
    corp_code: str
    corp_name: str
    auditor  : str


class ContactListResponse(BaseModel):
    data        : List[CorpContactInfoResponse]
    auditor_list: List[str]

class CorpBasicInfo(BaseModel):
    corp_code: str
    corp_name: str

class StarredStatusChangeResponse(BaseModel):
    message: str

class CorpInfoResponse(BaseModel):
    corp_code                   : str
    corp_name                   : str
    stock_code                  : str
    corp_cls                    : str
    flr_nm                      : str
    rm                          : str
    rcept_no                    : str
    report_nm                   : str
    rcept_dt                    : int
    is_changed                  : str
    auditor_now                 : str
    auditor_prior               : str
    auditor_two_years_ago       : str
    auditor_payed               : str
    audit_contents              : str
    earnings_actual             : str
    worktime_actual             : str
    earnings_contract           : str
    worktime_contract           : str
    unit                        : str
    earnings_actual_unit        : int
    earnings_contract_unit      : int
    is_audit_currently_assigned : str
    description                 : str
    auditor_in_heads            : List[str]
    xml_content                 : AnyUrl

class CorpInfoResponseExist(BaseModel):
    exist: bool
    data : CorpInfoResponse
    
class StarredCorpInfo(BaseModel):
    corp_code: str
    corp_name: str

class LoginResponse(BaseModel):
    log_in : bool
    starred: List[StarredCorpInfo]