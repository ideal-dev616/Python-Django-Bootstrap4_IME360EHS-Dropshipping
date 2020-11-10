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

/*Table structure for table `tbl_clinics` */

DROP TABLE IF EXISTS `tbl_clinics`;

CREATE TABLE `tbl_clinics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `clinic_name` varchar(200) CHARACTER SET latin1 NOT NULL DEFAULT '',
  `motto_name` varchar(200) CHARACTER SET latin1 NOT NULL DEFAULT '',
  `website` varchar(200) CHARACTER SET latin1 NOT NULL DEFAULT '',
  `ship_cost` int(11) NOT NULL,
  `note_profile` longtext CHARACTER SET latin1 NOT NULL,
  `address_type` varchar(200) CHARACTER SET latin1 NOT NULL DEFAULT '',
  `address_line1` varchar(200) CHARACTER SET latin1 NOT NULL DEFAULT '',
  `address_line2` varchar(200) CHARACTER SET latin1 NOT NULL DEFAULT '',
  `country` varchar(200) CHARACTER SET latin1 NOT NULL DEFAULT '',
  `region` varchar(200) CHARACTER SET latin1 NOT NULL DEFAULT '',
  `city` varchar(200) CHARACTER SET latin1 NOT NULL DEFAULT '',
  `postal_code` varchar(200) CHARACTER SET latin1 NOT NULL DEFAULT '',
  `clinic_users` longtext CHARACTER SET latin1 NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

/*Data for the table `tbl_clinics` */

insert  into `tbl_clinics`(`id`,`clinic_name`,`motto_name`,`website`,`ship_cost`,`note_profile`,`address_type`,`address_line1`,`address_line2`,`country`,`region`,`city`,`postal_code`,`clinic_users`) values (1,'Urgent Care Brampton','Urgent Care','urgentcarecentre.ca',10,'agree','Main','51 MountainAsh Rd.','Unit 8','Canada','Ontario','Brampton','L6R 4W1','10\r'),(2,'Urgent Care Brampton West','Urgent Care','urgentcarecentre.ca',10,'agree','Main','10088 McLaughlin Rd.','McLaughlin Corners West','Canada','Ontario','Brampton','L7A2X6','10\r'),(3,'Urgent Care Woodbridge','Urgent Care','urgentcarecentre.ca',10,'agree','Main','4000 Hwy 7','Unit 2','Canada','Ontario','Woodbridge','L4L 8Z2','10\r'),(4,'Urgent Care Etobicoke','Urgent Care','urgentcarecentre.ca',10,'agree','Main','25 Woodbine Downs Blvd.','Unit 10','Canada','Ontario','Etobicoke','M9W 6N5','10\r'),(5,'Urgent Care Malton','Urgent Care','urgentcarecentre.ca',10,'agree','Main','3530 Derry Road East','Unit 110-111','Canada','Ontario','Mississauga','L4T 4E3','10\r'),(6,'Urgent Care Mississauga','Urgent Care','urgentcarecentre.ca',10,'agree','Main','1500 Dundas Street East','Inside Walmart','Canada','Ontario','Mississauga','L4X 1L4','10\r');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
