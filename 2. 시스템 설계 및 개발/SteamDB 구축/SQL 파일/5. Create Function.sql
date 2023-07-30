DELIMITER //
#
# 1. 게임 관련 함수
#
-- -----------------------------------------------------
-- GetLowestPrice : GameName을 입력하면 역대 최저가를 반환
-- -----------------------------------------------------
CREATE DEFINER=`root`@`localhost`
FUNCTION GetLowestPrice(GameNameinput Varchar(100)) RETURNS INT 
DETERMINISTIC

BEGIN
	DECLARE LowestPrice INT;
    
	SET LowestPrice = (SELECT   MIN(Price)
					   FROM 	price_history
					   GROUP BY price_history.GameID
					   HAVING 	price_history.GameID = (SELECT GameID
														FROM   game
														WHERE  GameName = GameNameinput));
    
    RETURN (LowestPrice);
END//
#예시
#SELECT CONCAT(GetLowestPrice('Left 4 Dead 2'), '원') AS "'Left 4 Dead 2' 역대 최저가"//

-- -----------------------------------------------------
-- GetHighestCCU : GameName을 입력하면 역대 최고 동시접속자 수(Concurrent Users)를 반환
-- -----------------------------------------------------
CREATE DEFINER=`root`@`localhost`
FUNCTION GetHighestCCU(GameNameinput Varchar(100)) RETURNS INT 
DETERMINISTIC

BEGIN
	DECLARE HighestCCU INT;
    
	SET HighestCCU = (SELECT   MAX(PlayerNum)
					  FROM 	   player_history
					  GROUP BY GameID
					  HAVING   GameID = (SELECT GameID
										 FROM   game
										 WHERE  GameName = GameNameinput));
    
    RETURN (HighestCCU);
END//
#예시
#SELECT CONCAT(GetHighestCCU("PLAYERUNKNOWN'S BATTLEGROUNDS"), '명') AS "PLAYERUNKNOWN'S BATTLEGROUNDS 역대 최고 동시접속자 수"//

-- -----------------------------------------------------
-- GetTrendingCCU : GameName을 입력하면 동시접속자 수 상승량를 반환
-- -----------------------------------------------------
CREATE DEFINER=`root`@`localhost`
FUNCTION GetTrendingCCU(GameNameinput Varchar(100)) RETURNS INT 
DETERMINISTIC

BEGIN
	DECLARE TrendingCCU INT;
    
	SET TrendingCCU = (SELECT game.PlayerNow - player_history.PlayerNum
					   FROM   game JOIN player_history 
								   ON   game.GameID = player_history.GameID
                       WHERE  player_history.Num =  (SELECT MAX(Num) - 1
												     FROM   player_history
												     WHERE  GameID = (SELECT GameID
																	  FROM   game
																	  WHERE  GameName = GameNameinput)));
    
    RETURN (TrendingCCU);
END//
#예시
#SELECT CONCAT(GetTrendingCCU('Monster Hunter: World'), '명') AS "'Monster Hunter: World' 동시접속자 수 상승량"//

-- -----------------------------------------------------
-- GetMostCommonPrice : GameName을 입력하면 평소 가격(가장 많이 책정된 가격)을 반환
-- -----------------------------------------------------
CREATE DEFINER=`root`@`localhost`
FUNCTION GetMostCommonPrice(GameNameinput Varchar(100)) RETURNS INT 
DETERMINISTIC

BEGIN
	
    DECLARE MostCommonPrice INT;
    
    SET MostCommonPrice = (SELECT price_history.Price
						   FROM   price_history
						   WHERE  price_history.GameID = (SELECT GameID
														  FROM   game
														  WHERE  GameName = GameNameinput)
						   GROUP BY price_history.Price
						   ORDER BY COUNT(*) DESC
						   LIMIT 1);
    
    RETURN (MostCommonPrice);
END//
#예시
#SELECT CONCAT(GetMostCommonPrice("Garry's Mod"),'원') AS "Garry's Mod 평소 가격"//

-- -----------------------------------------------------
-- GetDiscountRate : GameName을 입력하면 평소 가격 대비 할인률을 반환
-- -----------------------------------------------------
CREATE DEFINER=`root`@`localhost`
FUNCTION GetDiscountRate(GameNameinput Varchar(100)) RETURNS FLOAT 
DETERMINISTIC

BEGIN
	DECLARE DiscountRate FLOAT;
    DECLARE MostCommonPrice INT;
    
    SET MostCommonPrice = (SELECT price_history.Price
						   FROM   price_history
						   WHERE  price_history.GameID = (SELECT GameID
														  FROM   game
														  WHERE  GameName = GameNameinput)
						   GROUP BY price_history.Price
						   ORDER BY COUNT(*) DESC
						   LIMIT 1);
    
	SET DiscountRate = (SELECT ROUND((MostCommonPrice - game.PriceNow)/MostCommonPrice * 100,2)
					    FROM   game
                        WHERE  GameID = (SELECT GameID
										 FROM   game
										 WHERE  GameName = GameNameinput));
    
    RETURN (DiscountRate);
END//
#예시
#SELECT CONCAT(GetDiscountRate('Counter-Strike: Global Offensive'),'%') AS "'Counter-Strike: Global Offensive' 평소 가격 대비 할인률"//

-- -----------------------------------------------------
-- GetSalesRate : GameName을 입력하면 판매량(Sales Rate)을 반환
-- -----------------------------------------------------
CREATE DEFINER=`root`@`localhost`
FUNCTION GetSalesRate(GameNameinput Varchar(100)) RETURNS INT 
DETERMINISTIC

BEGIN
	DECLARE SalesRate INT;
    
	SET SalesRate = (SELECT   COUNT(*)
					 FROM     owned_games
					 GROUP BY owned_games.GameID
				 	 HAVING   owned_games.GameID = (SELECT GameID
												    FROM   game
												    WHERE  GameName = GameNameinput));
    
    RETURN (SalesRate);
END//
#예시
#SELECT CONCAT(GetSalesRate('Grand Theft Auto V'),'회') AS "'Grand Theft Auto V' 판매량"//

-- -----------------------------------------------------
-- GetDibsRate : GameName을 입력하면 위시리스트에 담긴 횟수(Dibs Rate)을 반환
-- -----------------------------------------------------
CREATE DEFINER=`root`@`localhost`
FUNCTION GetDibsRate(GameNameinput Varchar(100)) RETURNS INT 
DETERMINISTIC

BEGIN
	DECLARE DibsRate INT;
    
	SET DibsRate = (SELECT   COUNT(*)
					FROM     wishlist
					GROUP BY wishlist.GameID
					HAVING   wishlist.GameID = (SELECT GameID
										        FROM   game
										        WHERE  GameName = GameNameinput));
    
    RETURN (DibsRate);
END//
#예시
#SELECT CONCAT(GetDibsRate('Grand Theft Auto V'),'회') AS "'Grand Theft Auto V' 위시리스트에 담긴 횟수"//

-- -----------------------------------------------------
-- GetUserRating : GameName을 입력하면 유저들의 평점을 반환
-- -----------------------------------------------------
CREATE DEFINER=`root`@`localhost`
FUNCTION GetUserRating(GameNameinput Varchar(100)) RETURNS FLOAT
DETERMINISTIC

BEGIN
	DECLARE UserRating FLOAT;
    
	SET UserRating = (SELECT ROUND(Positive_Reviews/(Positive_Reviews+Negative_Reviews) * 100,2)
					  FROM   game
					  Where  GameID = (SELECT GameID
									   FROM   game
									   WHERE  GameName = GameNameinput));
                      
	RETURN (UserRating);

END//
#예시
#SELECT CONCAT(GetUserRating('PAYDAY 2'),'점') AS "'PAYDAY 2' 유저 평점"//

#
# 2. 유저 관련 함수
#
-- -----------------------------------------------------
-- GetNumOfOwnedGames : UserName을 입력하면 보유한 게임 수를 반환
-- -----------------------------------------------------
CREATE DEFINER=`root`@`localhost`
FUNCTION GetNumOfOwnedGames(UserNameinput VARCHAR(30)) RETURNS INT
DETERMINISTIC

BEGIN
	DECLARE NumOfOwnedGames INT;
    
	SET NumOfOwnedGames = (SELECT COUNT(*)
						   FROM   owned_games
                           WHERE  owned_games.UserID = (SELECT UserID
														FROM   user
														WHERE  UserName = UserNameinput));
                      
	RETURN (NumOfOwnedGames);

END//
#예시
#SELECT CONCAT(GetNumOfOwnedGames('Birkin=BH='),'개') AS "'Birkin=BH=' 보유 게임 수"//

-- -----------------------------------------------------
-- GetTotalPlayTime : UserName을 입력하면 플레이 시간 총합을 반환
-- -----------------------------------------------------
CREATE DEFINER=`root`@`localhost`
FUNCTION GetTotalPlayTime(UserNameinput VARCHAR(30)) RETURNS INT
DETERMINISTIC

BEGIN
	DECLARE TotalPlayTime INT;
    
	SET TotalPlayTime = (SELECT SUM(PlayTime)
						 FROM   owned_games
                         WHERE  owned_games.UserID = (SELECT UserID
													  FROM   user
													  WHERE  UserName = UserNameinput));
                      
	RETURN (TotalPlayTime);

END//
#예시
#SELECT CONCAT(GetTotalPlayTime('Birkin=BH='),'시간') AS "'Birkin=BH=' 플레이 시간 총합"//

#
# 3. 그룹 관련 함수
#
-- -----------------------------------------------------
-- GetNumOfGroupMembers : GroupName을 입력하면 그룹에 속한 인원 수를 반환
-- -----------------------------------------------------
CREATE DEFINER=`root`@`localhost`
FUNCTION GetNumOfGroupMembers(GroupNameinput VARCHAR(30)) RETURNS INT
DETERMINISTIC

BEGIN
	DECLARE NumOfGroupMembers INT;
    
	SET NumOfGroupMembers = (SELECT   COUNT(*)
							 FROM 	  user_group
                             GROUP BY user_group.GroupID
							 HAVING   user_group.GroupID = (SELECT GroupID
														    FROM   steamgroup
															WHERE  GroupName = GroupNameinput));
                      
	RETURN (NumOfGroupMembers);

END//
#예시
#SELECT CONCAT(GetNumOfGroupMembers('Ninjas'),'명') AS "'Ninjas' 그룹원 수"//

DELIMITER ;
