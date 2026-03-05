from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.curd.curd import get_latest_info
from app.database.session import get_db
from app.database.models import Corp, Report
from app.database.schemas import CorpBasicInfo, CorpInfoResponseExist
from typing import List
from datetime import datetime
import pandas as pd
import io

router = APIRouter()

@router.get("/cur_corp_list", response_model=List[CorpBasicInfo], summary="현재 기업 목록 반환")
def get_cur_corp_list_endpoint(db: Session = Depends(get_db)):
    """
    현재 등록된 모든 기업의 기본 정보를 반환합니다.

    Returns:
    - 현재 기업 목록의 기본 정보 딕셔너리의 리스트.
      - **corp_code**: 기업 코드.
      - **corp_name**: 기업명.

    '기업별 검색' 서비스에 활용.
    """

    corp_list = db.query(Corp.corp_code, Corp.corp_name).all()
    response_data = [CorpBasicInfo(corp_code=corp_code, corp_name=corp_name) for corp_code, corp_name in corp_list]
    return response_data


@router.post("/get_latest_info", response_model=CorpInfoResponseExist, summary="최신 정보 반환")
def get_latest_info_endpoint(corp_code: str, db: Session = Depends(get_db)):
    """
    특정 기업의 최신 정보를 반환합니다.

    Args:
    - **corp_code**: 기업 코드.

    Returns:
    - 정보 유무와 정보를 담은 딕셔너리

    - **exist**: 선택한 기업의 정보 유무 Bool.

    - **data**: 기업의 최신 정보 딕셔너리.
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

    '기업별 검색' 서비스에 활용.
    """

    result = get_latest_info(db, corp_code)
    return result

@router.post("/select_info_total", response_model=List[CorpInfoResponseExist], summary="정보 선택 조회")
def select_info_total_endpoint(corp_code_list : List[str], db: Session = Depends(get_db)):
    """
    여러 기업의 정보를 선택하여 조회합니다.

    Args:
    - 기업 코드(문자열) 리스트.

    Returns:
    - 선택한 기업들의 정보(exist, data) 딕셔너리가 담긴 리스트.
    - **exist**: 선택한 기업의 정보 유무 Bool.
    - **data** : 기업의 최신 정보 딕셔너리.
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


    '기업별 검색' 서비스에 활용.
    """

    corp_info_list = [get_latest_info(db, corp_code) for corp_code in corp_code_list]
    return corp_info_list

@router.get("/get_this_year_info", response_model=List[CorpInfoResponseExist], summary="올해 정보 반환")
def get_this_year_info(db: Session = Depends(get_db)):
    """
    올해 보고서 정보를 반환합니다.

    Returns:
    - 올해 공시된 보고서 정보(exist, data)가 담긴 딕셔너리의 리스트.
    - **exist**: 선택한 기업의 정보 유무 Bool.
    - **data** : 기업의 최신 정보 딕셔너리.
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


    '올해 보고서 조회' 서비스에 활용.
    """

    current_year = datetime.now().year
    this_year_reports = db.query(Report).filter(Report.report_nm.like(f"%{current_year}%")).all()
    corp_code_list = {report.corp_code for report in this_year_reports}
    corp_info_list = [get_latest_info(db, corp_code) for corp_code in corp_code_list]
    return corp_info_list

@router.get("/download_csv", summary="Excel 다운로드")
def download_csv(db: Session = Depends(get_db)):
    """
    최근 보고서 정보를 Excel 파일로 다운로드합니다.

    Returns:
    - 다운로드할 Excel 파일 응답 객체.

    '올해 보고서 조회' 서비스에 활용.
    """

    current_year = datetime.now().year
    this_year_reports = db.query(Report).filter(Report.report_nm.like(f"%{current_year}%")).all()
    corp_code_list = [report.corp_code for report in this_year_reports]
    corp_info_list = [get_latest_info(db, corp_code)["data"] for corp_code in corp_code_list]
    cleaned_corps  = [{key: value for key, value in row.items() if key != "auditor_in_heads"} for row in corp_info_list]
    corp_df = pd.DataFrame(cleaned_corps)
    
    excel_output = io.BytesIO()
    excel_writer = pd.ExcelWriter(excel_output, engine="xlsxwriter")
    corp_df.to_excel(excel_writer, index=False, columns=corp_df.columns[1:])
    excel_writer.close() 

    excel_output.seek(0)
    response = Response(content=excel_output.read())
    response.headers["Content-Disposition"] = "attachment; filename=recent_auditors.xlsx"
    response.headers["Content-Type"]        = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    return response