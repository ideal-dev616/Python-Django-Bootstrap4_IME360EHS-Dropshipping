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

/*Table structure for table `tbl_products` */

DROP TABLE IF EXISTS `tbl_products`;

CREATE TABLE `tbl_products` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_code` varchar(200) CHARACTER SET latin1 NOT NULL,
  `unit` varchar(200) CHARACTER SET latin1 NOT NULL,
  `description` varchar(200) CHARACTER SET latin1 NOT NULL,
  `cost` varchar(200) CHARACTER SET latin1 NOT NULL,
  `manufacturer` varchar(200) CHARACTER SET latin1 NOT NULL,
  `markup` varchar(200) CHARACTER SET latin1 NOT NULL,
  `category` varchar(200) CHARACTER SET latin1 NOT NULL,
  `retail` varchar(200) CHARACTER SET latin1 NOT NULL,
  `product_image` varchar(200) CHARACTER SET latin1 NOT NULL,
  `status` varchar(200) CHARACTER SET latin1 NOT NULL,
  `product_type` varchar(200) CHARACTER SET latin1 NOT NULL,
  `service_cost` varchar(200) CHARACTER SET latin1 NOT NULL,
  `service_markup` varchar(200) CHARACTER SET latin1 NOT NULL,
  `service_retail` varchar(200) CHARACTER SET latin1 NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=198 DEFAULT CHARSET=utf8;

/*Data for the table `tbl_products` */

insert  into `tbl_products`(`id`,`product_code`,`unit`,`description`,`cost`,`manufacturer`,`markup`,`category`,`retail`,`product_image`,`status`,`product_type`,`service_cost`,`service_markup`,`service_retail`) values (1,'001-SC-102','BOX','Glove Exam Latex P/F N/S Promedix SMALL Bx/100','5.70','Stevens','75.26','GLOVES','9.99','','In Stock','FALSE','','',''),(2,'001-SC-103','BOX','Glove Exam Latex P/F N/S Promedix MEDIUM Bx/100','5.70','Stevens','75.26','GLOVES','9.99','','In Stock','FALSE','','',''),(3,'001-SC-104','BOX','Glove Exam Latex P/F N/S Promedix LARGE Bx/100','5.70','Stevens','75.26','GLOVES','9.99','','In Stock','FALSE','','',''),(4,'001-SC-105','BOX','Glove Exam Latex P/F N/S Promedix X-LARGE Bx/90','5.50','Stevens','81.64','GLOVES','9.99','','In Stock','FALSE','','',''),(5,'001-SC161200','BOX','Glove Exam NON LATEX P/F N/S Medium Bx/100','3.20','Stevens','87.19','GLOVES','5.99','','In Stock','FALSE','','',''),(6,'001-SC-401M','BAG','Speculum Vaginal Graves Med N/S Bg/10','3.05','Stevens','63.61','DIAGNOSTIC TEST & SUPPLIES','4.99','','In Stock','FALSE','','',''),(7,'001-SC-401S','BAG','Speculum Vaginal Graves Sml N/S Bg/10','3.05','Stevens','63.61','DIAGNOSTIC TEST & SUPPLIES','4.99','','In Stock','FALSE','','',''),(8,'001-SC918','CASE','Paper Table Smooth 18in x 225ft ca/12','27.00','Stevens','37.00','SUNDRY AND ROOM ITEMS','36.99','','In Stock','FALSE','','',''),(9,'001-SC-APM','BOX','Alcohol Prep Pads Medium Bx/200','1.50','Stevens','99.33','INFECTION CONTROL','2.99','','In Stock','FALSE','','',''),(10,'001-SC-CTA-6-X','BAG','Cotton Tip Applicator 6in N/S Bg/100','0.47','Stevens','110.64','SUNDRY AND ROOM ITEMS','0.99','','In Stock','FALSE','','',''),(11,'001-SC-MC-01-X','BOX','Cup Medicine Poly 1Oz Graduated 30Ml Pro-Medix Pk/100','0.62','Stevens','53.23','DIAGNOSTIC TEST & SUPPLIES','0.95','','In Stock','FALSE','','',''),(12,'001-SC-TDA-500','BOX','Tongue Depressor Adult Bx/500','5.25','Stevens','32.38','SUNDRY AND ROOM ITEMS','6.95','','In Stock','FALSE','','',''),(13,'011-201','BOX','Glustitch Adhesive Skin Single Dose 0.2ml Clear Bx/12','83.20','Stevens','38.22','SUTURES AND DRESSINGS','115.00','','In Stock','FALSE','','',''),(14,'053-NON255125','PACK','Packing Gauze Plain 0.5in X 5yd Sterile','3.90','Stevens','27.95','SUTURES AND DRESSINGS','4.99','','In Stock','FALSE','','',''),(15,'053-NON255145','PACK','Packing Gauze Plain 0.25In X 5yd Sterile','3.60','Stevens','31.94','SUTURES AND DRESSINGS','4.75','','In Stock','FALSE','','',''),(16,'102-1961','BOX','Dressing Telfa Non-Adherent Non-Ad Hesive 2 X 3in Ster Pk/1 Bx/100','13.20','Stevens','36.29','SUTURES AND DRESSINGS','17.99','','In Stock','FALSE','','',''),(17,'102-2132','BOX','Dressing Telfa Non-Adherent Non-Ad Hesive 3 X 4in Ster Bx/100','14.70','Stevens','32.65','SUTURES AND DRESSINGS','19.50','','In Stock','FALSE','','',''),(18,'111-03100','EACH','Bulb Halogen 3.5v For Otoscopes','20.70','Stevens','30.39','BULB REPLACEMENT','26.99','','In Stock','FALSE','','',''),(19,'111-03800','EACH','Bulb Halogen Opthalmoscopes','34.00','Stevens','32.35','BULB REPLACEMENT','45.00','','In Stock','FALSE','','',''),(20,'111-05075-005','BOX','Thermoscan Probe Covers For Pro-3000/4000 pk/200','15.80','Stevens','32.59','DIAGNOSTIC TEST & SUPPLIES','20.95','','In Stock','FALSE','','',''),(21,'111-06000-005-X','BOX','Cover Probe F/Braun Pro-6000 Bx/200','15.80','Stevens','32.59','DIAGNOSTIC TEST & SUPPLIES','20.95','','In Stock','FALSE','','',''),(22,'111-06500','BOX','Bulb Halogen 3.5V For 23820/23810 Macroview Otoscope','20.80','Stevens','34.38','BULB REPLACEMENT','27.95','','In Stock','FALSE','','',''),(23,'111-52432-U','BOX','Otoscope Disposable Ear Speculum 2.75 mm Bg/850','32.00','Stevens','32.81','SUNDRY AND ROOM ITEMS','42.50','','In Stock','FALSE','','',''),(24,'111-52434-U','BOX','Otoscope Disposable Ear Speculum 4.25 mm Bg/850','32.00','Stevens','32.81','SUNDRY AND ROOM ITEMS','42.50','','In Stock','FALSE','','',''),(25,'111-52450','BOX','Speculum Otoscope Disp Kleenscoop Cerumen Removal Bx/100','32.00','Stevens','32.81','SUNDRY AND ROOM ITEMS','42.50','','In Stock','FALSE','','',''),(26,'114-014','EACH','Anesthetic Local Inj Xylocaine 1% plain 50 ml Vial','9.30','Stevens','50.43','PHARMACEUTICALS','13.99','','In Stock','FALSE','','',''),(27,'114-016','EACH','Anesthetic Local Inj Xylocaine 1% W/Epine 20Ml Vial','10.30','Stevens','35.83','PHARMACEUTICALS','13.99','','In Stock','FALSE','','',''),(28,'114-023','EACH','Anesthetic Local Inj Xylocaine 2% plain 50 ml','9.90','Stevens','41.31','PHARMACEUTICALS','13.99','','In Stock','FALSE','','',''),(29,'114-1461','EACH','Anesthetic Local Inj Xylocaine 2% w/Epin 20Ml','10.30','Stevens','35.83','PHARMACEUTICALS','13.99','','In Stock','FALSE','','',''),(30,'140-4888','BOX','Curette Ear Safe Blue Infantscoop Bx/50','15.00','Stevens','33.00','SUTURES AND DRESSINGS','19.95','','In Stock','FALSE','','',''),(31,'140-9555','BOX','Curette Ear Safe White Flexloop Bx/50','15.00','Stevens','33.00','SUTURES AND DRESSINGS','19.95','','In Stock','FALSE','','',''),(32,'151-01700','CASE','Towel Hand Singlefold Scott 10.5 x 9.3 In 1 Ply White Ca/16X250','35.80','Stevens','31.15','TOILETRIES','46.95','','In Stock','FALSE','','',''),(33,'151-07805','CASE','Tissue Bath Jr Jumbo Roll Scott Jrt 3.55In X 1000 ft 2 Ply White Ca/12','58.80','Stevens','30.87','TOILETRIES','76.95','','In Stock','FALSE','','',''),(34,'151-21400','CASE','Tissue Facial Kleenex Popup 8.5 x 8In 2-Ply White Ca/36X100','32.00','Stevens','31.09','TOILETRIES','41.95','','In Stock','FALSE','','',''),(35,'164-SS1','BOX','Sterilization Pouches 3.5 X 8In Bx/200','12.30','Stevens','30.00','REPROCESSING SUPPLIES','15.99','','In Stock','FALSE','','',''),(36,'164-SS4','BOX','Sterilization Pouchs 5 X 10in Bx/200','16.70','Stevens','31.44','REPROCESSING SUPPLIES','21.95','','In Stock','FALSE','','',''),(37,'185-66003650','BOX','Dressing Bactigras Tulle Gras L/F 10Cm X 10Cm Bx/50','51.20','Stevens','30.76','SUTURES AND DRESSINGS','66.95','','In Stock','FALSE','','',''),(38,'185-7461','BOX','Dressing Bactigras Tulle Gras L/F 15 cm X 20 cm Bx/10','36.40','Stevens','31.73','SUTURES AND DRESSINGS','47.95','','In Stock','FALSE','','',''),(39,'187-81220','EACH','Stockinette Tubular Cotton 2 in X 25 yds','11.40','Stevens','31.14','IMMOBILIZATION (CASTING & SPINTING)','14.95','','In Stock','FALSE','','',''),(40,'187-81320','EACH','Stockinette Tubular Cotton 3 in X 25 Yds','17.30','Stevens','32.66','IMMOBILIZATION (CASTING & SPINTING)','22.95','','In Stock','FALSE','','',''),(41,'187-81420','EACH','Stockinette Tubular Cotton 4 in X 25 Yds','19.40','Stevens','33.76','IMMOBILIZATION (CASTING & SPINTING)','25.95','','In Stock','FALSE','','',''),(42,'195-7144303','BOX','Tape Hypafix Retention 15Cm X 10M L/Free Bx/1 Rl (714433)','10.50','Stevens','32.86','SUTURES AND DRESSINGS','13.95','','In Stock','FALSE','','',''),(43,'195-7201400','PACK','Cast Padding Pro-touch Plus 10 cm X 2.7 m Pk/12','13.80','Stevens','30.36','IMMOBILIZATION (CASTING & SPINTING)','17.99','','In Stock','FALSE','','',''),(44,'195-7201401','PACK','Cast Padding Pro-touch Plus 15 cm X 2.7 m Pk/12','20.70','Stevens','30.19','IMMOBILIZATION (CASTING & SPINTING)','26.95','','In Stock','FALSE','','',''),(45,'195-7201402','PACK','Cast Padding Pro-touch Plus 5 cm X 2.7 m Pk/12','6.90','Stevens','29.71','IMMOBILIZATION (CASTING & SPINTING)','8.95','','In Stock','FALSE','','',''),(46,'195-7201403','PACK','Cast Padding Pro-touch Plus 7.5 cm X 2.7 m Pk/12','10.40','Stevens','34.13','IMMOBILIZATION (CASTING & SPINTING)','13.95','','In Stock','FALSE','','',''),(47,'195-7214301','BOX','Dressing Coverplast Wound 7.2X2.2Cm Bx/100','15.70','Stevens','33.44','SUTURES AND DRESSINGS','20.95','','In Stock','FALSE','','',''),(48,'195-7214302','BOX','Dressing Coverplast Wound 3.8x3.8Cm Bx/100 (was 7130200)','16.70','Stevens','31.44','SUTURES AND DRESSINGS','21.95','','In Stock','FALSE','','',''),(49,'195-7214303','BOX','Dressing Coverplast Wound 2.4 Cm Round Spot Bx/100','5.60','Stevens','41.96','SUTURES AND DRESSINGS','7.95','','In Stock','FALSE','','',''),(50,'195-7214304','BOX','Dressing Coverplast Wound 3.8X2.2Cm Bx/100','12.20','Stevens','30.74','SUTURES AND DRESSINGS','15.95','','In Stock','FALSE','','',''),(51,'195-7214305','BOX','Dressing Coverplast Wound 6.3X3.8Cm Bx/100','12.50','Stevens','35.60','SUTURES AND DRESSINGS','16.95','','In Stock','FALSE','','',''),(52,'195-7260101','BOX','Adhesive Bandage Fabric 3.8 x 3.8 cm Coverplast Bx/100','14.60','Stevens','30.07','SUTURES AND DRESSINGS','18.99','','In Stock','FALSE','','',''),(53,'195-7260104','BOX','Adhesive Bandage Fabric Patch 5 x 7.2 cm Coverplast Classic Bx/100','28.90','Stevens','31.31','SUTURES AND DRESSINGS','37.95','','In Stock','FALSE','','',''),(54,'195-7260105','BOX','Adhesive Bandage Fabric Fingertip Lrg 4.5 x7.5 cm Coverplast Bx/100','22.60','Stevens','32.52','SUTURES AND DRESSINGS','29.95','','In Stock','FALSE','','',''),(55,'195-7260107','BOX','Dressing Adhesive Fabric Full Width Pad 7.2 X 2.2Cm Bx/100','21.50','Stevens','30.00','SUTURES AND DRESSINGS','27.95','','In Stock','FALSE','','',''),(56,'195-7260120','BOX','Adhesive Bandage Fabric Fingertip Small 4.5 x 5.0 cm Coverplast Bx/50','10.30','Stevens','35.44','SUTURES AND DRESSINGS','13.95','','In Stock','FALSE','','',''),(57,'195-L5530','BOX','Gypsona Slab Plaster Lpl2 12.5Cm X 75Cm L/F Bx/50','48.70','Stevens','31.31','IMMOBILIZATION (CASTING & SPINTING)','63.95','','In Stock','FALSE','','',''),(58,'195-LPL23','BOX','Gypsona Casting Bandage 5 cm X 2.7 m Bx/24','36.40','Stevens','31.73','IMMOBILIZATION (CASTING & SPINTING)','47.95','','In Stock','FALSE','','',''),(59,'195-LPL33','BOX','Gypsona Casting Bandage 7.5 cm x 2.7 m Bx/12','24.30','Stevens','85.19','IMMOBILIZATION (CASTING & SPINTING)','45.00','','In Stock','FALSE','','',''),(60,'195-LPL43','BOX','Gypsona Casting Bandage 10 cm x 2.7 m Bx/12','31.90','Stevens','41.07','IMMOBILIZATION (CASTING & SPINTING)','45.00','','In Stock','FALSE','','',''),(61,'195-LPL63','BOX','Gypsona Casting Bandage 15 cm x 2.7 m Bx/12','46.30','Stevens','31.73','IMMOBILIZATION (CASTING & SPINTING)','60.99','','In Stock','FALSE','','',''),(62,'200-220','CASE','Exam Gown Disposable White 30 X 42in Ca/50','27.20','Stevens','35.99','SUNDRY AND ROOM ITEMS','36.99','','In Stock','FALSE','','',''),(63,'200-50363','CASE','Drape Disposable Fanfold 36X40in White 2 Ply Tissue Ca/100','16.90','Stevens','30.12','SUNDRY AND ROOM ITEMS','21.99','','In Stock','FALSE','','',''),(64,'202-5711101','BOX','Glove Surgeon Latex Powdered Stersensi-Touch Perry 42 White 6 Bx/50Pr','29.80','Stevens','34.06','GLOVES','39.95','','In Stock','FALSE','','',''),(65,'202-5711104','BOX','Glove Surgeon Latex Powdered Stersensi-Touch 42 White 7.5 Bx/50Pr','29.80','Stevens','34.06','GLOVES','39.95','','In Stock','FALSE','','',''),(66,'202-5711105','BOX','Glove Surgeon Latex Powdered Stersensi-Touch Perry 42 White 8 Bx/50Pr','29.80','Stevens','34.06','GLOVES','39.95','','In Stock','FALSE','','',''),(67,'202-782575','BOX','Glove Surgeon Latex Pdr Stersensi-Touch White 7.5 Bx/50Pr','29.80','Stevens','34.06','GLOVES','39.95','','In Stock','FALSE','','',''),(68,'248-LUB-140-X','EACH','Lubricant Gel 140 gm Tube','1.65','Stevens','81.21','PHARMACEUTICALS','2.99','','In Stock','FALSE','','',''),(69,'248-SHP-500','EACH','Peroxide Hydrogen 10 Vol 3% 500ml','1.50','Stevens','99.33','PHARMACEUTICALS','2.99','','In Stock','FALSE','','',''),(70,'263-PG4-1211','BOX','Mask Face Procedure Primagard 80 Earloop Blue Bx/50','3.25','Stevens','115.08','OXYGEN AND AIR WAY','6.99','','In Stock','FALSE','','',''),(71,'263-PM5-630209','CASE','Tape Adhesive Surgical Primasure Cloth Secure 1In X 30Ft Wht Ca/24','56.40','Stevens','32.98','SUTURES AND DRESSINGS','75.00','','In Stock','FALSE','','',''),(72,'310-1645','EACH','Hand Sanitizer Isagel 70% Alcohol 21Oz 621ml W/Pump','7.60','Stevens','30.92','INFECTION CONTROL','9.95','','In Stock','FALSE','','',''),(73,'320-72404','CASE','Water Distilled 4 Litre Ca/4','4.35','Stevens','83.68','REPROCESSING SUPPLIES','7.99','','In Stock','FALSE','','',''),(74,'333-302995','BOX','Syringe Hypo 10Cc L/L Bx/200','46.50','Stevens','31.08','SYRINGES & NEEDLES','60.95','','In Stock','FALSE','','',''),(75,'333-303051','EACH','Sharps Collector 11.3 ltr yellow Horiz Drop Ea','10.10','Stevens','38.12','SHARPS CONTAINER','13.95','','In Stock','FALSE','','',''),(76,'333-305758','BOX','Needle Hypo 27 x 0.5in Eclipse Safety Bx/100','20.11','Stevens','34.01','SYRINGES & NEEDLES','26.95','','In Stock','FALSE','','',''),(77,'333-305767','BOX','Needle Hypo 25 X 1.5In Eclipse Safety Bx/100','20.11','Stevens','34.01','SYRINGES & NEEDLES','26.95','','In Stock','FALSE','','',''),(78,'333-305768','BOX','Needle Hypo 22 X 1In Eclipse Safety Bx/100','20.11','Stevens','34.01','SYRINGES & NEEDLES','26.95','','In Stock','FALSE','','',''),(79,'333-305781','BOX','Syringe & Needle 3cc 25G X 5/8in Safety Bx/50','11.12','Stevens','34.44','SYRINGES & NEEDLES','14.95','','In Stock','FALSE','','',''),(80,'333-305787','BOX','Syringe & Needle 3cc 25G X 1in Safety Bx/50','11.12','Stevens','34.44','SYRINGES & NEEDLES','14.95','','In Stock','FALSE','','',''),(81,'333-305901','BOX','Needle Hypo 25 x 5/8in Safety Bx/50','12.35','Stevens','37.25','SYRINGES & NEEDLES','16.95','','In Stock','FALSE','','',''),(82,'333-305902','BOX','Needle Hypo 23 x 1in Safety Bx/50','13.65','Stevens','31.50','SYRINGES & NEEDLES','17.95','','In Stock','FALSE','','',''),(83,'333-305916','BOX','Needle Hypo 25 x 1in Safety Bx/50','12.35','Stevens','37.25','SYRINGES & NEEDLES','16.95','','In Stock','FALSE','','',''),(84,'333-305918','BOX','Needle Hypo 18 x 1.5in Safety Bx/50','13.65','Stevens','31.50','SYRINGES & NEEDLES','17.95','','In Stock','FALSE','','',''),(85,'333-305950','BOX','Syringe & Needle Allergy 1cc 27 x 0.5in Rb Safety 25/Tray ORDER 40','10.46','Stevens','33.37','SYRINGES & NEEDLES','13.95','','In Stock','FALSE','','',''),(86,'347-9115-02','BOX','Splint Finger Alumafoam 0.5 X 18 in bx/12','17.10','Stevens','34.21','IMMOBILIZATION (CASTING & SPINTING)','22.95','','In Stock','FALSE','','',''),(87,'347-9115-03','BOX','Splint Finger Alumafoam 0.75 x 18 in bx/12','17.10','Stevens','34.21','IMMOBILIZATION (CASTING & SPINTING)','22.95','','In Stock','FALSE','','',''),(88,'355-A1110-BX','BOX','Pad Eye 1-5/8 X 2-5/8In Small Oval Sterile Bx/50','3.90','Stevens','79.23','DIAGNOSTIC TEST & SUPPLIES','6.99','','In Stock','FALSE','','',''),(89,'355-B2800-X','BOX','Sponge Gauze 2 X 2in 8-Ply Sterile ty/50 x 2s','1.50','Stevens','99.33','SUTURES AND DRESSINGS','2.99','','In Stock','FALSE','','',''),(90,'355-B3001-X','BOX','Sponge Gauze 2 X 2in 8-Ply NON STERILE pk/200','0.97','Stevens','157.73','SUTURES AND DRESSINGS','2.50','','In Stock','FALSE','','',''),(91,'355-B3005-X','BOX','Sponge Gauze 4 X 4in 8-Ply NON STERILE pk/200','3.35','Stevens','48.96','SUTURES AND DRESSINGS','4.99','','In Stock','FALSE','','',''),(92,'355-B4800-X','BOX','Sponge Gauze 4 X 4in 8-Ply Sterile ty/50 x 2s','4.05','Stevens','47.90','SUTURES AND DRESSINGS','5.99','','In Stock','FALSE','','',''),(93,'372-6281','EACH','Solution Saline 0.9% Nacl 1000Ml Ster Irrig Screw Cap Bottle','2.55','Stevens','95.69','PHARMACEUTICALS','4.99','','In Stock','FALSE','','',''),(94,'372-6291','EACH','Water Sterile 1000Ml Irrig Bottle Screw Cap','2.45','Stevens','103.67','PHARMACEUTICALS','4.99','','In Stock','FALSE','','',''),(95,'379-Q134B12/150','BAG','Bandage conform 6in x 4 yd bg/6','1.10','Stevens','171.82','IMMOBILIZATION (CASTING & SPINTING)','2.99','','In Stock','FALSE','','',''),(96,'379-Q134B12/50','BOX','Bandage conform 2in x 4.1Yd n/s bx/12','0.85','Stevens','134.12','IMMOBILIZATION (CASTING & SPINTING)','1.99','','In Stock','FALSE','','',''),(97,'379-Q233/100','BAG','Bandage Elastic 4In X 5 Yds Bulk Bg/12','4.65','Stevens','50.32','IMMOBILIZATION (CASTING & SPINTING)','6.99','','In Stock','FALSE','','',''),(98,'379-Q233/100-X','EACH','Bandage Elastic 4 in X 5 yd','0.39','Stevens','117.95','IMMOBILIZATION (CASTING & SPINTING)','0.85','','In Stock','FALSE','','',''),(99,'379-Q233/150','BAG','Bandage Elastic 6In X 5 Yds Bulk Bg/12','6.35','Stevens','41.57','IMMOBILIZATION (CASTING & SPINTING)','8.99','','In Stock','FALSE','','',''),(100,'379-Q233/150-X','EACH','Bandage Elastic 6 in X 5 yd','0.53','Stevens','79.25','IMMOBILIZATION (CASTING & SPINTING)','0.95','','In Stock','FALSE','','',''),(101,'379-Q233/50','BAG','Bandage Elastic 2In X 5 Yd Bulk Bg/12','2.95','Stevens','35.25','IMMOBILIZATION (CASTING & SPINTING)','3.99','','In Stock','FALSE','','',''),(102,'379-Q233/50-X','EACH','Bandage Elastic 2In X 5Yd','0.25','Stevens','200.00','IMMOBILIZATION (CASTING & SPINTING)','0.75','','In Stock','FALSE','','',''),(103,'379-Q233/75','BAG','Bandage Elastic 3In X 5 Yds Bulk Bg/12','3.85','Stevens','55.58','IMMOBILIZATION (CASTING & SPINTING)','5.99','','In Stock','FALSE','','',''),(104,'379-R10/50','EACH','Stockinette Tubular Cotton 2In X 25Yds Non Sterile Orthopedic','4.85','Stevens','44.12','IMMOBILIZATION (CASTING & SPINTING)','6.99','','In Stock','FALSE','','',''),(105,'391-2156-08-CAN00','CASE','Sanitizer Hand Instant Purell Nxt 62% Eth Alch 1000Ml Clear Ca/8','80.90','Stevens','35.97','TOILETRIES','110.00','','In Stock','FALSE','','',''),(106,'391-2156-08-CAN00-X','EACH','Sanitizer Hand Instant Purell Nxt 62% Eth Alch 1000Ml Clear','9.65','Stevens','34.20','TOILETRIES','12.95','','In Stock','FALSE','','',''),(107,'432-L0000009','EACH','Cleanser Chg Stanhexidine Aqueous 2% w/4% iso Alcohol 450ml','5.40','Stevens','47.96','PHARMACEUTICALS','7.99','','In Stock','FALSE','','',''),(108,'467-SW','EACH','Towelette Disinfectant Swipes 160 Per Canister','18.70','Stevens','33.42','INFECTION CONTROL','24.95','','In Stock','FALSE','','',''),(109,'517-10-4100','EACH','Cleaner Instrument Empower Dual Enzy 1Gal Low Foam','40.90','Stevens','34.47','REPROCESSING SUPPLIES','55.00','','In Stock','FALSE','','',''),(110,'517-11-1000','EACH','Disinfectant Hardsurface Cavicide 3.78 Litre','27.00','Stevens','33.33','INFECTION CONTROL','36.00','','In Stock','FALSE','','',''),(111,'517-11-1024','EACH','Disinfectant Hardsurface Cavicide 24Oz Spray Bottle','8.50','Stevens','41.06','INFECTION CONTROL','11.99','','In Stock','FALSE','','',''),(112,'527-1915-100','BOX','Electrode Ecg Fastrace 4 Tape Resting Pk/100','6.99','Stevens','42.92','DIAGNOSTIC TEST & SUPPLIES','9.99','','In Stock','FALSE','','',''),(113,'527-1915-100-CA','BOX','Electrode Ecg Fastrace 4 ca/1000','61.70','Stevens','45.85','DIAGNOSTIC TEST & SUPPLIES','89.99','','In Stock','FALSE','','',''),(114,'549-11008552119','BOX','Urine Test Chemstrip 7 Bx/100','34.80','Stevens','32.04','DIAGNOSTIC TEST & SUPPLIES','45.95','','In Stock','FALSE','','',''),(115,'553-4220-5','BOX','Test Pregnancy Biostrip Bx/25 Bulk - Not Indv Wrapped','25.50','Stevens','44.90','DIAGNOSTIC TEST & SUPPLIES','36.95','','In Stock','FALSE','','',''),(116,'560-1010','BOX','Scalpel Blade #10 S/S Sterile Bx/100','9.85','Stevens','102.94','SUTURES AND DRESSINGS','19.99','','In Stock','FALSE','','',''),(117,'560-1011','BOX','Scalpel Blade #11 S/S Sterile Bx/100','9.85','Stevens','102.94','SUTURES AND DRESSINGS','19.99','','In Stock','FALSE','','',''),(118,'560-1015','BOX','Scalpel Blade #15 S/S Sterile Bx/100','9.85','Stevens','102.94','SUTURES AND DRESSINGS','19.99','','In Stock','FALSE','','',''),(119,'560-1020','BOX','Scalpel Blade #20 S/S Ster Bx/100','9.85','Stevens','102.94','SUTURES AND DRESSINGS','19.99','','In Stock','FALSE','','',''),(120,'589-21376','BOX','Ball Rayon Economy Large 0.60Gram Bg/1000','8.95','Stevens','33.52','SUNDRY AND ROOM ITEMS','11.95','','In Stock','FALSE','','',''),(121,'635-018-300','CASE','Gown Isolation Yellow Univ W/Neck & Waist Ties W/Elastic Cuff Ca/50','40.50','Stevens','30.74','SUNDRY AND ROOM ITEMS','52.95','','In Stock','FALSE','','',''),(122,'635-118-395','BOX','Applicator Silver Nitrate 6in Pk/100','23.90','Stevens','33.68','SUTURES AND DRESSINGS','31.95','','In Stock','FALSE','','',''),(123,'680-405','BOX','Bandage Conform 4in X 4.1yd N/S Bx/12','1.65','Stevens','81.21','SUTURES AND DRESSINGS','2.99','','In Stock','FALSE','','',''),(124,'680-5460','EACH','Bandage Triangular Cotton/Muslin && 40 X 40 x 56In W/2-Pin Indv Pk','0.42','Stevens','102.38','IMMOBILIZATION (CASTING & SPINTING)','0.85','','In Stock','FALSE','','',''),(125,'680-605','BOX','Bandage Conform 6in X 4.1yd N/S Bx/6','1.75','Stevens','70.86','SUTURES AND DRESSINGS','2.99','','In Stock','FALSE','','',''),(126,'691-SG3-03L2238','BOX','Syringe & Needle Hypo 3Cc 22G X 1.5In Safety Surguard Iii Bx/100','25.00','Stevens','31.80','SYRINGES & NEEDLES','32.95','','In Stock','FALSE','','',''),(127,'691-SS05L','BOX','Syringe Hypo 5cc L/L Bx/100','15.30','Stevens','30.39','SYRINGES & NEEDLES','19.95','','In Stock','FALSE','','',''),(128,'714-10692CA','BOX','Drop Eye Minims Fluorescein Sodium 2.0% 0.5Ml Sterile Bx/20','47.70','Stevens','31.97','DIAGNOSTIC TEST & SUPPLIES','62.95','','In Stock','FALSE','','',''),(129,'721-2947455','BOX','Ecg Paper For Schiller/Welch Allyn AT1/2 Pk/175','12.50','Stevens','35.60','DIAGNOSTIC TEST & SUPPLIES','16.95','','In Stock','FALSE','','',''),(130,'745-20-001','BOX','Drape Disp Fenestrated Sterile 18X26In White T/P/T Bx/50','10.40','Stevens','34.13','SUTURES AND DRESSINGS','13.95','','In Stock','FALSE','','',''),(131,'759-01.57.107451','BOX','Paper Ecg Edan Se12 & Se1200 Series Z Fold Pk/100 - **BUCC West ONLY**','15.99','Stevens','31.02','DIAGNOSTIC TEST & SUPPLIES','20.95','','In Stock','FALSE','','',''),(132,'784-0344015','EACH','Ointment Polysporin 30 gm Tube','10.30','Stevens','35.83','PHARMACEUTICALS','13.99','','In Stock','FALSE','','',''),(133,'800-1527-1','BOX','Tape Adhesive Transpore 1 in X 10 Yd clear Porous Bx/12','12.60','Stevens','34.52','SUTURES AND DRESSINGS','16.95','','In Stock','FALSE','','',''),(134,'800-1530-1','BOX','Tape Adhesive Micropore 1 in X 10 Yd Bx/12','8.45','Stevens','30.06','SUTURES AND DRESSINGS','10.99','','In Stock','FALSE','','',''),(135,'800-8210','BOX','Mask Face Respirator N-95 White Bx/20','17.40','Stevens','31.90','OXYGEN AND AIR WAY','22.95','','In Stock','FALSE','','',''),(136,'800-DS-5','BOX','Skin Stapler Precise 5 Shot bx/12','103.55','Stevens','32.25','SUTURES AND DRESSINGS','136.95','','In Stock','FALSE','','',''),(137,'800-R1541','BOX','Skin Closure Adhesive Steri-Strip 0.25 x 3in Bx/50 RED','44.20','Stevens','31.11','SUTURES AND DRESSINGS','57.95','','In Stock','FALSE','','',''),(138,'800-R1542','BOX','Skin Closure Adhesive Steri-Strip 0.25 x 1.5in Bx/50 GREEN','40.40','Stevens','31.06','SUTURES AND DRESSINGS','52.95','','In Stock','FALSE','','',''),(139,'800-SR-1','BOX','Remover Staple Skin Regular Precise Disp Tweezer Style Bx/10','47.60','Stevens','68.05','SUTURES AND DRESSINGS','79.99','','In Stock','FALSE','','',''),(140,'800-SR-1-X','EACH','Skin Staple Remover Regular Precise Tweezer Style','4.80','Stevens','66.46','SUTURES AND DRESSINGS','7.99','','In Stock','FALSE','','',''),(141,'850-31925','CASE','Underpad Disposable 17 X 24in Dri-Sorb Blue Ca/30X10s','39.50','Stevens','31.52','SUTURES AND DRESSINGS','51.95','','In Stock','FALSE','','',''),(142,'887-AA01','EACH','Cautery Hi-Temp Surgical/Fine Tip Ster 2200F d disp','55.00','Stevens','75.26','SUTURES AND DRESSINGS','71.50','','In Stock','FALSE','','',''),(143,'887-H101','BOX','Tip Cautery Hi-Temp Fine Sterile 2200Yf deg for HIT1 Bx/10','49.95','Stevens','30.03','SUTURES AND DRESSINGS','64.95','','In Stock','FALSE','','',''),(144,'887-HIT1','EACH','Cautery Hi-Temp Change-A-Tip System W/H101 N/S Tip','39.95','Stevens','30.04','SUTURES AND DRESSINGS','51.95','','In Stock','FALSE','','',''),(145,'963-551B','BOX','Suture Gut Plain 4-0 27In C6 bx/12','36.00','Stevens','38.86','SUTURES AND DRESSINGS','49.99','','In Stock','FALSE','','',''),(146,'963-553B','BOX','Suture Gut Plain 3-0 27In C7 Bx/12','36.50','Stevens','36.96','SUTURES AND DRESSINGS','49.99','','In Stock','FALSE','','',''),(147,'963-592B','BOX','Suture Gut Plain 3-0 18In C6 Bx/12','55.90','Stevens','30.50','SUTURES AND DRESSINGS','72.95','','In Stock','FALSE','','',''),(148,'963-916B','BOX','Suture Nylon Mono Blk 6-0 18In C17 Bx/12','35.60','Stevens','40.42','SUTURES AND DRESSINGS','49.99','','In Stock','FALSE','','',''),(149,'963-917B','BOX','Suture Nylon Mono Blk 5-0 18In C17 Bx/12','38.20','Stevens','30.86','SUTURES AND DRESSINGS','49.99','','In Stock','FALSE','','',''),(150,'963-918B','BOX','Suture Nylon Mono Blk 5-0 18In C6 Bx/12','37.10','Stevens','34.74','SUTURES AND DRESSINGS','49.99','','In Stock','FALSE','','',''),(151,'963-921B','BOX','Suture Nylon Mono Blk 4-0 18In C17 Bx/12','37.30','Stevens','34.02','SUTURES AND DRESSINGS','49.99','','In Stock','FALSE','','',''),(152,'963-922B','BOX','Suture Nylon Mono Blk 4-0 18In C6 Bx/12','36.10','Stevens','38.48','SUTURES AND DRESSINGS','49.99','','In Stock','FALSE','','',''),(153,'963-925B','BOX','Suture Nylon Mono Blk 3-0 18In C7 bx/12','35.50','Stevens','40.82','SUTURES AND DRESSINGS','49.99','','In Stock','FALSE','','',''),(154,'963-928B','BOX','Suture Nylon Mono Blk 3-0 18In C6 bx/12','36.00','Stevens','38.86','SUTURES AND DRESSINGS','49.99','','In Stock','FALSE','','',''),(155,'975-632112923','EACH','Deodorizer Room Citrus Ii Original Blend 5.2Fl Oz','9.50','Stevens','36.32','TOILETRIES','12.95','','In Stock','FALSE','','',''),(156,'975-632112924','EACH','Deodorizer Room Citrus Ii Natural Lemon 7fl Oz (7751)','9.65','Stevens','34.20','TOILETRIES','12.95','','In Stock','FALSE','','',''),(157,'991-1012SC','EACH','Cannula Oxygen Nasal Adult Soft Cvd W/7Ft Sure Flow Tubing','0.60','Stevens','58.33','OXYGEN AND AIR WAY','0.95','','In Stock','FALSE','','',''),(158,'991-1041','EACH','Mask Oxygen Med Conc Adlt Elong- Ated W/7Ft Sure-Flow Tubing','1.05','Stevens','85.71','OXYGEN AND AIR WAY','1.95','','In Stock','FALSE','','',''),(159,'991-1043','EACH','Mask Oxygen Med Conc Paed Elongated W/7Ft Sure-Flow Tubing','1.05','Stevens','85.71','OXYGEN AND AIR WAY','1.95','','In Stock','FALSE','','',''),(160,'991-GL105','EACH','Gauze Tubular Surgitube #1 5/8in X 5 Yds Small Finger/Toe','2.75','Stevens','43.64','IMMOBILIZATION (CASTING & SPINTING)','3.95','','In Stock','FALSE','','',''),(161,'991-GL220','EACH','Gauze Tubular Surgitube 12 1in X 50Yds Large Finger/Toe','11.30','Stevens','32.30','IMMOBILIZATION (CASTING & SPINTING)','14.95','','In Stock','FALSE','','',''),(162,'991-GL231','EACH','Applicator Metal Cage Sz 1 For Gl219/Gl150','32.79','Stevens','30.99','IMMOBILIZATION (CASTING & SPINTING)','42.95','','In Stock','FALSE','','',''),(163,'991-GL232','EACH','Applicator Metal Cage Sz 2 F/Gl220 Gl250/Glb10','35.99','Stevens','30.45','IMMOBILIZATION (CASTING & SPINTING)','46.95','','In Stock','FALSE','','',''),(164,'100-1001','EACH','Optibond Solo Plus Btl 6Ml (34614)','32.34','Kerr','131.88','BONDS- ADHESIVE','74.99','','In Stock','FALSE','','',''),(165,'100-1002','EACH','3M Adper Single Bond  6G Bottle (51202)','52.14','3M','34.23','BONDS- ADHESIVE','69.99','','In Stock','FALSE','','',''),(166,'100-1003','EACH','Prime & Bond 3.5Ml Bottle (60667273)','46.86','Dentsply','38.69','BONDS- ADHESIVE','64.99','','In Stock','FALSE','','',''),(167,'100-1004','EACH','Gluma Desensitizer 5Ml Bottle(66003764)','49.50','Kulzer','41.39','BONDS- ADHESIVE','69.99','','In Stock','FALSE','','',''),(168,'100-1005','BOX','Gluma  Bond & Desensitizer 4Ml Btl + 50 Tips (Gluma2) (66040972)','77.22','Kulzer','16.54','BONDS- ADHESIVE','89.99','','In Stock','FALSE','','',''),(169,'100-1006','BOX','Scotchbond 8Ml Bottle- Primer 3008/ Adhesive 3009','32.34','3M','100.96','BONDS- ADHESIVE','64.99','','In Stock','FALSE','','',''),(170,'100-1007','BOX','Optibond Fl Adhesive 8Ml. (25882)/ 25881-Primer','69.89','Kerr','35.91','BONDS- ADHESIVE','94.99','','In Stock','FALSE','','',''),(171,'100-1008','BOX','Filtek Z-100 Syringes 4G.  8004 - A1-A3.5','26.33','3M','70.84','COMPOSITE- SYRINGES','44.99','','In Stock','FALSE','','',''),(172,'100-1009','BOX',' Filtex Z-250 Syringes  4G. 1370 A1-A3.5','32.93','3M','51.79','COMPOSITE- SYRINGES','49.99','','In Stock','FALSE','','',''),(173,'100-1010','BOX','Herculite Xrv Syringes 4G. Enamel 22859-22862 A1-A3.5','38.21','Kerr','109.32','COMPOSITE- SYRINGES','79.99','','In Stock','FALSE','','',''),(174,'100-1011','BOX','Filtek Supreme Ultra Syringes 4G. A1B- A3.5B 6028','104.94','3M','23.87','COMPOSITE- SYRINGES','129.99','','In Stock','FALSE','','',''),(175,'100-1012','BOX','3M Filtek P60 Syringes 4G. A3/ B2 (8100)','29.70','3M','68.32','COMPOSITE- SYRINGES','49.99','','In Stock','FALSE','','',''),(176,'100-1013','BOX','\"Filtek Z-100 Unidose, 18X0.2G. 5905- A1-A3.5\"','51.41','3M','55.58','COMPOSITE- UNIDOSE','79.99','','In Stock','FALSE','','',''),(177,'100-1014','BOX','\" Filtex Z-250 Unidose, 20X0.2G. 6021- A1-A3.5\"','69.30','3M','29.86','COMPOSITE- UNIDOSE','89.99','','In Stock','FALSE','','',''),(178,'100-1015','BOX','\"Herculite Xrv Unidose, 20X0.2G. A1 Enamel Us Pack  (29835)\"','46.13','Kerr','73.39','COMPOSITE- UNIDOSE','79.99','','In Stock','FALSE','','',''),(179,'100-1016','BOX','\"Filtek Supreme Ultra Capsules, 20X0.2G.  A1B-A3.5B 6029\"','107.58','3M','20.83','COMPOSITE- UNIDOSE','129.99','','In Stock','FALSE','','',''),(180,'100-1017','BOX','\"Filtek Z350 Flowable Syringe (7032A1)- A1-A3.5, 2X2G.\"','49.50','3M','55.54','COMPOSITE- FLOWABLE','76.99','','In Stock','FALSE','','',''),(181,'100-1018','BOX','Revolution 2  4 X 1G Syringe A1 (29493-6-A1-A3.5','42.90','Kerr','60.82','COMPOSITE- FLOWABLE','68.99','','In Stock','FALSE','','',''),(182,'100-1019','BOX','Starflow 1X 5G Syringe A1-A3.5 (85051)','37.62','Danville','86.04','COMPOSITE- FLOWABLE','69.99','','In Stock','FALSE','','',''),(183,'100-1020','BOX','\"Filtek Bulk Fill Syringe, 4G. A2/ A3 (4863A2)\"','77.81','3M','41.35','COMPOSITE- BULK FILL','109.99','','In Stock','FALSE','','',''),(184,'100-1021','BOX','\"Filtek Bulk Fill Capsules, 20X0.2G. A2/ A3 (4864A2)\"','77.81','3M','41.35','COMPOSITE- BULK FILL','109.99','','In Stock','FALSE','','',''),(185,'100-1022','BOX','Filtek Bulk Fill A2 Flowable 2X 2G  4862 A2/ A3','75.17','3M','46.31','COMPOSITE- BULK FILL','109.99','','In Stock','FALSE','','',''),(186,'100-1023','BOX','\"Enhance Finishers, 30/Pk: Cups (624055)/ Pts (624065)/ Disc (624045)\"','60.72','Dentsply','39.97','FINISHERS','84.99','','In Stock','FALSE','','',''),(187,'100-1024','BOX','3M (85 Pk) Soflex-  85/Pk- 1981/1982/2381/2382- C/M/F/Sf','31.61','3M','58.13','FINISHERS','49.99','','In Stock','FALSE','','',''),(188,'100-1025','BOX','Soflex Finishing Strips (1954)/ 1954N- 150/Pk','32.34','3M','54.58','FINISHERS','49.99','','In Stock','FALSE','','',''),(189,'100-1026','BOX','\"Vitrebond Kit (7510), 9G. Powder+ 5.5Ml. Liquid\"','77.22','3M','16.54','CEMENTS AND LINERS','89.99','','In Stock','FALSE','','',''),(190,'100-1027','BOX','\"Vitrebond Liquid 3M  (7512L), 5.5Ml.\"','52.14','3M','34.23','CEMENTS AND LINERS','69.99','','In Stock','FALSE','','',''),(191,'100-1028','BOX','\"Rely X Luting Kit (3515), 16G. Powder+9Ml. Liq.\"','78.54','3M','33.68','CEMENTS AND LINERS','104.99','','In Stock','FALSE','','',''),(192,'100-1029','BOX','\"Ketac Cem Single Kit 3M Espe (37200), 33G. Powder +12Ml. Liquid\"','55.44','3M','53.30','CEMENTS AND LINERS','84.99','','In Stock','FALSE','','',''),(193,'100-1030','BOX','Maxcem Elite Clear (33872)/ White 33873/- 2X 5G.','63.36','Kerr','49.92','CEMENTS AND LINERS','94.99','','In Stock','FALSE','','',''),(194,'100-1031','BOX','\"Express Putty (7312), 305Ml. Each Of Base And Catalyst\"','75.17','3M','26.36','IMPRESSION MATERIAL','94.99','','In Stock','FALSE','','',''),(195,'100-1032','BOX','Spongostan Dental Ethicon 1X1X1 (24Pk) (Ms0005)','31.02','J & J','61.15','OTHERS-','49.99','','In Stock','FALSE','','',''),(196,'100-1033','BOX','Kavo Spray 500Ml (411-9660)','34.98','Kavo','71.50','OTHERS-','59.99','','In Stock','FALSE','','',''),(197,'100-1034','BOX','EHS 24hr Test bx/100','79.20','Teroogen','120.96','BIOLOGICAL INDICATORS','175.00','','In Stock','FALSE','','','');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;