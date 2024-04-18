create table match_data(
ID int(50),
City varchar(100),
match_date date,
Season year,
MatchNumber varchar(100),
Team1 varchar(100),
Team2  varchar(100),
Venue varchar(100),
TossWinner varchar(100),
TossDecision  varchar(100),
SuperOver varchar(100),
WinningTeam  varchar(100),
WonBy varchar(100),
Margin int(50)
);

Create table ball_data(
ID int(50),
Innings int(50),
Overs int(50),
ballnumber int(50),
Batter varchar(100),
Bowler varchar(100),
non_striker varchar(100),
extra_type varchar(100),
batsman_run int(50),
extras_run int(50),
total_run int(50),
non_boundary int(50),
isWicketDelivery varchar(100),
player_out varchar(100),
Kind varchar(100),
fielders_involved varchar(100),
BattingTeam varchar(100)
);

Create table files(
Id int(50),
Name varchar(50)
);

Create table FS_Structure(
Root_id int(50),
Parent_id int(50),
Child_id int(50),
Current_id int(50),
name varchar(100),
Ancestral_path  varchar(100),
File_or_Directory varchar(100)
);


Create table partition_file(
Content varchar(100),
Partition_table varchar(100),
File_id int(50));