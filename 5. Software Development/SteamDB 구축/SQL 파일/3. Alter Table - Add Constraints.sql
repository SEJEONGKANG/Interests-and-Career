SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Table `Price_History`
-- -----------------------------------------------------
ALTER TABLE `steam_database`.`price_history`
  ADD CONSTRAINT `Price_History_GameIDFK`
    FOREIGN KEY (`GameID`)
    REFERENCES `steam_database`.`game` (`GameID`)
		ON DELETE CASCADE
		ON UPDATE CASCADE;
        
-- -----------------------------------------------------
-- Table `Player_History`
-- -----------------------------------------------------
ALTER TABLE `steam_database`.`player_history` 
  ADD CONSTRAINT `Player_History_GameIDFK`
    FOREIGN KEY (`GameID`)
    REFERENCES `steam_database`.`game` (`GameID`)
		ON DELETE CASCADE
		ON UPDATE CASCADE;
        
-- -----------------------------------------------------
-- Table `Friendship`
-- -----------------------------------------------------
ALTER TABLE `steam_database`.`friendship` 
  ADD CONSTRAINT `Friendship_From_FK`
    FOREIGN KEY (`From_UserID`)
    REFERENCES `steam_database`.`user` (`UserID`)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION,
  ADD CONSTRAINT `Friendship_To_FK`
    FOREIGN KEY (`To_UserID`)
    REFERENCES `steam_database`.`user` (`UserID`)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION;    

-- -----------------------------------------------------
-- Table `User_Group`
-- -----------------------------------------------------
ALTER TABLE `steam_database`.`user_group`
   ADD CONSTRAINT `User_Group_GroupFK`
    FOREIGN KEY (`GroupID`)
    REFERENCES `steam_database`.`steamgroup` (`GroupID`)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
  ADD CONSTRAINT `User_Group_UserFK`
    FOREIGN KEY (`UserID`)
    REFERENCES `steam_database`.`user` (`UserID`)
		ON DELETE CASCADE
		ON UPDATE CASCADE;
        
-- -----------------------------------------------------
-- Table `Owned_Games`
-- -----------------------------------------------------
ALTER TABLE `steam_database`.`owned_games`
   ADD CONSTRAINT `FK_owned_games_games`
    FOREIGN KEY (`GameID`)
    REFERENCES `steam_database`.`game` (`GameID`)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_owned_games_users`
    FOREIGN KEY (`UserID`)
    REFERENCES `steam_database`.`user` (`UserID`)
		ON DELETE CASCADE
		ON UPDATE CASCADE;
 
-- -----------------------------------------------------
-- Table `WishList`
-- -----------------------------------------------------
ALTER TABLE `steam_database`.`wishlist`
  ADD CONSTRAINT `FK_wishlist_games`
    FOREIGN KEY (`GameID`)
    REFERENCES `steam_database`.`game` (`GameID`)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_wishlist_users`
    FOREIGN KEY (`UserID`)
    REFERENCES `steam_database`.`user` (`UserID`)
		ON DELETE CASCADE
		ON UPDATE CASCADE;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
