# Taxi-taking-Simulation

______________
--------------
# A. ���ݿⲿ��

/ dida.sql  
 customer��driver��car��orders��corders��Ķ��壬�������ݿ��ʵ�������ԺͲ��������ԣ����ð��� NOT NULL,  ON DELETE CASCADE��Լ���ͼ�������

/ trigger.sql
 ��ȡPython�д�������ݣ�����͸��±�ʱ������һ�������ݸ�ʽ
 ʵ���û��Զ����������Լ�������car����ɾ������ʱ������Ӧdriver�����carno��ΪNULL
 ����ɶ�����ֱ��˾���ͳ˿��˻����ӿ۳��������
 ����logs������customer,driver,orders��corders�в���һ�����ݣ���logs������һ����־��Ϣ

/ grant.sql
 ���δ��boss�����û���ʶ�����������������������ȫ��Ȩ��
 ���δ�򳵹�˾ְԱ�����û���ʶ����������������������Ĳ�ѯȨ��

/ view.sql
 ��ÿһλ�û�������ѯ��������ͼ���Ա��ڽ����������
��ʵ���������ͨ��python��csv����ǰ������û����еģ���ע���û�����ע��ͬʱ��python�������ݿ⽨����Ӧ����ͼ��
___________________
-------------------
# B. Python���Բ���

/ DATA customer.py, DATA driver.py, DATA car.py
 ����python���Դ�csv����������ݿ⵼����ǰ�ĳ˿�˾��������Ϣ

/ sql.py
 ��MySQL���Ӻͽ�������������

/ globaliterm.py
 ȫ�ֱ����������Զ��庯����

/ simulation.py
 ģ���ϵͳ���еĳ���

/ interactive-test.py
 ����������ģ��
 ����pygame�����Ľ���ƽ̨��������
___________________
-------------------
# C. ���й���˵��

1.  ����dida.sql�ļ��������ݿⲢ����
2. ����DATA customer.py, DATA driver.py, DATA car.py�����������
3. ����trigger.sql��grant.sql��view.sql��Ϊģ������������ݿ�
4. ����interactive-test.py

ע�������Ȱ�װ��pygame��MySQLdb
________________________________________