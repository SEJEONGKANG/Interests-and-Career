from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import UserInterest
from app.database.schemas import StarredStatusChangeResponse, CorpInfoResponse
from app.curd.curd import get_latest_info
from typing import List

router = APIRouter()

# 사용자 즐겨찾기 목록 변경 엔드포인트
@router.post("/change_starred_status", response_model=StarredStatusChangeResponse, summary="즐겨찾기 목록 변경")
def change_starred_status_endpoint(user_id: str, corp_code: str, db: Session = Depends(get_db)):
    """
    사용자 관심 기업의 즐겨찾기 목록을 변경합니다.

    - **user_id**  : 사용자 식별자.
    - **corp_code**: 기업 코드.
    - **db**       : SQLAlchemy 세션.
    
    Returns:
    - 즐겨찾기 목록 변경 성공/에러 메시지 딕셔너리.

    '즐겨찾기 기업 확인' 서비스에 활용.
    """
    try:
        user_interest = db.query(UserInterest).filter_by(user_id=user_id, corp_code=corp_code).first()
        if user_interest:
            db.delete(user_interest)
        else:
            new_user_interest = UserInterest(user_id=user_id, corp_code=corp_code)
            db.add(new_user_interest)
        db.commit()
        return {"message": "즐겨찾기 목록이 성공적으로 변경되었습니다."}
    except Exception as e:
        db.rollback() 
        return {"message": f"에러 발생: {str(e)}"}
    
  
# 사용자 관심 기업 정보 엔드포인트
@router.post("/starred_corp_info_total", response_model=List[CorpInfoResponse], summary="즐겨찾기 기업 정보")
def starred_corp_info_total_endpoint(user_id: str, db: Session = Depends(get_db)):
    """
    즐겨찾기에 등록된 기업들의 정보를 반환합니다.

    - **user_id**: 사용자 식별자.
    - **db**     : SQLAlchemy 세션.

    Returns:
    - 기업 정보가 담긴 딕셔너리의 리스트.
      - corp_code                   : 기업 코드
      - corp_name                   : 기업명
      - stock_code                  : 종목번호
      - corp_cls                    : 기업구분
      - flr_nm                      : 공시 제출인명
      - rm                          : 비고
      - rcept_no                    : 접수번호
      - report_nm                   : 보고서명
      - rcept_dt                    : 접수일자
      - is_changed                  : 감사인 변경여부
      - auditor_now                 : 당기 감사인
      - auditor_prior               : 전기 감사인
      - auditor_two_years_ago       : 전전기 감사인
      - auditor_payed               : 보수를 받은 감사인
      - audit_contents              : 감사내용
      - earnings_actual             : 실제 감사보수
      - worktime_actual             : 실제 감사시간
      - earnings_contract           : 계약 감사보수
      - worktime_contract           : 계약 감사시간
      - unit                        : 보수/시간의 단위
      - earnings_actual_unit        : 단위가 고려된 실제 감사보수
      - earnings_contract_unit      : 단위가 고려된 계약 감사보수
      - is_audit_currently_assigned : 지정감사 여부
      - description                 : 회계감사인의 변동 부분 원문
      - auditor_in_heads (List[str]): 보고서 내 감사인이 담긴 모든 표
      - xml_content                 : 보고서 원문 링크


    '즐겨찾기 기업 확인' 서비스에 활용.
    """

    user_interest = db.query(UserInterest).filter_by(user_id=user_id).all()
    if not user_interest:
        return []
    corp_info_list = [get_latest_info(db, interest.corp_code)['data'] for interest in user_interest]
    return corp_info_list
