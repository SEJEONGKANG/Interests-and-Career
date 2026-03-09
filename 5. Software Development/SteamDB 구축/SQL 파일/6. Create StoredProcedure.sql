DELIMITER //
#
# 1. 게임 관련 저장 프로시저
#
-- -----------------------------------------------------
-- ShowGameIntroduction : GameName을 입력하면 게임의 정보들을 보여줌
--               -게임의 기본 정보, 역대 최저가격, 평소 가격 및 할인율, 역대 최고 동시접속자 수, 판매량 및 찜 수, 유저 평점
-- -----------------------------------------------------
CREATE DEFINER=`root`@`localhost`
PROCEDURE ShowGameIntroduction(IN GameNameinput Varchar(100))

BEGIN
	#게임의 기본 정보
    SELECT GameID      					AS '등록번호',
		   GameName    					AS '게임명',
           Developer     				AS '개발자',
           Publisher 	   				AS '공급자',
           ReleaseDate					AS '출시일',
           CONCAT(PriceNow,'원') 		AS '현재 가격',
           CONCAT(PlayerNow,'명') 		AS '현재 동시접속자 수',
           CONCAT(Positive_Reviews,'개') AS '긍정 리뷰 수',
           CONCAT(Negative_Reviews,'개') AS '부정 리뷰 수'
    FROM game
    WHERE GameName = GameNameinput;
    
	#게임의 역대 최저가격, 평소 가격, 할인율, 역대 최고 동시접속자 수, 어제 대비 동시접속자 수 상승량, 판매량, 찜 수, 유저 평점
	SELECT CONCAT(GetLowestPrice(GameNameinput),'원') 	 AS '역대 최저가격',
		   CONCAT(GetMostCommonPrice(GameNameinput),'원') AS '평소 가격',
           CONCAT(GetDiscountRate(GameNameinput),'%')	 AS '현재 할인율',
           CONCAT(GetHighestCCU(GameNameinput),'명') 	 AS '역대 최고 동시접속자 수',
           CONCAT(GetTrendingCCU(GameNameinput),'명') 	 AS '어제 대비 동시접속자 수 상승량',
           CONCAT(GetSalesRate(GameNameinput),'회') 		 AS '판매량',
           CONCAT(GetDibsRate(GameNameinput),'회') 		 AS '찜 수',
           CONCAT(GetUserRating(GameNameinput),'점')		 AS '유저 평점';
END//
#예시
#CALL ShowGameIntroduction('Counter-Strike: Global Offensive')//

-- -----------------------------------------------------
-- ShowGameRecommend : UserName을 입력하면 맞춤 게임들을 추천 (그룹원들의 플레이타임 총합 기반)
-- -----------------------------------------------------
CREATE DEFINER=`root`@`localhost`
PROCEDURE ShowGameRecommend(IN UserNameinput Varchar(30))

BEGIN
	SELECT GameName				 					AS '게임명', 
		   CONCAT(SUM(owned_games.PlayTime),'시간')  AS '그룹원들의 플레이타임 총합', 
           CONCAT(game.PriceNow, '원')  				AS '판매가격'
	FROM owned_games, game
	WHERE UserID IN (
			SELECT user_group.UserID
			FROM user_group
			WHERE user_group.GroupID IN (SELECT GroupID
										FROM user_group
										WHERE UserID = (SELECT user.UserID
														FROM   user
														WHERE  UserName = UserNameinput)))
	AND game.GameID = owned_games.GameID
	GROUP BY game.GameID
	ORDER BY SUM(owned_games.PlayTime) DESC;
END//
#예시
#CALL ShowGameRecommend('isitme')//

#
# 2. 유저 관련 저장 프로시저
#
-- -----------------------------------------------------
-- ShowProfile : UserName을 입력하면 유저의 프로필을 보여줌
--               -유저의 기본 인적사항, 게임 프로필, 친구관계 프로필, 그룹 프로필
-- -----------------------------------------------------
CREATE DEFINER=`root`@`localhost`
PROCEDURE ShowUserProfile(IN UserNameinput Varchar(30))

BEGIN
	#유저의 기본 인적사항
    SELECT UserID      AS '아이디',
		   UserName    AS '닉네임',
           Email       AS '이메일',
           Phone 	   AS '전화번호',
           Nationality AS '국적'
    FROM user
    WHERE UserName = UserNameinput;
    
	#유저의 게임 프로필(보유 게임, 플레이 시간, 평가) - 플레이 시간 순서
	SELECT game.GameName 					   AS '보유 게임', 
           CONCAT(owned_games.PlayTime, '시간') AS '플레이 시간', 
           owned_games.Review				   AS '평가 (긍정:1, 부정:-1)'
	FROM user LEFT JOIN owned_games ON user.UserID=owned_games.UserID 
					LEFT JOIN game ON owned_games.GameID=game.GameID
	WHERE user.UserID = (SELECT user.UserID
						 FROM   user
						 WHERE  UserName = UserNameinput)
	ORDER BY owned_games.PlayTime DESC;
    
    #유저의 친구관계 프로필
    SELECT friendship.To_UserID AS '친구 목록'
	FROM user LEFT JOIN friendship 
			  ON user.UserID = friendship.From_UserID
	WHERE user.UserID = (SELECT user.UserID
						 FROM   user
						 WHERE  UserName = UserNameinput)
	ORDER BY user.UserName;
    
    #유저의 그룹 프로필
    SELECT steamgroup.GroupName AS '가입 그룹'
	FROM user LEFT JOIN user_group ON user.UserID=user_group.UserID 
					LEFT JOIN steamgroup ON user_group.GroupID = steamgroup.GroupID
	WHERE user.UserID = (SELECT user.UserID
						 FROM   user
						 WHERE  UserName = UserNameinput)
	ORDER BY user.UserName;          
END//
#예시
#CALL ShowUserProfile('salad')//

#
# 3. 그룹 관련 저장 프로시저
#
-- -----------------------------------------------------
-- ShowGroupIntroduction : GroupName을 입력하면 그룹의 정보들을 보여줌
--               -그룹의 기본 정보, 멤버 수
-- -----------------------------------------------------
CREATE DEFINER=`root`@`localhost`
PROCEDURE ShowGroupIntroduction(IN GroupNameinput Varchar(30))

BEGIN
	#게임의 기본 정보
    SELECT GroupID      					AS '등록번호',
		   GroupName    					AS '그룹명',
           CreatedDateTime     				AS '창설 일자',
           Creator		 	   				AS '창설자'
	FROM steamgroup
    WHERE GroupName = GroupNameinput;
    
	#그룹의 멤버 수
	SELECT CONCAT(GetNumOfGroupMembers(GroupNameinput),'명') AS '멤버 수';
END//
#예시
#CALL ShowGroupIntroduction('Ninjas')// 

DELIMITER ;
