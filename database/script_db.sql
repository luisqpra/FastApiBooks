-- MySQL Script generated by MySQL Workbench
-- vie 27 ene 2023 13:32:14
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`User`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`User` (
  `id_user` INT NOT NULL,
  `firts_name` VARCHAR(32) CHARACTER SET 'binary' NOT NULL,
  `last_name` VARCHAR(32) COLLATE 'Default Collation' NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password` VARCHAR(32) NOT NULL,
  `birth_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_user`),
  UNIQUE INDEX `id_user_UNIQUE` (`id_user` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE);


-- -----------------------------------------------------
-- Table `mydb`.`Book`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Book` (
  `id_book` INT NOT NULL,
  `title` VARCHAR(255) NOT NULL,
  `reading_age` VARCHAR(255) NULL,
  `pages` INT NULL,
  `language` VARCHAR(64) NULL,
  `publisher` VARCHAR(128) NULL,
  `date_add` TIMESTAMP NOT NULL,
  `date_update` TIMESTAMP NOT NULL,
  PRIMARY KEY (`id_book`),
  UNIQUE INDEX `id_book_UNIQUE` (`id_book` ASC) VISIBLE);


-- -----------------------------------------------------
-- Table `mydb`.`Author`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Author` (
  `id_author` INT NOT NULL,
  `name` VARCHAR(64) NOT NULL,
  `nationality` VARCHAR(255) NULL,
  `genre` VARCHAR(32) NULL,
  `birthdate` TIMESTAMP NULL,
  PRIMARY KEY (`id_author`),
  UNIQUE INDEX `id_author_UNIQUE` (`id_author` ASC) VISIBLE);


-- -----------------------------------------------------
-- Table `mydb`.`Book_Author`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Book_Author` (
  `id_book_author` INT NOT NULL,
  `fk_id_author` INT NOT NULL,
  `fk_id_book` INT NOT NULL,
  INDEX `fk_Book_has_Author_Author1_idx` (`fk_id_author` ASC) VISIBLE,
  INDEX `fk_Book_has_Author_Book_idx` (`fk_id_book` ASC) VISIBLE,
  PRIMARY KEY (`id_book_author`),
  UNIQUE INDEX `id_book_author_UNIQUE` (`id_book_author` ASC) VISIBLE,
  CONSTRAINT `fk_Book`
    FOREIGN KEY (`fk_id_book`)
    REFERENCES `mydb`.`Book` (`id_book`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Author`
    FOREIGN KEY (`fk_id_author`)
    REFERENCES `mydb`.`Author` (`id_author`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `mydb`.`User_Book`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`User_Book` (
  `id_user_book` INT NOT NULL,
  `fk_id_user` INT NOT NULL,
  `fk_id_book` INT NOT NULL,
  INDEX `fk_User_has_Book_Book1_idx` (`fk_id_book` ASC) VISIBLE,
  INDEX `fk_User_has_Book_User1_idx` (`fk_id_user` ASC) VISIBLE,
  PRIMARY KEY (`id_user_book`),
  UNIQUE INDEX `id_user_book_UNIQUE` (`id_user_book` ASC) VISIBLE,
  CONSTRAINT `fk_id_user`
    FOREIGN KEY (`fk_id_user`)
    REFERENCES `mydb`.`User` (`id_user`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_id_book`
    FOREIGN KEY (`fk_id_book`)
    REFERENCES `mydb`.`Book` (`id_book`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;