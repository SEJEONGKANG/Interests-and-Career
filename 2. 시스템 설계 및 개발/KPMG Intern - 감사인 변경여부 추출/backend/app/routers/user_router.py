from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import UserInterest, User, Corp
from app.database.schemas import StarredCorpInfo, LoginResponse
from sqlalchemy          import select
from typing import List
from pydantic import BaseModel

router = APIRouter()

# 유저의 즐겨찾기 목록 반환
def show_starred(db: Session, user_id: str):
    user_interest = db.query(UserInterest).filter_by(user_id=user_id).all()
    query         = select(Corp.corp_code, Corp.corp_name).where(Corp.corp_code.in_([interest.corp_code for interest in user_interest]))
    result        = db.execute(query).fetchall()
    starred_corps = [StarredCorpInfo(corp_code=corp.corp_code, corp_name=corp.corp_name) for corp in result]
    return starred_corps

# id password를 통해 로그인 및 즐겨찾기 목록을 반환하는 엔드포인트
@router.post("/login", response_model=LoginResponse, summary="로그인 및 즐겨찾기 목록 반환")
def check_id_endpoint(id_input: str, password: str, db: Session = Depends(get_db)):
    """
    사용자 로그인 및 즐겨찾기 목록을 반환합니다.

    - **id_input**: 사용자 아이디.
    - **password**: 비밀번호.
    - **db**      : SQLAlchemy 세션.

    Returns:
    - **log_in**: 로그인 성공 여부 bool.
    - **starred**: 즐겨찾기에 등록한 기업들의 기본 정보 딕셔너리가 담긴 리스트.
      - corp_code: 기업 코드.
      - corp_name: 기업명.

    로그인 기능에 활용.
    """

    user = db.query(User).filter(User.user_id == id_input).first()
    if user:
        db_password = user.password
        if password == db_password:
            starred = show_starred(db, id_input)
            return {"log_in": True,  "starred": starred}
        else:
            return {"log_in": False, "starred": []}
    else:
        new_user = User(user_id=id_input, password=password)
        db.add(new_user)
        db.commit()
        return {"log_in": True, "starred": []}
