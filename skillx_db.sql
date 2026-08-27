-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: skillx_db
-- ------------------------------------------------------
-- Server version	8.0.46

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
-- Current Database: `skillx_db`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `skillx_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `skillx_db`;

--
-- Table structure for table `bookings`
--

DROP TABLE IF EXISTS `bookings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bookings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `skill_id` int NOT NULL,
  `learner_id` int NOT NULL,
  `session_date` date NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `status` varchar(20) NOT NULL,
  `cancel_reason` varchar(255) DEFAULT NULL,
  `meeting_link` varchar(500) DEFAULT NULL,
  `booked_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `skill_id` (`skill_id`),
  KEY `learner_id` (`learner_id`),
  KEY `ix_bookings_id` (`id`),
  CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`skill_id`) REFERENCES `skills` (`id`),
  CONSTRAINT `bookings_ibfk_2` FOREIGN KEY (`learner_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookings`
--

LOCK TABLES `bookings` WRITE;
/*!40000 ALTER TABLE `bookings` DISABLE KEYS */;
INSERT INTO `bookings` VALUES (1,1,3,'2026-07-01','13:00:00','15:00:00','completed',NULL,NULL,'2026-08-07 04:22:48'),(2,2,4,'2026-07-18','09:30:00','11:00:00','pending',NULL,NULL,'2026-08-07 04:22:48'),(3,1,3,'2026-07-08','14:00:00','15:30:00','completed',NULL,NULL,'2026-08-07 04:22:48'),(4,1,3,'2026-07-15','14:00:00','15:30:00','completed',NULL,NULL,'2026-08-07 04:22:48'),(5,1,3,'2026-07-22','14:00:00','15:30:00','completed',NULL,NULL,'2026-08-07 04:22:48'),(6,2,2,'2026-08-13','09:00:00','10:00:00','confirmed',NULL,NULL,'2026-08-07 13:25:27');
/*!40000 ALTER TABLE `bookings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `certificates`
--

DROP TABLE IF EXISTS `certificates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `certificates` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `certificate_code` varchar(50) NOT NULL,
  `sessions_completed` int NOT NULL,
  `issued_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `certificate_code` (`certificate_code`),
  KEY `student_id` (`student_id`),
  KEY `ix_certificates_id` (`id`),
  CONSTRAINT `certificates_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `certificates`
--

LOCK TABLES `certificates` WRITE;
/*!40000 ALTER TABLE `certificates` DISABLE KEYS */;
/*!40000 ALTER TABLE `certificates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `complaints`
--

DROP TABLE IF EXISTS `complaints`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `complaints` (
  `id` int NOT NULL AUTO_INCREMENT,
  `submitted_by` int NOT NULL,
  `subject` varchar(150) NOT NULL,
  `message` varchar(1000) NOT NULL,
  `status` varchar(20) NOT NULL,
  `admin_response` varchar(1000) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `resolved_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `submitted_by` (`submitted_by`),
  KEY `ix_complaints_id` (`id`),
  CONSTRAINT `complaints_ibfk_1` FOREIGN KEY (`submitted_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `complaints`
--

LOCK TABLES `complaints` WRITE;
/*!40000 ALTER TABLE `complaints` DISABLE KEYS */;
INSERT INTO `complaints` VALUES (1,4,'Session materials never shared','My tutor said they would send prep notes before the session but I never received anything.','open',NULL,'2026-08-07 04:22:49',NULL),(2,5,'Wireframing','The meeting link was never sent.','resolved','The session will be replaced very soon. Thanks for your understanding.','2026-08-07 13:32:02','2026-08-07 13:32:47');
/*!40000 ALTER TABLE `complaints` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback` (
  `id` int NOT NULL AUTO_INCREMENT,
  `booking_id` int NOT NULL,
  `given_by` int NOT NULL,
  `given_to` int NOT NULL,
  `rating` int NOT NULL,
  `comments` varchar(500) DEFAULT NULL,
  `submitted_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_feedback_once_per_reviewer` (`booking_id`,`given_by`),
  KEY `given_by` (`given_by`),
  KEY `given_to` (`given_to`),
  KEY `ix_feedback_id` (`id`),
  CONSTRAINT `feedback_ibfk_1` FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`id`),
  CONSTRAINT `feedback_ibfk_2` FOREIGN KEY (`given_by`) REFERENCES `users` (`id`),
  CONSTRAINT `feedback_ibfk_3` FOREIGN KEY (`given_to`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback`
--

LOCK TABLES `feedback` WRITE;
/*!40000 ALTER TABLE `feedback` DISABLE KEYS */;
INSERT INTO `feedback` VALUES (1,1,3,2,5,'Explained React state perfectly. Recommended!','2026-08-07 04:22:48');
/*!40000 ALTER TABLE `feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `message` varchar(255) NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `sent_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_notifications_id` (`id`),
  CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications`
--

LOCK TABLES `notifications` WRITE;
/*!40000 ALTER TABLE `notifications` DISABLE KEYS */;
INSERT INTO `notifications` VALUES (1,2,'Your skill \'ReactJS Development\' was approved.',0,'2026-08-07 04:22:48'),(2,3,'Reminder: your ReactJS session is coming up.',0,'2026-08-07 04:22:48'),(3,3,'New booking request from Aung Kyaw Min for \'Figma Wireframing\'.',0,'2026-08-07 13:25:27'),(4,2,'Your booking for \'Figma Wireframing\' is now confirmed.',0,'2026-08-07 13:25:58'),(5,5,'Your complaint \'Wireframing\' has been resolved.',0,'2026-08-07 13:32:47'),(6,5,'Your skill \'Data Science for Beginners\' was approved by the administrator.',0,'2026-08-07 13:36:03');
/*!40000 ALTER TABLE `notifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `password_reset_requests`
--

DROP TABLE IF EXISTS `password_reset_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `password_reset_requests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `status` varchar(20) NOT NULL,
  `requested_at` datetime DEFAULT NULL,
  `approved_at` datetime DEFAULT NULL,
  `completed_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `ix_password_reset_requests_id` (`id`),
  CONSTRAINT `password_reset_requests_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `password_reset_requests`
--

LOCK TABLES `password_reset_requests` WRITE;
/*!40000 ALTER TABLE `password_reset_requests` DISABLE KEYS */;
/*!40000 ALTER TABLE `password_reset_requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `skill_categories`
--

DROP TABLE IF EXISTS `skill_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `skill_categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_skill_categories_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `skill_categories`
--

LOCK TABLES `skill_categories` WRITE;
/*!40000 ALTER TABLE `skill_categories` DISABLE KEYS */;
INSERT INTO `skill_categories` VALUES (1,'Web Development','Frontend and backend web technologies.'),(2,'Data Science','Data analysis, statistics and machine learning.'),(3,'Design & UX','UI/UX design, wireframing and design tools.'),(4,'Languages','Spoken and written language practice.'),(5,'Soft Skills','Communication, presentation and teamwork.');
/*!40000 ALTER TABLE `skill_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `skill_materials`
--

DROP TABLE IF EXISTS `skill_materials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `skill_materials` (
  `id` int NOT NULL AUTO_INCREMENT,
  `skill_id` int NOT NULL,
  `file_name` varchar(255) NOT NULL,
  `stored_path` varchar(255) NOT NULL,
  `uploaded_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `skill_id` (`skill_id`),
  KEY `ix_skill_materials_id` (`id`),
  CONSTRAINT `skill_materials_ibfk_1` FOREIGN KEY (`skill_id`) REFERENCES `skills` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `skill_materials`
--

LOCK TABLES `skill_materials` WRITE;
/*!40000 ALTER TABLE `skill_materials` DISABLE KEYS */;
INSERT INTO `skill_materials` VALUES (1,1,'react-hooks-cheatsheet.md','skill1_seed_notes.md','2026-08-07 04:22:48'),(2,2,'Set A - PTSA1 Instruction Question.docx','skill2_ebd21507.docx','2026-08-07 13:22:55');
/*!40000 ALTER TABLE `skill_materials` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `skills`
--

DROP TABLE IF EXISTS `skills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `skills` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tutor_id` int NOT NULL,
  `category_id` int NOT NULL,
  `approved_by` int DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `description` varchar(500) DEFAULT NULL,
  `proficiency` varchar(20) DEFAULT NULL,
  `session_duration_minutes` int DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `date_listed` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tutor_id` (`tutor_id`),
  KEY `category_id` (`category_id`),
  KEY `approved_by` (`approved_by`),
  KEY `ix_skills_id` (`id`),
  CONSTRAINT `skills_ibfk_1` FOREIGN KEY (`tutor_id`) REFERENCES `users` (`id`),
  CONSTRAINT `skills_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `skill_categories` (`id`),
  CONSTRAINT `skills_ibfk_3` FOREIGN KEY (`approved_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `skills`
--

LOCK TABLES `skills` WRITE;
/*!40000 ALTER TABLE `skills` DISABLE KEYS */;
INSERT INTO `skills` VALUES (1,2,1,1,'ReactJS Development','Modern single-page apps with hooks and context.','advanced',90,'approved','2026-08-07 04:22:48'),(2,3,3,1,'Figma Wireframing','High-fidelity prototypes and UI component libraries.','intermediate',60,'approved','2026-08-07 04:22:48'),(3,4,2,NULL,'Python Data Analysis with Pandas','EDA, data cleaning and visualisation.','intermediate',60,'pending','2026-08-07 04:22:48'),(4,5,2,1,'Data Science for Beginners','Blah Blah','intermediate',60,'approved','2026-08-07 13:35:27');
/*!40000 ALTER TABLE `skills` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tutor_availability`
--

DROP TABLE IF EXISTS `tutor_availability`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tutor_availability` (
  `id` int NOT NULL AUTO_INCREMENT,
  `skill_id` int NOT NULL,
  `day_of_week` int NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  PRIMARY KEY (`id`),
  KEY `skill_id` (`skill_id`),
  KEY `ix_tutor_availability_id` (`id`),
  CONSTRAINT `tutor_availability_ibfk_1` FOREIGN KEY (`skill_id`) REFERENCES `skills` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tutor_availability`
--

LOCK TABLES `tutor_availability` WRITE;
/*!40000 ALTER TABLE `tutor_availability` DISABLE KEYS */;
INSERT INTO `tutor_availability` VALUES (1,1,2,'14:00:00','17:00:00'),(2,1,6,'10:00:00','12:00:00'),(3,2,4,'09:00:00','11:00:00');
/*!40000 ALTER TABLE `tutor_availability` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(20) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `bio` varchar(500) DEFAULT NULL,
  `profile_picture` varchar(255) DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_users_email` (`email`),
  KEY `ix_users_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Zaw Myo Htet','admin@skillx-demo.com','$2b$12$2YUq64hEPkyAOAhtAZ2wCeQ41hy2N/zMR6ndNhJ2i8/mHGu1ejEV2','admin',NULL,NULL,NULL,'active','2026-08-07 04:22:48'),(2,'Aung Kyaw Min','aungkyaw@skillx-demo.com','$2b$12$92hkDHNQDupShhe2KJ7.AuFG5TFwAH2giA344r5rs6NuQRlIKZpNC','student',NULL,'Computer Science major interested in Web Development.',NULL,'active','2026-08-07 04:22:48'),(3,'Thiri San','thirisan@skillx-demo.com','$2b$12$7dkq.HIPVOrXkwLbQsvLgOohyXwEcnXVfqoEjne9jJRVndIFuowhG','student',NULL,'UX/UI Design student who loves building interfaces.',NULL,'active','2026-08-07 04:22:48'),(4,'Hsu Myat Noe','hsumyat@skillx-demo.com','$2b$12$9NnK0TPpl0CUX/IjEVP8H.RfTXh2/XZsFUwcZpIIBsGi2nUbOR/i6','student',NULL,'Data Science enthusiast passionate about ML.',NULL,'active','2026-08-07 04:22:48'),(5,'Lu Min Han','hanlumin@skillx.com','$2b$12$GdHwJYYu.2JiGahAqJNsFOUmljHK5kk.qZX0Ins2pr3GfzuKrqulS','student',NULL,'fslkjfjsdlkf',NULL,'active','2026-08-07 13:30:40');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'skillx_db'
--

--
-- Dumping routines for database 'skillx_db'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-10  4:38:00
