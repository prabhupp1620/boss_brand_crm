-- MariaDB dump 10.19  Distrib 10.4.22-MariaDB, for Win64 (AMD64)
--
-- Host: 127.0.0.1    Database: boss_brand
-- ------------------------------------------------------
-- Server version	10.4.24-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `boss_brand`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `boss_brand` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `boss_brand`;

--
-- Table structure for table `branding_methods`
--

DROP TABLE IF EXISTS `branding_methods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `branding_methods` (
  `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `slug` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `form_label` varchar(80) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sort_order` smallint(5) unsigned NOT NULL DEFAULT 0,
  `is_active` tinyint(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_branding_slug` (`slug`),
  UNIQUE KEY `uq_branding_label` (`form_label`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `branding_methods`
--

LOCK TABLES `branding_methods` WRITE;
/*!40000 ALTER TABLE `branding_methods` DISABLE KEYS */;
/*!40000 ALTER TABLE `branding_methods` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `collections`
--

DROP TABLE IF EXISTS `collections`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `collections` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `slug` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tagline` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `image_url` varchar(512) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `garment` enum('round-neck','full-sleeve','oversized','polo','hoodie','sweatshirt','jacket','formal-shirt','cap','tote','mug','bottle','kit-box') COLLATE utf8mb4_unicode_ci NOT NULL,
  `moq` int(10) unsigned NOT NULL DEFAULT 50,
  `starting_price_override` decimal(10,2) unsigned DEFAULT NULL,
  `sku_count_override` int(10) unsigned DEFAULT NULL,
  `sort_order` smallint(5) unsigned NOT NULL DEFAULT 0,
  `is_active` tinyint(1) NOT NULL DEFAULT 1,
  `seo_title` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `seo_description` varchar(400) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `crm_id` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_collections_slug` (`slug`),
  UNIQUE KEY `uq_collections_crm_id` (`crm_id`),
  KEY `idx_collections_listing` (`is_active`,`sort_order`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `collections`
--

LOCK TABLES `collections` WRITE;
/*!40000 ALTER TABLE `collections` DISABLE KEYS */;
INSERT INTO `collections` VALUES (1,'corporate-t-shirts','Corporate T-Shirts','Round neck, polo, full-sleeve and oversized — 110 to 220 GSM','/products/collection-corporate-t-shirts.webp','round-neck',50,45.00,68,1,1,NULL,NULL,NULL,'2026-08-29 10:48:41','2026-08-29 10:48:41'),(2,'hoodies-sweatshirts-jackets','Hoodies, Sweatshirts & Jackets','Fleece-backed and brushed interiors, 320 to 420 GSM','/products/collection-hoodies-sweatshirts-jackets.webp','hoodie',50,289.00,42,2,1,NULL,NULL,NULL,'2026-08-29 10:48:41','2026-08-29 10:48:41'),(3,'corporate-uniforms','Corporate Uniforms','Formal shirts, blazers, aprons and front-of-house workwear','/products/collection-corporate-uniforms.webp','formal-shirt',100,196.00,54,3,1,NULL,NULL,NULL,'2026-08-29 10:48:41','2026-08-29 10:48:41'),(4,'caps-accessories','Caps & Accessories','6-panel, snapback, bucket hats, lanyards and socks','/products/collection-caps-accessories.webp','cap',100,54.00,37,4,1,NULL,NULL,NULL,'2026-08-29 10:48:41','2026-08-29 10:48:41'),(5,'corporate-gifting','Corporate Gifting','Drinkware, desk objects and curated festive hampers','/products/collection-corporate-gifting.webp','mug',25,119.00,96,5,1,NULL,NULL,NULL,'2026-08-29 10:48:41','2026-08-29 10:48:41'),(6,'employee-welcome-kits','Employee Welcome Kits','Day-one boxes assembled, branded and shipped to the desk','/products/collection-employee-welcome-kits.webp','kit-box',25,329.00,18,6,1,NULL,NULL,NULL,'2026-08-29 10:48:41','2026-08-29 10:48:41'),(7,'event-team-merchandise','Event & Team Merchandise','Jerseys, crew tees and lanyards for offsites and launches','/products/collection-event-team-merchandise.webp','oversized',50,86.00,44,7,1,NULL,NULL,NULL,'2026-08-29 10:48:41','2026-08-29 10:48:41'),(8,'promotional-merchandise','Promotional Merchandise','Totes, bottles and giveaways built for high-volume campaigns','/products/collection-promotional-merchandise.webp','tote',250,29.00,61,8,1,NULL,NULL,NULL,'2026-08-29 10:48:41','2026-08-29 10:48:41');
/*!40000 ALTER TABLE `collections` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `colours`
--

DROP TABLE IF EXISTS `colours`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `colours` (
  `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `hex` char(7) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sort_order` smallint(5) unsigned NOT NULL DEFAULT 0,
  `is_active` tinyint(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_colours_name` (`name`),
  CONSTRAINT `ck_colours_hex` CHECK (`hex` regexp '^#[0-9a-fA-F]{6}$')
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `colours`
--

LOCK TABLES `colours` WRITE;
/*!40000 ALTER TABLE `colours` DISABLE KEYS */;
INSERT INTO `colours` VALUES (1,'White','#ffffff',10,1),(2,'Black','#17171b',20,1),(3,'Navy','#1e2a4a',30,1),(4,'Charcoal','#3a3a42',40,1),(5,'Heather Grey','#b9bcc2',50,1),(6,'Steel','#9ba3ab',60,1),(7,'Sky','#a8c8e8',70,1),(8,'Royal Blue','#1f4fa8',80,1),(9,'Bottle Green','#14513a',90,1),(10,'Olive','#5c6347',100,1),(11,'Maroon','#6d1f2c',110,1),(12,'Terracotta','#b4553a',120,1),(13,'Mustard','#d99b2b',130,1),(14,'Beige','#d8c7ad',140,1),(15,'Natural','#ded3bd',150,1),(16,'Kraft','#c69c6d',160,1);
/*!40000 ALTER TABLE `colours` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contact_requests`
--

DROP TABLE IF EXISTS `contact_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contact_requests` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `reference` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `company` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `message` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(40) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `topic_id` smallint(5) unsigned DEFAULT NULL,
  `topic_label` varchar(80) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `intent` varchar(60) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` enum('new','in-review','replied','closed','spam') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'new',
  `status_note` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `assigned_to` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `replied_at` datetime DEFAULT NULL,
  `source_page` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `referrer` varchar(512) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `utm_source` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `utm_medium` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `utm_campaign` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ip_address` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_agent` varchar(512) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `crm_id` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_contact_reference` (`reference`),
  UNIQUE KEY `uq_contact_crm_id` (`crm_id`),
  KEY `idx_contact_status_created` (`status`,`created_at`),
  KEY `idx_contact_email` (`email`),
  KEY `idx_contact_created` (`created_at`),
  KEY `idx_contact_intent` (`intent`),
  KEY `idx_contact_topic` (`topic_id`),
  CONSTRAINT `fk_contact_topic` FOREIGN KEY (`topic_id`) REFERENCES `contact_topics` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contact_requests`
--

LOCK TABLES `contact_requests` WRITE;
/*!40000 ALTER TABLE `contact_requests` DISABLE KEYS */;
/*!40000 ALTER TABLE `contact_requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contact_topics`
--

DROP TABLE IF EXISTS `contact_topics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contact_topics` (
  `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `slug` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `form_label` varchar(80) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sort_order` smallint(5) unsigned NOT NULL DEFAULT 0,
  `is_active` tinyint(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_contact_topic_slug` (`slug`),
  UNIQUE KEY `uq_contact_topic_label` (`form_label`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contact_topics`
--

LOCK TABLES `contact_topics` WRITE;
/*!40000 ALTER TABLE `contact_topics` DISABLE KEYS */;
INSERT INTO `contact_topics` VALUES (1,'bulk-order','Bulk order enquiry','Bulk order enquiry',10,1),(2,'corporate-gifting','Corporate gifting','Corporate gifting',20,1),(3,'custom-uniforms','Custom uniforms','Custom uniforms',30,1),(4,'branding','Branding solutions','Branding solutions',40,1),(5,'existing-order','Existing order','Existing order',50,1),(6,'other','Something else','Something else',60,1),(7,'factory-call','Factory call',NULL,70,1);
/*!40000 ALTER TABLE `contact_topics` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_colours`
--

DROP TABLE IF EXISTS `product_colours`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_colours` (
  `product_id` int(10) unsigned NOT NULL,
  `colour_id` smallint(5) unsigned NOT NULL,
  `sort_order` smallint(5) unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY (`product_id`,`colour_id`),
  KEY `idx_product_colours_order` (`product_id`,`sort_order`),
  KEY `idx_product_colours_colour` (`colour_id`),
  CONSTRAINT `fk_product_colours_colour` FOREIGN KEY (`colour_id`) REFERENCES `colours` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_product_colours_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_colours`
--

LOCK TABLES `product_colours` WRITE;
/*!40000 ALTER TABLE `product_colours` DISABLE KEYS */;
INSERT INTO `product_colours` VALUES (1,1,10),(1,2,20),(1,3,30),(1,5,50),(1,8,80),(1,9,90),(1,11,110),(1,13,130),(2,1,10),(2,2,20),(2,3,30),(2,5,50),(2,8,80),(2,9,90),(2,11,110),(2,13,130),(3,1,10),(3,2,20),(3,3,30),(3,5,50),(3,8,80),(3,9,90),(3,11,110),(3,13,130),(4,1,10),(4,2,20),(4,3,30),(4,5,50),(4,8,80),(4,9,90),(4,11,110),(4,13,130),(5,1,10),(5,2,20),(5,3,30),(5,5,50),(5,8,80),(5,9,90),(5,11,110),(5,13,130),(7,1,10),(7,2,20),(7,3,30),(7,5,50),(7,8,80),(7,9,90),(7,11,110),(7,13,130);
/*!40000 ALTER TABLE `product_colours` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_images`
--

DROP TABLE IF EXISTS `product_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_images` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `product_id` int(10) unsigned NOT NULL,
  `url` varchar(512) COLLATE utf8mb4_unicode_ci NOT NULL,
  `alt` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sort_order` smallint(5) unsigned NOT NULL DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `idx_product_images_product` (`product_id`,`sort_order`),
  CONSTRAINT `fk_product_images_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_images`
--

LOCK TABLES `product_images` WRITE;
/*!40000 ALTER TABLE `product_images` DISABLE KEYS */;
INSERT INTO `product_images` VALUES (1,1,'/products/polyester-round-neck-110-130-1.webp','Polyester Round Neck, front',0,'2026-08-29 11:05:34'),(2,1,'/products/polyester-round-neck-110-130-2.webp','Polyester Round Neck, back',1,'2026-08-29 11:05:34'),(3,1,'/products/polyester-round-neck-110-130-3.webp','Polyester Round Neck, detail',2,'2026-08-29 11:05:34'),(4,2,'/products/polyester-round-neck-110-1.webp','Polyester Round Neck 110 GSM',0,'2026-08-29 11:05:34'),(5,3,'/products/full-sleeve-round-neck-tshirt-1.webp','Full-Sleeve Round Neck T-Shirt',0,'2026-08-29 11:05:34'),(6,4,'/products/oversized-tshirt-1.webp','Oversized T-Shirt',0,'2026-08-29 11:05:34'),(7,5,'/products/premium-cotton-polo-tshirt-1.webp','Premium Cotton Polo, front',0,'2026-08-29 11:05:34'),(8,5,'/products/premium-cotton-polo-tshirt-2.webp','Premium Cotton Polo, collar detail',1,'2026-08-29 11:05:34');
/*!40000 ALTER TABLE `product_images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_price_tiers`
--

DROP TABLE IF EXISTS `product_price_tiers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_price_tiers` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `product_id` int(10) unsigned NOT NULL,
  `min_qty` int(10) unsigned NOT NULL,
  `unit_price` decimal(10,2) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_price_tier` (`product_id`,`min_qty`),
  CONSTRAINT `fk_price_tiers_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `ck_price_tier_min_qty` CHECK (`min_qty` >= 1)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_price_tiers`
--

LOCK TABLES `product_price_tiers` WRITE;
/*!40000 ALTER TABLE `product_price_tiers` DISABLE KEYS */;
INSERT INTO `product_price_tiers` VALUES (1,1,50,79.00),(2,1,250,64.00),(3,1,1000,56.00),(4,1,5000,49.00),(5,2,50,72.00),(6,2,250,59.00),(7,2,1000,52.00),(8,2,5000,45.00),(9,3,50,169.00),(10,3,250,142.00),(11,3,1000,124.00),(12,4,50,219.00),(13,4,250,189.00),(14,4,1000,164.00),(15,5,50,249.00),(16,5,250,214.00),(17,5,1000,186.00),(19,7,50,139.00),(20,7,250,119.00),(21,7,1000,104.00),(22,7,5000,94.00);
/*!40000 ALTER TABLE `product_price_tiers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_sizes`
--

DROP TABLE IF EXISTS `product_sizes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_sizes` (
  `product_id` int(10) unsigned NOT NULL,
  `size_id` smallint(5) unsigned NOT NULL,
  PRIMARY KEY (`product_id`,`size_id`),
  KEY `idx_product_sizes_size` (`size_id`),
  CONSTRAINT `fk_product_sizes_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_product_sizes_size` FOREIGN KEY (`size_id`) REFERENCES `sizes` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_sizes`
--

LOCK TABLES `product_sizes` WRITE;
/*!40000 ALTER TABLE `product_sizes` DISABLE KEYS */;
INSERT INTO `product_sizes` VALUES (1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(1,9),(2,1),(2,2),(2,3),(2,4),(2,5),(2,6),(2,7),(2,8),(2,9),(3,1),(3,2),(3,3),(3,4),(3,5),(3,6),(3,7),(3,8),(3,9),(4,2),(4,3),(4,4),(4,5),(4,6),(4,7),(5,1),(5,2),(5,3),(5,4),(5,5),(5,6),(5,7),(5,8),(5,9),(7,1),(7,2),(7,3),(7,4),(7,5),(7,6),(7,7),(7,8),(7,9);
/*!40000 ALTER TABLE `product_sizes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_variants`
--

DROP TABLE IF EXISTS `product_variants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_variants` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `product_id` int(10) unsigned NOT NULL,
  `size_id` smallint(5) unsigned DEFAULT NULL,
  `colour_id` smallint(5) unsigned DEFAULT NULL,
  `sku` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `stock_units` int(10) unsigned NOT NULL DEFAULT 0,
  `hub` varchar(80) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` enum('in-stock','low','made-to-order') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'in-stock',
  `crm_id` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_variants_sku` (`sku`),
  UNIQUE KEY `uq_variant_combo` (`product_id`,`size_id`,`colour_id`),
  KEY `idx_variants_size` (`size_id`),
  KEY `idx_variants_colour` (`colour_id`),
  CONSTRAINT `fk_variants_colour` FOREIGN KEY (`colour_id`) REFERENCES `colours` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_variants_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_variants_size` FOREIGN KEY (`size_id`) REFERENCES `sizes` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_variants`
--

LOCK TABLES `product_variants` WRITE;
/*!40000 ALTER TABLE `product_variants` DISABLE KEYS */;
/*!40000 ALTER TABLE `product_variants` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `slug` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `collection_id` int(10) unsigned NOT NULL,
  `garment` enum('round-neck','full-sleeve','oversized','polo','hoodie','sweatshirt','jacket','formal-shirt','cap','tote','mug','bottle','kit-box') COLLATE utf8mb4_unicode_ci NOT NULL,
  `fabric` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `gsm` varchar(40) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `moq` int(10) unsigned NOT NULL DEFAULT 50,
  `status` enum('in-stock','low','made-to-order') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'in-stock',
  `badge` enum('Best seller','New','Sold out') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sort_order` smallint(5) unsigned NOT NULL DEFAULT 0,
  `is_active` tinyint(1) NOT NULL DEFAULT 1,
  `seo_title` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `seo_description` varchar(400) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `crm_id` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `crm_sku` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_products_slug` (`slug`),
  UNIQUE KEY `uq_products_crm_id` (`crm_id`),
  KEY `idx_products_collection` (`collection_id`,`is_active`,`sort_order`),
  KEY `idx_products_crm_sku` (`crm_sku`),
  FULLTEXT KEY `ft_products_search` (`name`,`fabric`,`description`),
  CONSTRAINT `fk_products_collection` FOREIGN KEY (`collection_id`) REFERENCES `collections` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'polyester-round-neck-110-130','Polyester Round Neck 110–130 GSM',1,'round-neck','100% Polyester, moisture-wicking','110–130 GSM',NULL,50,'in-stock','Best seller',1,1,NULL,NULL,NULL,'BB-TS-001','2026-08-29 11:05:34','2026-08-29 11:05:34'),(2,'polyester-round-neck-110','Polyester Round Neck 110 GSM',1,'round-neck','100% Polyester, sublimation-ready','110 GSM',NULL,50,'in-stock',NULL,2,1,NULL,NULL,NULL,'BB-TS-002','2026-08-29 11:05:34','2026-08-29 11:05:34'),(3,'full-sleeve-round-neck-tshirt','Full-Sleeve Round Neck T-Shirt',1,'full-sleeve','Combed cotton, bio-washed','180 GSM',NULL,50,'in-stock',NULL,3,1,NULL,NULL,NULL,'BB-TS-003','2026-08-29 11:05:34','2026-08-29 11:05:34'),(4,'oversized-tshirt','Oversized T-Shirt',1,'oversized','Heavyweight combed cotton, drop shoulder','220 GSM',NULL,50,'in-stock','New',4,1,NULL,NULL,NULL,'BB-TS-004','2026-08-29 11:05:34','2026-08-29 11:05:34'),(5,'premium-cotton-polo-tshirt','Premium Cotton Polo T-Shirt',1,'polo','Cotton pique, ribbed collar and cuffs','220 GSM',NULL,50,'in-stock','Best seller',5,1,NULL,NULL,NULL,'BB-TS-005','2026-08-29 11:05:34','2026-08-29 11:05:34'),(7,'cotton-round-neck-180','Cotton Round Neck 180 GSM',1,'round-neck','100% combed cotton, bio-washed','180 GSM',NULL,50,'in-stock',NULL,6,1,NULL,NULL,'CRM-1006','BB-TS-006','2026-08-29 11:24:12','2026-08-29 11:24:12');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quote_request_branding`
--

DROP TABLE IF EXISTS `quote_request_branding`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quote_request_branding` (
  `quote_request_id` int(10) unsigned NOT NULL,
  `branding_method_id` smallint(5) unsigned DEFAULT NULL,
  `submitted_label` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`quote_request_id`,`submitted_label`),
  KEY `idx_qrb_method` (`branding_method_id`),
  CONSTRAINT `fk_qrb_method` FOREIGN KEY (`branding_method_id`) REFERENCES `branding_methods` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_qrb_quote` FOREIGN KEY (`quote_request_id`) REFERENCES `quote_requests` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quote_request_branding`
--

LOCK TABLES `quote_request_branding` WRITE;
/*!40000 ALTER TABLE `quote_request_branding` DISABLE KEYS */;
/*!40000 ALTER TABLE `quote_request_branding` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quote_request_line_sizes`
--

DROP TABLE IF EXISTS `quote_request_line_sizes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quote_request_line_sizes` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `quote_request_line_id` int(10) unsigned NOT NULL,
  `size_id` smallint(5) unsigned DEFAULT NULL,
  `size_label` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `units` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_line_size` (`quote_request_line_id`,`size_label`),
  KEY `idx_qrls_size` (`size_id`),
  CONSTRAINT `fk_qrls_line` FOREIGN KEY (`quote_request_line_id`) REFERENCES `quote_request_lines` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_qrls_size` FOREIGN KEY (`size_id`) REFERENCES `sizes` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `ck_qrls_units` CHECK (`units` > 0)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quote_request_line_sizes`
--

LOCK TABLES `quote_request_line_sizes` WRITE;
/*!40000 ALTER TABLE `quote_request_line_sizes` DISABLE KEYS */;
/*!40000 ALTER TABLE `quote_request_line_sizes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quote_request_lines`
--

DROP TABLE IF EXISTS `quote_request_lines`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quote_request_lines` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `quote_request_id` int(10) unsigned NOT NULL,
  `product_id` int(10) unsigned DEFAULT NULL,
  `product_slug` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `product_name` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `colour_name` varchar(60) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `colour_hex` char(7) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `line_units` int(10) unsigned NOT NULL DEFAULT 0,
  `quoted_unit_price` decimal(10,2) unsigned DEFAULT NULL,
  `line_note` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sort_order` smallint(5) unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_line_product_colour` (`quote_request_id`,`product_slug`,`colour_name`),
  KEY `idx_lines_product` (`product_id`),
  CONSTRAINT `fk_lines_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_lines_quote` FOREIGN KEY (`quote_request_id`) REFERENCES `quote_requests` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quote_request_lines`
--

LOCK TABLES `quote_request_lines` WRITE;
/*!40000 ALTER TABLE `quote_request_lines` DISABLE KEYS */;
/*!40000 ALTER TABLE `quote_request_lines` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quote_requests`
--

DROP TABLE IF EXISTS `quote_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quote_requests` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `reference` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `company` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `destination` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `deadline` date DEFAULT NULL,
  `notes` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` enum('new','in-review','quoted','won','lost','spam') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'new',
  `status_note` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `assigned_to` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `quoted_at` datetime DEFAULT NULL,
  `quoted_total` decimal(12,2) unsigned DEFAULT NULL,
  `prefill_product` varchar(60) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `prefill_qty` int(10) unsigned DEFAULT NULL,
  `prefill_branding` varchar(60) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `source_page` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `referrer` varchar(512) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `utm_source` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `utm_medium` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `utm_campaign` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ip_address` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_agent` varchar(512) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `total_units` int(10) unsigned NOT NULL DEFAULT 0,
  `crm_id` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_quote_reference` (`reference`),
  UNIQUE KEY `uq_quote_crm_id` (`crm_id`),
  KEY `idx_quote_status_created` (`status`,`created_at`),
  KEY `idx_quote_email` (`email`),
  KEY `idx_quote_created` (`created_at`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quote_requests`
--

LOCK TABLES `quote_requests` WRITE;
/*!40000 ALTER TABLE `quote_requests` DISABLE KEYS */;
/*!40000 ALTER TABLE `quote_requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sizes`
--

DROP TABLE IF EXISTS `sizes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sizes` (
  `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `label` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sort_order` smallint(5) unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_sizes_label` (`label`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sizes`
--

LOCK TABLES `sizes` WRITE;
/*!40000 ALTER TABLE `sizes` DISABLE KEYS */;
INSERT INTO `sizes` VALUES (1,'XS',10),(2,'S',20),(3,'M',30),(4,'L',40),(5,'XL',50),(6,'2XL',60),(7,'3XL',70),(8,'4XL',80),(9,'5XL',90),(10,'One size',100);
/*!40000 ALTER TABLE `sizes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  `email` varchar(190) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `phone` varchar(30) DEFAULT NULL,
  `role` varchar(30) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `last_login_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_users_email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Boss Brand Admin','admin@bossbrand.ai','scrypt:32768:8:1$O5PnmQ88EZpsNiFO$f78010506f39cf2e9cae743f86b7a12a1c6cd2e51ec7b483d656b150e3be246380a21922847fc71b49f536d44e4c750cff96b47156d2baf971f800591e7ff98f',NULL,'admin',1,'2026-09-05 11:19:43','2026-08-29 07:10:51','2026-09-05 11:19:43');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `v_all_enquiries`
--

DROP TABLE IF EXISTS `v_all_enquiries`;
/*!50001 DROP VIEW IF EXISTS `v_all_enquiries`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `v_all_enquiries` (
  `kind` tinyint NOT NULL,
  `id` tinyint NOT NULL,
  `reference` tinyint NOT NULL,
  `status` tinyint NOT NULL,
  `name` tinyint NOT NULL,
  `company` tinyint NOT NULL,
  `email` tinyint NOT NULL,
  `phone` tinyint NOT NULL,
  `created_at` tinyint NOT NULL,
  `total_units` tinyint NOT NULL,
  `source_page` tinyint NOT NULL,
  `utm_source` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `v_collections`
--

DROP TABLE IF EXISTS `v_collections`;
/*!50001 DROP VIEW IF EXISTS `v_collections`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `v_collections` (
  `id` tinyint NOT NULL,
  `slug` tinyint NOT NULL,
  `name` tinyint NOT NULL,
  `image` tinyint NOT NULL,
  `tagline` tinyint NOT NULL,
  `garment` tinyint NOT NULL,
  `moq` tinyint NOT NULL,
  `starting_price` tinyint NOT NULL,
  `sku_count` tinyint NOT NULL,
  `sort_order` tinyint NOT NULL,
  `is_active` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `v_contact_requests`
--

DROP TABLE IF EXISTS `v_contact_requests`;
/*!50001 DROP VIEW IF EXISTS `v_contact_requests`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `v_contact_requests` (
  `id` tinyint NOT NULL,
  `reference` tinyint NOT NULL,
  `status` tinyint NOT NULL,
  `intent` tinyint NOT NULL,
  `name` tinyint NOT NULL,
  `company` tinyint NOT NULL,
  `email` tinyint NOT NULL,
  `phone` tinyint NOT NULL,
  `topic` tinyint NOT NULL,
  `message` tinyint NOT NULL,
  `assigned_to` tinyint NOT NULL,
  `replied_at` tinyint NOT NULL,
  `created_at` tinyint NOT NULL,
  `age_hours` tinyint NOT NULL,
  `response_minutes` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `v_products`
--

DROP TABLE IF EXISTS `v_products`;
/*!50001 DROP VIEW IF EXISTS `v_products`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `v_products` (
  `id` tinyint NOT NULL,
  `slug` tinyint NOT NULL,
  `name` tinyint NOT NULL,
  `collection` tinyint NOT NULL,
  `garment` tinyint NOT NULL,
  `fabric` tinyint NOT NULL,
  `gsm` tinyint NOT NULL,
  `moq` tinyint NOT NULL,
  `status` tinyint NOT NULL,
  `badge` tinyint NOT NULL,
  `sort_order` tinyint NOT NULL,
  `is_active` tinyint NOT NULL,
  `images` tinyint NOT NULL,
  `sizes` tinyint NOT NULL,
  `colours` tinyint NOT NULL,
  `tiers` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Dumping routines for database 'boss_brand'
--

--
-- Current Database: `boss_brand`
--

USE `boss_brand`;

--
-- Final view structure for view `v_all_enquiries`
--

/*!50001 DROP TABLE IF EXISTS `v_all_enquiries`*/;
/*!50001 DROP VIEW IF EXISTS `v_all_enquiries`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_all_enquiries` AS select 'contact' AS `kind`,`c`.`id` AS `id`,`c`.`reference` AS `reference`,`c`.`status` AS `status`,`c`.`name` AS `name`,`c`.`company` AS `company`,`c`.`email` AS `email`,`c`.`phone` AS `phone`,`c`.`created_at` AS `created_at`,NULL AS `total_units`,`c`.`source_page` AS `source_page`,`c`.`utm_source` AS `utm_source` from `contact_requests` `c` union all select 'quote' AS `kind`,`q`.`id` AS `id`,`q`.`reference` AS `reference`,`q`.`status` AS `status`,`q`.`name` AS `name`,`q`.`company` AS `company`,`q`.`email` AS `email`,`q`.`phone` AS `phone`,`q`.`created_at` AS `created_at`,`q`.`total_units` AS `total_units`,`q`.`source_page` AS `source_page`,`q`.`utm_source` AS `utm_source` from `quote_requests` `q` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_collections`
--

/*!50001 DROP TABLE IF EXISTS `v_collections`*/;
/*!50001 DROP VIEW IF EXISTS `v_collections`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_collections` AS select `c`.`id` AS `id`,`c`.`slug` AS `slug`,`c`.`name` AS `name`,`c`.`image_url` AS `image`,`c`.`tagline` AS `tagline`,`c`.`garment` AS `garment`,`c`.`moq` AS `moq`,coalesce(`c`.`starting_price_override`,(select min(`t`.`unit_price`) from (`product_price_tiers` `t` join `products` `p` on(`p`.`id` = `t`.`product_id`)) where `p`.`collection_id` = `c`.`id` and `p`.`is_active` = 1)) AS `starting_price`,coalesce(`c`.`sku_count_override`,(select count(0) from `products` `p` where `p`.`collection_id` = `c`.`id` and `p`.`is_active` = 1)) AS `sku_count`,`c`.`sort_order` AS `sort_order`,`c`.`is_active` AS `is_active` from `collections` `c` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_contact_requests`
--

/*!50001 DROP TABLE IF EXISTS `v_contact_requests`*/;
/*!50001 DROP VIEW IF EXISTS `v_contact_requests`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_contact_requests` AS select `c`.`id` AS `id`,`c`.`reference` AS `reference`,`c`.`status` AS `status`,`c`.`intent` AS `intent`,`c`.`name` AS `name`,`c`.`company` AS `company`,`c`.`email` AS `email`,`c`.`phone` AS `phone`,coalesce(`t`.`name`,`c`.`topic_label`) AS `topic`,`c`.`message` AS `message`,`c`.`assigned_to` AS `assigned_to`,`c`.`replied_at` AS `replied_at`,`c`.`created_at` AS `created_at`,timestampdiff(HOUR,`c`.`created_at`,coalesce(`c`.`replied_at`,current_timestamp())) AS `age_hours`,case when `c`.`replied_at` is null then NULL else timestampdiff(MINUTE,`c`.`created_at`,`c`.`replied_at`) end AS `response_minutes` from (`contact_requests` `c` left join `contact_topics` `t` on(`t`.`id` = `c`.`topic_id`)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_products`
--

/*!50001 DROP TABLE IF EXISTS `v_products`*/;
/*!50001 DROP VIEW IF EXISTS `v_products`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_products` AS select `p`.`id` AS `id`,`p`.`slug` AS `slug`,`p`.`name` AS `name`,`c`.`slug` AS `collection`,`p`.`garment` AS `garment`,`p`.`fabric` AS `fabric`,`p`.`gsm` AS `gsm`,`p`.`moq` AS `moq`,`p`.`status` AS `status`,`p`.`badge` AS `badge`,`p`.`sort_order` AS `sort_order`,`p`.`is_active` AS `is_active`,(select concat('[',coalesce(group_concat(json_quote(`i`.`url`) order by `i`.`sort_order` ASC,`i`.`id` ASC separator ','),''),']') from `product_images` `i` where `i`.`product_id` = `p`.`id`) AS `images`,(select concat('[',coalesce(group_concat(json_quote(`sz`.`label`) order by `sz`.`sort_order` ASC separator ','),''),']') from (`product_sizes` `ps` join `sizes` `sz` on(`sz`.`id` = `ps`.`size_id`)) where `ps`.`product_id` = `p`.`id`) AS `sizes`,(select concat('[',coalesce(group_concat(json_object('name',`co`.`name`,'hex',`co`.`hex`) order by `pc`.`sort_order` ASC,`co`.`sort_order` ASC separator ','),''),']') from (`product_colours` `pc` join `colours` `co` on(`co`.`id` = `pc`.`colour_id`)) where `pc`.`product_id` = `p`.`id`) AS `colours`,(select concat('[',coalesce(group_concat(json_object('minQty',`t`.`min_qty`,'price',`t`.`unit_price`) order by `t`.`min_qty` ASC separator ','),''),']') from `product_price_tiers` `t` where `t`.`product_id` = `p`.`id`) AS `tiers` from (`products` `p` join `collections` `c` on(`c`.`id` = `p`.`collection_id`)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-09-05 18:35:24
