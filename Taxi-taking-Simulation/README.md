# Taxi-taking-Simulation

______________
--------------
# A. 数据库部分

/ dida.sql  
 customer，driver，car，orders，corders表的定义，考虑数据库的实体完整性和参照完整性，设置包括 NOT NULL,  ON DELETE CASCADE等约束和级联操作

/ trigger.sql
 获取Python中传入的数据（插入和更新表）时，设置一定的数据格式
 实现用户自定义的完整性约束：如从car表中删除车辆时，将相应driver的外键carno设为NULL
 在完成订单后分别对司机和乘客账户增加扣除订单金额
 建表logs，当在customer,driver,orders或corders中插入一条数据，在logs中生成一条日志信息

/ grant.sql
 给滴答打车boss创建用户标识、口令，并赋予对以上六个表的全部权限
 给滴答打车公司职员创建用户标识、口令，并赋予对以上六个表的查询权限

/ view.sql
 对每一位用户建立查询订单的视图，以便在交互窗口输出
（实际上是针对通过python从csv中提前导入的用户进行的，新注册用户将在注册同时由python连接数据库建立相应的视图）
___________________
-------------------
# B. Python语言部分

/ DATA customer.py, DATA driver.py, DATA car.py
 利用python语言从csv表格中向数据库导入先前的乘客司机车辆信息

/ sql.py
 与MySQL连接和交互的语言设置

/ globaliterm.py
 全局变量，常用自定义函数等

/ simulation.py
 模拟打车系统运行的程序

/ interactive-test.py
 主函数所在模块
 运用pygame建立的交互平台和输出情况
___________________
-------------------
# C. 运行过程说明

1.  运行dida.sql文件建立数据库并定义
2. 利用DATA customer.py, DATA driver.py, DATA car.py导入基本数据
3. 运行trigger.sql，grant.sql，view.sql，为模拟过程配置数据库
4. 运行interactive-test.py

注：请事先安装好pygame，MySQLdb
________________________________________