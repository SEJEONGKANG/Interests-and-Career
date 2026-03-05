from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import Assigned, Corp
from app.database.schemas import ContactListResponse
from app.curd.curd import get_latest_info
import datetime

router = APIRouter()

# 잠재적 고객의 목록을 보여주는 엔드포인트
@router.get("/show_contact_list", response_model=ContactListResponse, summary="잠재 고객 리스트")
def show_contact_list_endpoint(db: Session = Depends(get_db)):
    """
    올해 지정감사가 종료되어 영업 대상인 기업 목록을 추출합니다.

    - **db**: SQLAlchemy Session
        데이터베이스 세션.

    Returns:
    - **data**: 기업 정보가 포함된 딕셔너리의 리스트.
      - corp_code: 기업 코드.
      - corp_name: 기업명.
      - auditor  : 최근 3년간 지정감사를 수행한 법인명.
    
    - **auditor_list**: 검색된 데이터로부터 얻은 고유한 감사인 목록 문자열 리스트.

    '잠재 고객 검색' 서비스에 활용.
    """

    current_year = datetime.datetime.now().year
    last_year = current_year - 1
    prev_year = current_year - 2
    prev_prev_year = current_year - 3

    assigned_last_year = (db.query(Assigned.corp_code).filter(Assigned.assigned_year == last_year).subquery())
    assigned_prev_year = (db.query(Assigned.corp_code).filter(Assigned.assigned_year == prev_year).subquery())
    assigned_prev_prev_year = (db.query(Assigned.corp_code).filter(Assigned.assigned_year == prev_prev_year).subquery())

    contact_target = (
        db.query(assigned_last_year.c.corp_code, Corp.corp_name)
        .join(Corp, assigned_last_year.c.corp_code == Corp.corp_code)
        .filter(assigned_last_year.c.corp_code.in_(assigned_prev_year))
        .filter(~assigned_last_year.c.corp_code.in_(assigned_prev_prev_year))
        .all()
    )

    contact_list = {"data":[{"corp_code": corp_code, "corp_name": corp_name, "auditor": get_latest_info(db, corp_code)['data']['auditor_now']} for corp_code, corp_name in contact_target],}
    contact_list["auditor_list"] = list(set([corp['auditor'] for corp in contact_list['data']]))
    return contact_list
