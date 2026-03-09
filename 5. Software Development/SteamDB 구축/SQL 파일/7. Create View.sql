#
# 1. 게임 관련 뷰
#
-- -----------------------------------------------------
-- SPECIAL_OFFERS : 각 게임의 평소 가격 대비 할인율을 순위를 매겨 제시
-- -----------------------------------------------------
CREATE  OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER
VIEW SPECIAL_OFFERS AS
	SELECT CONCAT(rank() over (order by GetDiscountRate(game.GameName) DESC),'위') AS '할인율 순위', 
		   game.GameName AS '게임명', 
		   CONCAT(ROUND(GetDiscountRate(game.GameName),2),'%') AS '평소 대비 현재 할인율', 
	   	   CONCAT(game.PriceNow,'원') AS '현재 가격', 
		   CONCAT(GetMostCommonPrice(game.GameName),'원') AS '평소 가격',
		   CONCAT(GetLowestPrice(game.GameName),'원') AS '역대 최저 가격'
    FROM game
    GROUP BY game.GameName;
    
#VIEW 보기
#SELECT * FROM SPECIAL_OFFERS;

-- -----------------------------------------------------
-- LowestPrice : 각 게임의 역대 최저가와 당시 날짜를 제시
-- -----------------------------------------------------
CREATE  OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER
VIEW LowestPrice AS
	SELECT game.GameName AS '게임명', 
		   CONCAT(GetLowestPrice(game.GameName),'원') AS '역대 최저가', 
		   price_history.DateTime AS '당시 날짜'
    FROM game LEFT JOIN price_history ON game.GameID = price_history.GameID
    WHERE GetLowestPrice(game.GameName) = price_history.price
    GROUP BY game.GameName
    ORDER BY game.GameName;

#VIEW 보기
#SELECT * FROM LowestPrice;

-- -----------------------------------------------------
-- HightestCCU : 각 게임의 역대 최고 동시접속자 수와 당시 날짜를 순위를 매겨 제시
-- -----------------------------------------------------
CREATE  OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER
VIEW HightestCCU AS
	SELECT CONCAT(rank() over (order by GetHighestCCU(game.GameName) DESC),'위') AS '게임 순위(최대 동시접속자 수)', 
		   game.GameName AS '게임명', 
           CONCAT(GetHighestCCU(game.GameName),'명') AS '최대 동시접속자 수', 
           player_history.DateTime AS '당시 날짜'
    FROM game LEFT JOIN player_history ON game.GameID = player_history.GameID
    WHERE GetHighestCCU(game.GameName) = player_history.PlayerNum
    GROUP BY game.GameName;
    
#VIEW 보기 ( 시간이 다소 걸릴 수 있음 )
#SELECT * FROM HightestCCU;
    
-- -----------------------------------------------------
-- TrendingCCU : 각 게임의 어제 대비 동시접속자 수 상승량을 순위를 매겨 제시
-- -----------------------------------------------------
CREATE  OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER
VIEW TrendingCCU AS
	SELECT CONCAT(rank() over (order by GetTrendingCCU(game.GameName) DESC),'위') AS '게임 순위(동시접속자 수 상승량)', 
		   game.GameName AS '게임명', 
           CONCAT(GetTrendingCCU(game.GameName),'명') AS '어제 대비 동시접속자 수 상승량', 
           SYSDATE() AS '현재 시간'
    FROM game LEFT JOIN player_history ON game.GameID = player_history.GameID
    GROUP BY game.GameName;

#VIEW 보기
#SELECT * FROM TrendingCCU;

-- -----------------------------------------------------
-- NowCCU : 각 게임의 현재 동시접속자 수를 순위를 매겨 제시
-- -----------------------------------------------------
CREATE  OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER
VIEW NowCCU AS
	SELECT CONCAT(rank() over (order by game.PlayerNow DESC),'위') AS '게임 순위(현재 동시접속자 수)',
		   game.GameName AS '게임명', 
		   CONCAT(game.PlayerNow,'명') AS '현재 동시접속자 수', 
           sysdate() AS '현재 시간'
    FROM game;
    
#VIEW 보기
#SELECT * FROM NowCCU;

-- -----------------------------------------------------
-- UserRating : 각 게임의 유저 평점을 순위를 매겨 제시
-- -----------------------------------------------------
CREATE  OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER
VIEW UserRating AS
	SELECT CONCAT(rank() over (order by GetUserRating(GameName) DESC),'위') AS '게임 순위(유저 평점)',
		   game.GameName AS '게임명', 
           CONCAT(GetUserRating(GameName),'점') AS '유저 평점'
    FROM game;

#VIEW 보기
#SELECT * FROM UserRating;

-- -----------------------------------------------------
-- SalesRate : 각 게임의 판매 수, 찜 수를 순위를 매겨 제시
-- -----------------------------------------------------
CREATE  OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER
VIEW SalesRate AS
	SELECT CONCAT(rank() over (order by GetSalesRate(GameName) DESC),'위') AS '게임 순위(판매량)', 
		   game.GameName AS '게임명', 
           CONCAT(GetSalesRate(GameName),'회') AS '판매 횟수',
           CONCAT(rank() over (order by GetDibsRate(GameName) DESC),'위') AS '게임 순위(찜 수)', 
		   CONCAT(GetDibsRate(GameName),'회') AS '찜 횟수'
    FROM game
    ORDER BY GetSalesRate(GameName) DESC;

#VIEW 보기
#SELECT * FROM SalesRate;

#
# 2. 유저 관련 뷰
#
-- -----------------------------------------------------
-- UserRanking_OwnedGames : 게임 보유 수에 따른 유저의 순위표를 제시
-- -----------------------------------------------------
CREATE  OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER
VIEW UserRanking_OwnedGames AS
	SELECT CONCAT(rank() over (order by GetNumOfOwnedGames(UserName) DESC),'위') AS '유저 순위(보유 게임 수)', 
		   UserName AS '닉네임', 
           CONCAT(GetNumOfOwnedGames(UserName),'개') AS '보유 게임 수'
    FROM user;

#VIEW 보기
#SELECT * FROM UserRanking_OwnedGames;

-- -----------------------------------------------------
-- UserRanking_PlayTime : 플레이 시간 총합에 따른 유저의 순위표를 제시
-- -----------------------------------------------------
CREATE  OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER
VIEW UserRanking_PlayTime AS
	SELECT CONCAT(rank() over (order by GetTotalPlayTime(UserName) DESC),'위') AS '유저 순위(플레이 시간 총합)', 
		   UserName AS '닉네임', 
           CONCAT(GetTotalPlayTime(UserName),'시간') AS '플레이 시간 총합'
    FROM user;

#VIEW 보기
#SELECT * FROM UserRanking_PlayTime;

#
# 3. 그룹 관련 뷰
#
-- -----------------------------------------------------
-- GroupRanking : 멤버 수에 따른 그룹의 순위표를 제시
-- -----------------------------------------------------
CREATE  OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER
VIEW GroupRanking AS
	SELECT CONCAT(rank() over (order by GetNumOfGroupMembers(GroupName) DESC),'위') AS '그룹 순위(멤버 수)', 
		   GroupName AS '그룹명', 
           CONCAT(GetNumOfGroupMembers(GroupName),'명') AS '멤버 수'
    FROM steamgroup;

#VIEW 보기
#SELECT * FROM GroupRanking;

