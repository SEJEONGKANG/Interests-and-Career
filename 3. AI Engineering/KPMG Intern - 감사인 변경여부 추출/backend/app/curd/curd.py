from sqlalchemy.orm      import Session
from app.database.models import Report, Corp

def get_latest_info(db: Session, corp_code: str):
    """각 기업의 감사인 변경여부 정보가 담긴 가장 최신 보고서에서 정보 추출하는 함수.

    Args:
        db : 데이터베이스 세션.
        corp_code : 기업 코드.

    Returns:
        response_data (dict) : 기업 정보 및 보고서에서 추출한 감사 관련 정보가 담긴 딕셔너리.
    """
    corp = db.query(Corp).filter(Corp.corp_code == corp_code).first()
    if not corp:
        return {"exist": False}

    latest_report = db.query(Report).filter(Report.corp_code == corp.corp_code)\
                        .filter(Report.is_changed.in_(['변경안됨', '변경됨', '신규']))\
                        .filter(Report.report_nm.not_like("%기재정정%"))\
                        .order_by(Report.rcept_dt.desc()).first()
    if not latest_report:
        return {"exist": False, "data": {"corp_code":corp_code, "corp_name":corp.corp_name}}

    auditor_in_heads_list = []
    if latest_report.auditor_in_heads:
        auditor_in_heads_list = latest_report.auditor_in_heads.split("\\")
        auditor_in_heads_list = [item for item in auditor_in_heads_list if item]

    response_data = {
        "exist": True,
        "data": {
            "corp_code"                   : corp.corp_code,
            "corp_name"                   : corp.corp_name,
            "stock_code"                  : corp.stock_code,
            "corp_cls"                    : corp.corp_cls,
            "flr_nm"                      : corp.flr_nm,
            "rm"                          : corp.rm,
            "rcept_no"                    : latest_report.rcept_no,
            "report_nm"                   : latest_report.report_nm,
            "rcept_dt"                    : latest_report.rcept_dt,
            "is_changed"                  : latest_report.is_changed,
            "auditor_now"                 : latest_report.auditor_now,
            "auditor_prior"               : latest_report.auditor_prior,
            "auditor_two_years_ago"       : latest_report.auditor_two_years_ago,
            "auditor_payed"               : latest_report.auditor_payed,
            "audit_contents"              : latest_report.audit_contents,
            "earnings_actual"             : latest_report.earnings_actual,
            "worktime_actual"             : latest_report.worktime_actual,
            "earnings_contract"           : latest_report.earnings_contract,
            "worktime_contract"           : latest_report.worktime_contract,
            "unit"                        : latest_report.unit,
            "earnings_actual_unit"        : latest_report.earnings_actual_unit,
            "earnings_contract_unit"      : latest_report.earnings_contract_unit,
            "is_audit_currently_assigned" : latest_report.is_audit_currently_assigned,
            "description"                 : latest_report.description,
            "auditor_in_heads"            : auditor_in_heads_list,
            "xml_content"                 : f"https://dart.fss.or.kr/dsaf001/main.do?rcpNo={latest_report.rcept_no}" if latest_report.xml_content else None
        }
    }
    return response_data