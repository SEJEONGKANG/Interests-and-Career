from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import Report
from app.database.schemas import EarningTimeStatsResponse
from typing import List
import re
router = APIRouter()

def extract_numeric(s):
    if s in ('', '-'):
        return 0
    else:
        return int(re.sub(r'\D', '', s))

# 수익 및 작업시간 통계를 계산하는 엔드포인트
@router.get("/earning_time_count", response_model=List[EarningTimeStatsResponse], summary="수익 및 작업시간 통계 계산")
def earning_time_count_endpoint(db: Session = Depends(get_db)):
    """
    서로 다른 감사인 및 연도에 대한 수익 및 작업시간 통계를 계산합니다.

    - **db**: SQLAlchemy 세션
        데이터베이스 세션.

    Returns:
    - 각 계산된 통계를 포함하는 딕셔너리의 리스트:
      - **auditor**: 감사인 이름.
      - **year**   : 계산된 연도.
      - **avgCost**: 평균 수익 실제 단위 비용.
      - **totCost**: 총 수익 실제 단위 비용.
      - **avgTime**: 평균 작업시간 실제.
      - **totTime**: 총 작업시간 실제.
      - **count**  : 보고서 수.

    '기업 현황 분석' 서비스에 활용.
    """

    result = []
    auditor_list = db.query(Report.auditor_now.distinct()).all()
    years = ['2022'] #['2022', '2021', '2020']
    for auditor in auditor_list:
        auditor = auditor[0]
        for year in years:
            this_year_reports = db.query(Report).filter(Report.report_nm.like(f"%사업보고서 ({year}%")).filter(Report.auditor_now == auditor).all()
            
            if this_year_reports:
                total_earnings_actual_unit = 0
                total_worktime_actual      = 0

                for report in this_year_reports:
                    total_earnings_actual_unit += report.earnings_actual_unit
                    total_worktime_actual      += extract_numeric(report.worktime_actual)

                count = len(this_year_reports)
                avg_earnings_actual_unit = total_earnings_actual_unit / count
                avg_worktime_actual      = total_worktime_actual / count

                result.append({
                    "auditor": auditor,
                    "year"   : year,
                    "avgCost": avg_earnings_actual_unit,
                    "totCost": total_earnings_actual_unit,
                    "avgTime": avg_worktime_actual,
                    "totTime": total_worktime_actual,
                    "count"  : count
                })

    return result