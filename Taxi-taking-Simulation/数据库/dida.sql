DROP DATABASE dida;
CREATE DATABASE dida;

USE dida;

DROP TABLE IF EXISTS `customer`;
CREATE TABLE `customer` (
  `name` varchar(40) NOT NULL,
  `phone` varchar(20),
  `acctbal` real NOT NULL,
  `log` FLOAT NOT NULL,
  `lat` FLOAT NOT NULL,
  `stat` INTEGER,
  PRIMARY KEY (`phone`),
  UNIQUE KEY `custkey` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- INSERT INTO `customer` VALUES ('Lee', '13883538912', 100,79,54,0);
-- SELECT *
-- FROM driver;
-- DELETE FROM customer WHERE name='Lee';

DROP TABLE IF EXISTS `car`;
CREATE TABLE `car` (
  `carno` varchar(20) NOT NULL,
  `cartype` varchar(20),
  `carcol` varchar(10),
  PRIMARY KEY (`carno`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `driver`;
CREATE TABLE `driver` (
  `name` varchar(40) NOT NULL,
  `phone` varchar(20),
  `carno` varchar(20) NOT NULL,
  `acctbal` real NOT NULL,
  `log` FLOAT NOT NULL,
  `lat` FLOAT NOT NULL,
  `stat` INTEGER,
  PRIMARY KEY (`phone`),
  UNIQUE KEY `drvkey` (`name`),
  FOREIGN KEY (`carno`) 
	  REFERENCES car (`carno`)
      ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders` (
    `orderkey` varchar(18) NOT NULL,
    `custkey` varchar(20) NOT NULL,
    `drvkey` varchar(20),
    `log` float(2,1) NOT NULL,
    `lat` float(2,1) NOT NULL,
    `prize` REAL,
    `stat` INTEGER,
    PRIMARY KEY (`orderkey`),
    FOREIGN KEY (`custkey`)
        REFERENCES customer (`phone`)
        ON DELETE CASCADE,
    FOREIGN KEY (`drvkey`)
        REFERENCES driver (`phone`)
        ON DELETE CASCADE
)  ENGINE=INNODB DEFAULT CHARSET=LATIN1;

DROP TABLE IF EXISTS `corders`;
CREATE TABLE `corders` (
    `orderkey` CHAR(18) NOT NULL,
    `custkey` CHAR(20) NOT NULL,
    `drvkey` CHAR(20) NOT NULL,
    `log` FLOAT(1) NOT NULL,
    `lat` FLOAT(1) NOT NULL,
    `prize` REAL,  
    `stat` INTEGER,
    PRIMARY KEY (`orderkey`),
    FOREIGN KEY (`custkey`)
        REFERENCES customer (`phone`)
        ON DELETE CASCADE,
    FOREIGN KEY (`drvkey`)
        REFERENCES driver (`phone`)
        ON DELETE CASCADE
)  ENGINE=INNODB DEFAULT CHARSET=LATIN1;