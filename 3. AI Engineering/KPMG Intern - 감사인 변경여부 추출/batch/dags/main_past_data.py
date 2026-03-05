from get_yesterday_data import make_update_target, get_xml, write_result_csv
from tqdm.auto import tqdm
import pandas as pd
import re
import warnings
warnings.filterwarnings('ignore')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Text, LargeBinary, Index, BigInteger
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import relationship

db_connection_url = 'mysql+pymysql://root:password@localhost:3306/sr'
db_engine = create_engine(db_connection_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

Base = declarative_base()

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
    audit_contents              = Column(LONGTEXT,        nullable    = True)
    earnings_actual             = Column(String(255), nullable    = True)
    worktime_actual             = Column(String(255), nullable    = True)
    earnings_contract           = Column(String(255), nullable    = True)
    worktime_contract           = Column(String(255), nullable    = True)
    unit                        = Column(LONGTEXT,        nullable    = True)
    earnings_actual_unit        = Column(BigInteger,  nullable    = True)
    earnings_contract_unit      = Column(BigInteger,  nullable    = True)
    auditor_in_heads            = Column(LONGTEXT,        nullable    = True)
    xml_content                 = Column(LargeBinary(length=(2**32)-1), nullable    = True)
    is_audit_currently_assigned = Column(String(255), nullable    = True)
    description                 = Column(LONGTEXT,        nullable    = True)

    corp = relationship("Corp", back_populates="reports", cascade="all")

class Assigned(Base):
    __tablename__ = "assigned"
    corp_code     = Column(String(255), ForeignKey("corp.corp_code"), primary_key = True, index=True )
    assigned_year = Column(Integer,                                   primary_key = True, index=True )
    description   = Column(Text,                                      nullable    = True)
    __table_args__ = (Index("ix_assigned_corp_code_assigned_year", "corp_code", "assigned_year"),)

    corp = relationship("Corp", back_populates="assigned")

def push_corp_to_db(df: pd.DataFrame, session: Session):
    """기업 관련 정보를 corp 테이블에 적재"""
    for _, row in df.iterrows():
        corp = Corp(**row)
        try:
            session.merge(corp)
            session.commit()
        except IntegrityError:
            session.rollback()

def extract_assigned_year(report_nm: str):
    """보고서명으로부터 해당 연도 추출"""
    year = report_nm.split('(')[-1].split(')')[0].split('.')[0]
    return int(year)

def push_report_to_db(df: pd.DataFrame, session: Session):
    """보고서 관련 정보를 report 테이블에 적재"""
    for _, row in df.iterrows():
        report = Report(**row)
        try:
            session.add(report)
            session.commit()
        except IntegrityError:  # primary key 가 이미 있는 경우
            session.rollback()

def run(startday:int, endday:int, api_key:str):
    """원하는 기간에 공시된 보고서로부터 정보를 추출하여 DB에 적재하는 전체 코드를 실행시키는 함수"""
    Session = sessionmaker(bind=db_engine)
    session = Session()

    update_target = make_update_target(str(startday),str(endday))

    xml_data = []
    for i in tqdm(range(len(update_target))):
        rcept_no = update_target['rcept_no'][i]
        try:
            xml_content = get_xml(rcept_no, api_key)
            xml_data.append((rcept_no, re.sub('\n', '\r', xml_content[0]), xml_content[1]))
        except:
            xml_data.append((rcept_no, None, None))
    xml_df = pd.DataFrame(xml_data, columns=['rcept_no', 'xml_content', 'xml_content_byte'])

    result = write_result_csv(update_target, xml_df)
    corps_result = result[['corp_code', 'corp_name', 'stock_code', 'corp_cls', 'flr_nm', 'rm']]
    reports_result = result[['report_nm', 'rcept_no', 'rcept_dt', 'corp_code', 'is_changed', 'auditor_now', 'auditor_prior', 'auditor_two_years_ago', 'auditor_payed', 'audit_contents', 'earnings_actual', 'worktime_actual', 'earnings_contract', 'worktime_contract', 'unit', 'earnings_actual_unit', 'earnings_contract_unit', 'auditor_in_heads', 'xml_content', 'is_audit_currently_assigned', 'description']]

    push_corp_to_db(corps_result, session)
    print(f"{startday}~{endday} corp table update 완료")

    push_report_to_db(reports_result, session)
    print(f"{startday}~{endday} report table update 완료")

    session.close()

# 원하는 기간의 시작 일자, 마지막 일자 기입
run(20230101, 20230331, 'your_opendart_api_key')
