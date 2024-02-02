-- -----------------------------------------------------
-- Table `Game`
-- -----------------------------------------------------
load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/game.csv'
into table game
character set euckr
fields terminated by ','
optionally enclosed by '"'
escaped by '"'
lines terminated by '\n'
ignore 1 lines;

-- -----------------------------------------------------
-- Table `Price_History`
-- -----------------------------------------------------
load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/price_history.csv'
into table price_history
fields terminated by ','
optionally enclosed by '"'
escaped by '"'
lines terminated by '\n'
ignore 1 lines;

-- -----------------------------------------------------
-- Table `Player_History`
-- -----------------------------------------------------
load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/player_history.csv'
into table player_history
fields terminated by ','
optionally enclosed by '"'
escaped by '"'
lines terminated by '\n'
ignore 1 lines;

-- -----------------------------------------------------
-- Table `User`
-- -----------------------------------------------------
load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/user.csv'
into table user
fields terminated by ','
optionally enclosed by '"'
escaped by '"'
lines terminated by '\n'
ignore 1 lines;

-- -----------------------------------------------------
-- Table `Friendship`
-- -----------------------------------------------------
load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/friendship.csv'
into table friendship
fields terminated by ','
optionally enclosed by '"'
escaped by '"'
lines terminated by '\n'
ignore 1 lines;

-- -----------------------------------------------------
-- Table `SteamGroup`
-- -----------------------------------------------------
load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/steamgroup.csv'
into table steamgroup
fields terminated by ','
optionally enclosed by '"'
escaped by '"'
lines terminated by '\n'
ignore 1 lines;

-- -----------------------------------------------------
-- Table `User_Group`
-- -----------------------------------------------------
load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/user_group.csv'
into table user_group
fields terminated by ','
optionally enclosed by '"'
escaped by '"'
lines terminated by '\n'
ignore 1 lines;

-- -----------------------------------------------------
-- Table `Owned_Games`
-- -----------------------------------------------------
load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/owned_games.csv'
into table owned_games
fields terminated by ','
optionally enclosed by '"'
escaped by '"'
lines terminated by '\n'
ignore 1 lines;

-- -----------------------------------------------------
-- Table `WishList`
-- -----------------------------------------------------
load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/wishlist.csv'
into table wishlist
fields terminated by ','
optionally enclosed by '"'
escaped by '"'
lines terminated by '\n'
ignore 1 lines;