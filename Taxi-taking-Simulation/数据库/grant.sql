# 给滴答打车boss创建用户标识、口令，并赋予全部权限
CREATE USER 'liujiajun'@'localhost' IDENTIFIED BY 'shujukuqiu4.0';

GRANT ALL Privileges ON TABLE `dida.customer` TO 'liujiajun'@'localhost';
GRANT ALL Privileges ON TABLE `dida.driver` TO 'liujiajun'@'localhost';
GRANT ALL Privileges ON TABLE `dida.car` TO 'liujiajun'@'localhost';
GRANT ALL Privileges ON TABLE `dida.orders` TO 'liujiajun'@'localhost';
GRANT ALL Privileges ON TABLE `dida.corders` TO 'liujiajun'@'localhost';
GRANT ALL Privileges ON TABLE `dida.logs` TO 'liujiajun'@'localhost';

# 给滴答打车公司职员创建用户标识、口令，并赋予查询权限
CREATE USER 'employee'@'localhost' IDENTIFIED BY '123456';

GRANT SELECT ON TABLE `dida.customer` TO 'liujiajun'@'localhost';
GRANT SELECT ON TABLE `dida.driver` TO 'liujiajun'@'localhost';
GRANT SELECT ON TABLE `dida.car` TO 'liujiajun'@'localhost';
GRANT SELECT ON TABLE `dida.orders` TO 'liujiajun'@'localhost';
GRANT SELECT ON TABLE `dida.corders` TO 'liujiajun'@'localhost';
GRANT SELECT ON TABLE `dida.logs` TO 'liujiajun'@'localhost';