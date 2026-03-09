-- -----------------------------------------------------
-- 2019147019 강세정 기말 프로젝트 2020
-- 게임사이트 '스팀' 데이터베이스 제작
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema 'Steam_Database'
-- -----------------------------------------------------
CREATE SCHEMA `steam_database` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `steam_database` ;

-- -----------------------------------------------------
-- Table 'Game'
-- -----------------------------------------------------
CREATE TABLE `steam_database`.`game` (
  `GameID` 			 INT 		  NOT NULL,
  `GameName` 		 VARCHAR(100) NOT NULL,
  `Developer` 		 VARCHAR(100) NOT NULL,
  `Publisher` 		 VARCHAR(100) NOT NULL,
  `ReleaseDate` 	 DATE 		  NOT NULL,
  `PlayerNow` 		 INT		  NOT NULL,
  `PriceNow` 		 INT 		  NOT NULL,
  `Positive_Reviews` INT 		      NULL DEFAULT '0',
  `Negative_Reviews` INT 			  NULL DEFAULT '0',
  PRIMARY KEY (`GameID`),
  UNIQUE INDEX `GameNameAK` (`GameName` ASC) VISIBLE);

-- -----------------------------------------------------
-- Table `Price_History`
-- -----------------------------------------------------
CREATE TABLE `steam_database`.`price_history` (
  `Num` 			INT 		NOT NULL,
  `GameID` 			INT 		NOT NULL,
  `DateTime` 		DATETIME	NOT NULL,
  `Price` 			INT 		NOT NULL,
  PRIMARY KEY (`Num`),
  INDEX `FK_player_history` (`GameID` ASC) VISIBLE);
  
-- -----------------------------------------------------
-- Table 'Player_History'
-- -----------------------------------------------------
CREATE TABLE `steam_database`.`player_history` (
  `Num` 			INT 		NOT NULL,
  `GameID` 			INT 		NOT NULL,
  `DateTime` 		DATETIME 	NOT NULL,
  `PlayerNum` 		INT 			NULL DEFAULT '0',
  PRIMARY KEY (`Num`),
  INDEX `FK_player_history` (`GameID` ASC) VISIBLE);

-- -----------------------------------------------------
-- Table `User`
-- -----------------------------------------------------
CREATE TABLE `steam_database`.`user` (
  `UserID` 			VARCHAR(30) NOT NULL,
  `UserName` 		VARCHAR(30) NOT NULL,
  `Email` 			VARCHAR(50) NOT NULL,
  `Phone` 			VARCHAR(20) NOT NULL,
  `Nationality` 	VARCHAR(30) 	NULL DEFAULT NULL,
  PRIMARY KEY (`UserID`),
  UNIQUE INDEX `UserNameAK` (`UserName` ASC) VISIBLE,
  UNIQUE INDEX `EmailAK` (`Email` ASC) VISIBLE,
  UNIQUE INDEX `PhoneAK` (`Phone` ASC) VISIBLE);

-- -----------------------------------------------------
-- Table `Friendship`
-- -----------------------------------------------------
CREATE TABLE `steam_database`.`friendship` (
  `Num` 			INT 		NOT NULL,
  `From_UserID` 	VARCHAR(30) NOT NULL,
  `To_UserID` 		VARCHAR(30) NOT NULL,
  PRIMARY KEY (`From_UserID`, `To_UserID`),
  INDEX `Friendship_To_FK_idx` (`To_UserID` ASC) VISIBLE);
  
-- -----------------------------------------------------
-- Table 'SteamGroup`
-- -----------------------------------------------------
CREATE TABLE `steam_database`.`steamgroup` (
  `GroupID` 		INT 		NOT NULL,
  `GroupName` 		VARCHAR(30) NOT NULL,
  `CreatedDateTime` DATETIME 		NULL DEFAULT NULL,
  `Creator` 		VARCHAR(30) NOT NULL,
  PRIMARY KEY (`GroupID`),
  UNIQUE INDEX `GroupNameAK` (`GroupName` ASC) VISIBLE);

-- -----------------------------------------------------
-- Table `User_Group`
-- -----------------------------------------------------
CREATE TABLE `steam_database`.`user_group` (
  `UserID` 			VARCHAR(30) NOT NULL,
  `GroupID` 		INT 		NOT NULL,
  PRIMARY KEY (`UserID`, `GroupID`),
  INDEX `FK_user_group_users` (`UserID` ASC) VISIBLE,
  INDEX `FK_user_group_groups` (`GroupID` ASC) VISIBLE);

-- -----------------------------------------------------
-- Table `Owned_Games`
-- -----------------------------------------------------
CREATE TABLE `steam_database`.`owned_games` (
  `UserID` 			VARCHAR(30) NOT NULL,
  `GameID` 			INT 		NOT NULL,
  `PlayTime` 		INT 			NULL DEFAULT '0',
  `Review` 			INT 			NULL DEFAULT NULL,
  PRIMARY KEY (`UserID`, `GameID`),
  INDEX `FK_owned_games_users` (`UserID` ASC) VISIBLE,
  INDEX `FK_owned_games_games` (`GameID` ASC) VISIBLE);

-- -----------------------------------------------------
-- Table `WishList`
-- -----------------------------------------------------
CREATE TABLE `steam_database`.`wishlist` (
  `UserID` 			VARCHAR(30) NOT NULL,
  `GameID` 			INT 		NOT NULL,
  PRIMARY KEY (`UserID`, `GameID`),
  INDEX `FK_wishlist_users` (`UserID` ASC) VISIBLE,
  INDEX `FK_wishlist_games` (`GameID` ASC) VISIBLE);
  