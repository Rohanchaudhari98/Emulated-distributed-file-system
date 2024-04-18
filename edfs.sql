-- MySQL dump 10.13  Distrib 8.0.31, for macos12.6 (arm64)
--
-- Host: localhost    Database: edfs
-- ------------------------------------------------------
-- Server version	8.0.31

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `FS_Structure`
--

create table match_data(
ID int(50),
City varchar(100),
MatchDate date,
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
Margin int(50),
method varchar(10),
Player_of_Match varchar(100),
Umpire1 varchar(100),
Umpire2 varchar(100)
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

Create table partition_file(
Content varchar(100),
Partition_table varchar(100),
File_id int(50));


CREATE TABLE partition_file (
  file_name varchar(100) DEFAULT NULL,
  table_name varchar(100) DEFAULT NULL,
  partitions varchar(100) DEFAULT NULL,
  content varchar(500) DEFAULT NULL
);


DROP TABLE IF EXISTS `FS_Structure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `FS_Structure` (
  `Root_id` int DEFAULT NULL,
  `Parent_id` int DEFAULT NULL,
  `Child_id` int DEFAULT NULL,
  `Current_id` int DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `Ancestral_path` varchar(100) DEFAULT NULL,
  `File_or_Directory` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `FS_Structure`
--

LOCK TABLES `FS_Structure` WRITE;
/*!40000 ALTER TABLE `FS_Structure` DISABLE KEYS */;
INSERT INTO `FS_Structure` VALUES (1,0,5,1,'/user','','Directory'),(1,1,6,2,'/lahari','/user','Directory'),(1,2,NULL,3,'/DM','/lahari','Directory'),(1,1,NULL,4,'/john','/user','Directory'),(0,0,2,1,'/user','','Directory'),(1,1,NULL,5,'/lucky','/user','Directory'),(0,0,4,1,'/user','','Directory'),(1,2,NULL,6,'/game','/lahari','Directory'),(0,1,3,2,'/lahari','/user','Directory');
/*!40000 ALTER TABLE `FS_Structure` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-10-19 18:39:07
