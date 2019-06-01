USE dida;

-- 在插入或更新数据时变换坐标
-- 逐行进行（因为插入和更新是逐行的）
DELIMITER ||
DROP TRIGGER IF EXISTS tr_c_readin0 ||  
CREATE TRIGGER tr_c_readin0 BEFORE INSERT ON customer FOR EACH ROW
BEGIN
	IF NEW.acctbal > 0
    THEN
	SET NEW.log = FORMAT(NEW.log/10,1);
	SET NEW.lat = FORMAT(NEW.lat/10,1);
    END IF;
END ||

DROP TRIGGER IF EXISTS tr_c_readin1 ||  
CREATE TRIGGER tr_c_readin1 BEFORE UPDATE ON customer FOR EACH ROW
BEGIN
	SET NEW.log = FORMAT(NEW.log/10,1);
	SET NEW.lat = FORMAT(NEW.lat/10,1);
END ||

DROP TRIGGER IF EXISTS tr_d_readin0 ||  
CREATE TRIGGER tr_d_readin0 BEFORE INSERT ON driver FOR EACH ROW
BEGIN
	SET NEW.log = FORMAT(NEW.log/10,1);
	SET NEW.lat = FORMAT(NEW.lat/10,1);
END ||

DROP TRIGGER IF EXISTS tr_d_readin1 ||  
CREATE TRIGGER tr_d_readin1 BEFORE UPDATE ON driver FOR EACH ROW
BEGIN
	SET NEW.log = FORMAT(NEW.log/10,1);
	SET NEW.lat = FORMAT(NEW.lat/10,1);
END ||

DROP TRIGGER IF EXISTS tr_o_readin0 ||  
CREATE TRIGGER tr_o_readin0 BEFORE INSERT ON orders FOR EACH ROW
BEGIN
	SET NEW.log = FORMAT(NEW.log/10,1);
	SET NEW.lat = FORMAT(NEW.lat/10,1);
END ||

DROP TRIGGER IF EXISTS tr_o_readin1 ||  
CREATE TRIGGER tr_o_readin1 BEFORE UPDATE ON orders FOR EACH ROW
BEGIN
	SET NEW.log = FORMAT(NEW.log/10,1);
	SET NEW.lat = FORMAT(NEW.lat/10,1);
END ||

DROP TRIGGER IF EXISTS tr_co_readin0 ||  
CREATE TRIGGER tr_co_readin0 BEFORE INSERT ON corders FOR EACH ROW
BEGIN
	SET NEW.log = FORMAT(NEW.log/10,1);
	SET NEW.lat = FORMAT(NEW.lat/10,1);
END ||

DROP TRIGGER IF EXISTS tr_co_readin1 ||  
CREATE TRIGGER tr_co_readin1 BEFORE UPDATE ON corders FOR EACH ROW
BEGIN
	SET NEW.log = FORMAT(NEW.log/10,1);
	SET NEW.lat = FORMAT(NEW.lat/10,1);
END ||
DELIMITER ;


DELIMITER ||
DROP TRIGGER IF EXISTS tr_dropcar ||
CREATE TRIGGER tr_dropcar BEFORE DELETE ON car FOR EACH ROW
BEGIN
	UPDATE driver D
    SET D.carno = NULL
    WHERE D.carno = OLD.carno;
END||
DELIMITER ;


-- 当订单完成时，分别对客户扣款和司机账户赠款，并删除orders中的相应订单
DELIMITER ||
DROP TRIGGER IF EXISTS tr_pay ||  
CREATE TRIGGER tr_pay BEFORE INSERT ON corders FOR EACH ROW
BEGIN
IF NEW.stat = 4 THEN
	IF C.acctbal >= NEW.prize THEN
		UPDATE customer C
		SET C.acctbal = C.acctbal - NEW.prize
		WHERE C.phone = NEW.custkey;
		UPDATE driver D
		SET D.acctbal = D.acctbal + NEW.prize
		WHERE D.phone = NEW.drvkey;
	ELSE 
		UPDATE driver D
		SET D.acctbal = D.acctbal + C.acctbal
		WHERE D.phone = NEW.drvkey;
		UPDATE customer C
		SET C.acctbal = 0
		WHERE C.phone = NEW.custkey;
	END IF;
END IF;
DELETE FROM orders
WHERE orders.orderkey = NEW.orderkey;
END || 
DELIMITER ;

-- 当在customer,driver,orders或corders中插入一条数据，在logs中生成一条日志信息
DROP TABLE IF EXISTS `logs`;
CREATE TABLE `logs` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Time` DATETIME,
  `log` varchar(255) DEFAULT NULL COMMENT '日志说明',
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='日志表';

-- SELECT *
-- FROM logs;

DROP TRIGGER IF EXISTS drvier_log;
DELIMITER ||
CREATE TRIGGER customer_log BEFORE INSERT ON customer FOR EACH ROW
BEGIN
DECLARE s1 VARCHAR(60)character set utf8;
DECLARE s2 VARCHAR(20) character set utf8; #设置字符集，防止中文字符编码出现乱码
DECLARE s3 DATETIME;
SET s2 = " is created";
SET s1 = CONCAT(NEW.name,'(',NEW.phone,')',s2);     #函数CONCAT：字符串连接
SET s3 = now();
INSERT INTO logs(time,log) values(s3,s1);
END ||

CREATE TRIGGER drvier_log AFTER INSERT ON driver FOR EACH ROW
BEGIN
DECLARE s1 VARCHAR(60)character set utf8;
DECLARE s2 VARCHAR(20) character set utf8; 
DECLARE s3 DATETIME;
SET s2 = " is created";
SET s3 = now();
SET s1 = CONCAT(NEW.name,'(',NEW.phone,')',s2);     
INSERT INTO logs(Time,log) values(s3,s1);
END ||

CREATE TRIGGER orders_log AFTER INSERT ON orders FOR EACH ROW
BEGIN
DECLARE s1 VARCHAR(80)character set utf8;
DECLARE s2 VARCHAR(20) character set utf8; 
DECLARE s3 DATETIME;
SET s2 = " submit an order: ";
SET s3 = now();
SET s1 = CONCAT(NEW.custkey, s2, NEW.orderkey);     
INSERT INTO logs(Time,log) values(s3,s1);
END ||

CREATE TRIGGER corders_log AFTER INSERT ON corders FOR EACH ROW
BEGIN
DECLARE s1 VARCHAR(80)character set utf8;
DECLARE s2 VARCHAR(20) character set utf8; 
DECLARE s3 DATETIME;
SET s2 = " is completed";
SET s1 = CONCAT(NEW.orderkey, s2);     
SET s3 = now();
INSERT INTO logs(Time,log) values(s3,s1);
END ||
DELIMITER ;