/*
SQLyog Professional v12.09 (64 bit)
MySQL - 5.7.24 : Database - 360ehs
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`360ehs` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `360ehs`;

/*Table structure for table `tbl_users` */

DROP TABLE IF EXISTS `tbl_users`;

CREATE TABLE `tbl_users` (
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role` varchar(200) NOT NULL,
  `status` varchar(200) NOT NULL,
  `first_name` varchar(75) NOT NULL,
  `last_name` varchar(75) DEFAULT NULL,
  `email` varchar(254) NOT NULL,
  `phone` varchar(200) NOT NULL,
  `extension` varchar(200) NOT NULL,
  `signature` varchar(200) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `check` varchar(200) NOT NULL,
  `branch` varchar(200) NOT NULL,
  `institute` varchar(200) NOT NULL,
  `account` varchar(200) NOT NULL,
  `report_fee` varchar(200) NOT NULL,
  `address` longtext NOT NULL,
  `cpso_id` varchar(200) NOT NULL,
  `cmpa_id` varchar(200) NOT NULL,
  `physician_type` varchar(200) NOT NULL,
  `bio` varchar(200) NOT NULL,
  `neurological` longtext NOT NULL,
  `shoulder` longtext NOT NULL,
  `cervical` longtext NOT NULL,
  `lumbarspine` longtext NOT NULL,
  `knee` longtext NOT NULL,
  `ankle` longtext NOT NULL,
  `hand` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `tbl_users` */

insert  into `tbl_users`(`password`,`last_login`,`id`,`role`,`status`,`first_name`,`last_name`,`email`,`phone`,`extension`,`signature`,`is_superuser`,`check`,`branch`,`institute`,`account`,`report_fee`,`address`,`cpso_id`,`cmpa_id`,`physician_type`,`bio`,`neurological`,`shoulder`,`cervical`,`lumbarspine`,`knee`,`ankle`,`hand`) values ('pbkdf2_sha256$180000$rIHKJaeETQrA$Zq1sSgrOI9zlbAwRsjQsvx0AhnwcsLSi0n/jTtNlNmE=','2020-10-21 03:24:57.869833',1,'System Admin','true','Yingying','Ye','yingyingyeah@outlook.com','123456789','','',0,'','','','','','AAA','','','','','','','','','','','');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
