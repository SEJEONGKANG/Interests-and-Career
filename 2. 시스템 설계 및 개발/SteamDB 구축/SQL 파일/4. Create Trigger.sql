DELIMITER //

-- -----------------------------------------------------
-- InsertPriceHistory_First : game이 최초로 추가되면 price_history에 데이터 추가
-- -----------------------------------------------------
CREATE
DEFINER=`root`@`localhost`
TRIGGER InsertPriceHistory_First
AFTER INSERT ON GAME FOR EACH ROW

BEGIN
	INSERT INTO price_history SET
		Num = (SELECT MAX(Num)+1 FROM game),
		GameID = NEW.GameID,
		DateTime = sysdate(),
		Price = NEW.PriceNow;
END//

-- -----------------------------------------------------
-- InsertPlayerHistory_First : game이 최초로 추가되면 player_history에 데이터 추가
-- -----------------------------------------------------
CREATE
DEFINER=`root`@`localhost`
TRIGGER InsertPlayerHistory_First
AFTER INSERT ON GAME FOR EACH ROW

BEGIN
	INSERT INTO player_history SET
		Num = (SELECT MAX(Num)+1 FROM game),
		GameID = NEW.GameID,
		DateTime = sysdate(),
		PlayerNum = NEW.PlayerNow;
END//

-- -----------------------------------------------------
-- InsertPriceHistory : game이 변경되면 price_history에 데이터 추가
-- -----------------------------------------------------
CREATE
DEFINER=`root`@`localhost`
TRIGGER InsertPriceHistory
AFTER UPDATE ON GAME FOR EACH ROW

BEGIN
	INSERT INTO price_history SET
		Num = (SELECT MAX(Num)+1 FROM game),
		GameID = NEW.GameID,
		DateTime = sysdate(),
		Price = NEW.PriceNow;
END//

-- -----------------------------------------------------
-- InsertPlayerHistory : game이 변경되면 player_history에 데이터 추가
-- -----------------------------------------------------
CREATE
DEFINER=`root`@`localhost`
TRIGGER InsertPlayerHistory
AFTER UPDATE ON GAME FOR EACH ROW

BEGIN
	INSERT INTO player_history SET
		Num = (SELECT MAX(Num)+1 FROM game),
		GameID = NEW.GameID,
		DateTime = sysdate(),
		PlayerNum = NEW.PlayerNow;
END//

-- -----------------------------------------------------
-- DeleteWishlistWhenBuy : owned_games에 게임이 추가됐을 때, wishlist에서 삭제
-- -----------------------------------------------------
CREATE
DEFINER=`root`@`localhost`
TRIGGER DeleteWishlistWhenBuy
AFTER INSERT ON owned_games FOR EACH ROW

BEGIN
	IF NEW.UserID = owned_games.UserID AND NEW.GameID = owned_games.GameID
	THEN
        DELETE
		FROM wishlist
        WHERE NEW.UserID = owned_games.UserID AND NEW.GameID = owned_games.GameID;
	END IF;
END//

DELIMITER ;
