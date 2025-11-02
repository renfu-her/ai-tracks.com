-- 直接创建所有必需的表（如果迁移失败时的备选方案）
-- 使用方法: mysql -u root -p blog < create_tables.sql

USE blog;

-- 创建 users 表（如果不存在）
CREATE TABLE IF NOT EXISTS `users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(80) NOT NULL COMMENT '用戶名',
    `email` VARCHAR(255) NOT NULL COMMENT '電子郵件',
    `password_hash` VARCHAR(255) NOT NULL COMMENT '密碼雜湊',
    `role` ENUM('admin', 'user') NOT NULL COMMENT '角色',
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE COMMENT '是否啟用',
    `created_at` DATETIME NOT NULL,
    `updated_at` DATETIME NOT NULL,
    `last_login` DATETIME NULL COMMENT '最後登入時間',
    UNIQUE KEY `username` (`username`),
    UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建 product_categories 表（如果不存在）
CREATE TABLE IF NOT EXISTS `product_categories` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL COMMENT '類別名稱',
    `slug` VARCHAR(100) NOT NULL COMMENT 'URL 友好名稱',
    `description` TEXT NULL COMMENT '描述',
    `image` VARCHAR(255) NULL COMMENT '類別圖片',
    `status` BOOLEAN NOT NULL DEFAULT TRUE COMMENT '狀態',
    `sort_order` INT NOT NULL DEFAULT 0 COMMENT '排序',
    `created_at` DATETIME NOT NULL,
    `updated_at` DATETIME NOT NULL,
    UNIQUE KEY `name` (`name`),
    UNIQUE KEY `slug` (`slug`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建 project_cases 表
CREATE TABLE IF NOT EXISTS `project_cases` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL COMMENT '名稱',
    `sub_name` VARCHAR(255) NULL COMMENT '副標題',
    `url` VARCHAR(255) NULL COMMENT '網址',
    `content` TEXT NOT NULL COMMENT '內容',
    `category_id` INT NULL COMMENT '類別ID',
    `status` BOOLEAN NOT NULL DEFAULT TRUE COMMENT '狀態',
    `created_at` DATETIME NOT NULL,
    `updated_at` DATETIME NOT NULL,
    FOREIGN KEY (`category_id`) REFERENCES `product_categories`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建 case_photos 表
CREATE TABLE IF NOT EXISTS `case_photos` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `project_case_id` INT NOT NULL COMMENT '案例ID',
    `image` VARCHAR(255) NOT NULL COMMENT '案例照片',
    `sort_order` INT NOT NULL DEFAULT 0 COMMENT '排序',
    `created_at` DATETIME NOT NULL,
    `updated_at` DATETIME NOT NULL,
    FOREIGN KEY (`project_case_id`) REFERENCES `project_cases`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建 contacts 表
CREATE TABLE IF NOT EXISTS `contacts` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL COMMENT '姓名',
    `email` VARCHAR(255) NOT NULL COMMENT '信箱',
    `phone` VARCHAR(20) NULL COMMENT '電話',
    `subject` VARCHAR(255) NOT NULL COMMENT '主旨',
    `message` TEXT NOT NULL COMMENT '訊息',
    `status` ENUM('pending', 'processing', 'completed') NOT NULL DEFAULT 'pending' COMMENT '處理狀態',
    `reply` TEXT NULL COMMENT '回覆內容',
    `replied_at` DATETIME NULL COMMENT '回覆時間',
    `image` VARCHAR(255) NULL COMMENT '圖片',
    `created_at` DATETIME NOT NULL,
    `updated_at` DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建 news 表
CREATE TABLE IF NOT EXISTS `news` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `title` VARCHAR(255) NOT NULL COMMENT '標題',
    `content` TEXT NOT NULL COMMENT '內容',
    `image` VARCHAR(255) NULL COMMENT '圖片',
    `published_at` DATE NOT NULL COMMENT '發布日期',
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE COMMENT '是否啟用',
    `created_at` DATETIME NOT NULL,
    `updated_at` DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建 sliders 表
CREATE TABLE IF NOT EXISTS `sliders` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `title` VARCHAR(255) NOT NULL COMMENT '標題',
    `description` TEXT NULL COMMENT '描述',
    `image` VARCHAR(255) NOT NULL COMMENT '圖片',
    `link` VARCHAR(255) NULL COMMENT '連結',
    `sort` INT NOT NULL DEFAULT 0 COMMENT '排序',
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE COMMENT '是否啟用',
    `created_at` DATETIME NOT NULL,
    `updated_at` DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建 page_settings 表（如果不存在）
CREATE TABLE IF NOT EXISTS `page_settings` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `page_type` VARCHAR(50) NOT NULL COMMENT '頁面類型',
    `banner_image` VARCHAR(255) NULL COMMENT 'Banner 圖片',
    `created_at` DATETIME NOT NULL,
    `updated_at` DATETIME NOT NULL,
    UNIQUE KEY `page_type` (`page_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建 alembic_version 表（如果不存在）
CREATE TABLE IF NOT EXISTS `alembic_version` (
    `version_num` VARCHAR(32) NOT NULL,
    PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 设置迁移版本（标记为最新版本 ed9a3a646336）
INSERT INTO `alembic_version` (`version_num`) 
VALUES ('ed9a3a646336')
ON DUPLICATE KEY UPDATE `version_num` = 'ed9a3a646336';

-- 显示创建的表
SHOW TABLES;

