import time
from sql import *
from globaliterm import *
global screensize

wait_time = 10


class Order():
    def __init__(self, orderkey, custkey, drvkey, log, lat, prize, state, t0):
        self.orderkey = orderkey
        self.custkey = custkey
        self.drvkey = drvkey
        self.log = log
        self.lat = lat
        self.prize = prize
        self.state = state
        self.t0=t0 # 代表创建订单的时间

    def __repr__(self):
        return"{orderkey:%s, custkey:%s, drvkey:%s, log:%.1f, lat:%.1f, amount:% .2f,  stat:%d}" \
              % (self.orderkey, self.custkey, self.drvkey, self.log, self.lat, self.amount, self.state)

    # 定义了一个随机生成订单号的函数
    def create_id(custkey):
        # 顾客id后2位+下单时间的年月日12+随机数4位
        local_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))[2:]
        result = str(custkey)[-2:] + local_time + str(random.randint(1000, 9999))
        return result


def random_walk():
    direction = [(-1, 0), (1, 0), (0, 1), (0, -1)] # 左右下上
    a = random.randint(0, 3)
    return direction[a]


def translate(objects, objectsname):
    if objectsname == 'drv':
        if objects.state == 0:
            return 'available'
        elif objects.state == 1:
            return 'to get customer'
        elif objects.state == 2:
            return 'engaged'
        elif objects.state == 3:
            return 'wait'
        elif objects.state == 4:
            return 'get caught'
    elif objectsname == 'cust':
        if objects.state == 0:
            return 'random'
        if objects.state == 1:
            return 'wait'
        if objects.state == 3:
            return 'submit'
        if objects.state == 4:
            return 'angry'


 # 定义了一个随机提交订单的函数:5秒刷新一次
def submit_order():
    
    count = 0
    for x in global_var.objectscar:
        if x.state == 0:
            count += 1
    available = count
    print(count)
    cnt = random.randint(1, available)
    print(cnt)
    for i in range(int(cnt)):
        create_order()


# 定义了一个生成订单的函数
#  含插入数据库
def create_order():
    print('create order')
    list_cust0 = [x for x in global_var.objectscust if x.state == 0]
    if len(list_cust0) >= 1:
        cust = random.choice(list_cust0)
        # 表示创建了订单，但还没有人接订单
        c = cust.phone
        o = Order.create_id(c)
        d = 0
        t0 = time.clock()

        longitude = random.randint(0, screensize)  # 生成一个0-41的横坐标,一位小数(目的地)
        latitude = random.randint(0, screensize)  # 生成纵坐标
        amount = prize(distance(cust, longitude, latitude))  # 订单多少钱
        # 只有在用户余额比订单金额大的时候才能下单
        if cust.acctbal > amount:
            cust.state = 3
            new_order = Order(o, c, d, longitude, latitude, amount, 0, t0)
            global_var.list_order.append(new_order)

            mysql = 'INSERT INTO orders VALUES("{orderkey}","{custkey}","{drvkey}",{log},{lat},{prize},{stat})'
            mysql_command = mysql.format(orderkey=o, custkey=c, drvkey=d, log=longitude, lat=latitude, stat=0,
                                         prize=amount)
            db = MySQL()
            db.execute(mysql_command)
            print(mysql_command)
        else:
            return
    else:
        return


# 计算距离
def distance(cust, x, y):
    step0 = abs(cust.log-x)
    step1 = abs(cust.lat-y)
    return step0+step1


# 定义一个刷新状态的函数
# 更新到数据库
def refresh_stat(subject, subjectname, stat):
    subject.state = stat

    if subjectname == 'drv':
        d = subject.phone
        sql = "UPDATE dida.driver SET stat ={state} WHERE phone ='{dphone}' "
        sql_c = sql.format(state=stat, dphone=d)
    elif subjectname == 'cust':
        c = subject.phone
        sql = "UPDATE dida.customer SET stat={state} WHERE phone='{cphone}'"
        sql_c = sql.format(state=stat, cphone=c)
    elif subjectname == 'order':
        o = subject.orderkey
        sql = "UPDATE orders SET stat={state} WHERE orderkey='{orderkey}'"
        sql_c = sql.format(state=stat, orderkey=o)
    try:
        db = MySQL()
        db.execute(sql_c)
        db.connection.commit()
    except:
        db.connection.rollback()


# 订单被接到，车和乘客和订单状态再刷新
def getcar_stat(drv, cust, order):
    refresh_stat(drv, 'drv', 1)
    print("drv" + drv.phone + ' is gonging to get cust!')
    refresh_stat(cust, 'cust', 1)
    refresh_stat(order, 'order', 1)


# 在接单后，更新订单中的drvkey
def refresh_order_drvkey(drvphone, order):
    sql = 'update orders set drvkey="{drvkey}" where orderkey="{orderkey}" '
    sql_command = sql.format(drvkey=drvphone, orderkey=order)
    try:
        db = MySQL()
        db.execute(sql_command)
        db.connection.commit()
    except:
        db.connection.rollback()


# 客户发起订单之后 判断哪个车接到订单 得到driver的信息
def search_car(order, cust, log, lat, time_passed):
    # 不在整点上或者边上
    if (log > (log // 10) * 10) & (lat > (lat // 10) * 10):
        for i in range(len(global_var.objectscar)):
            if global_var.objectscar[i].state == 0:
                if ((log // 10) * 10 - 10 <= global_var.objectscar[i].log <= (log // 10) * 10 + 20) & (
                                (lat // 10) * 10 - 10 <= global_var.objectscar[i].lat <= (lat // 10) * 10 + 20):
                    order.drvkey = global_var.objectscar[i].phone

                    getcar_stat(global_var.objectscar[i], cust, order)
                    refresh_order_drvkey(global_var.objectscar[i].phone, order.orderkey)
                    whether_cancel(cust, global_var.objectscar[i], order)

                    break
    elif (log == (log // 10) * 10) & (lat > (lat // 10) * 10):
        for i in range(len(global_var.objectscar)):
            if global_var.objectscar[i].state == 0:
                if ((log // 10) * 10 - 10 <= global_var.objectscar[i].log <= (log // 10) * 10 + 10) & (
                                (lat // 10) * 10 - 10 <= global_var.objectscar[i].lat <= (lat // 10) * 10 + 20):
                    order.drvkey = global_var.objectscar[i].phone

                    getcar_stat(global_var.objectscar[i], cust, order)
                    refresh_order_drvkey(global_var.objectscar[i].phone, order.orderkey)
                    whether_cancel(cust, global_var.objectscar[i], order)

                    break
    elif (log > (log // 10) * 10) & (lat == (lat // 10) * 10):
        for i in range(len(global_var.objectscar)):

            if global_var.objectscar[i].state == 0:
                if ((log // 10) * 10 - 10 <= global_var.objectscar[i].log <= (log // 10) * 10 + 20) & (
                                (lat // 10) * 10 - 10 <= global_var.objectscar[i].lat <= (lat // 10) * 10 + 10):
                    order.drvkey = global_var.objectscar[i].phone

                    getcar_stat(global_var.objectscar[i], cust, order)
                    refresh_order_drvkey(global_var.objectscar[i].phone, order.orderkey)
                    whether_cancel(cust, global_var.objectscar[i], order)

                    break
    else:
        for i in range(len(global_var.objectscar)):
            if global_var.objectscar[i].state == 0:
                if (log - 10 <= global_var.objectscar[i].log <= log + 10) & (
                            lat - 10 <= global_var.objectscar[i].lat <= lat + 10):
                    order.drvkey = global_var.objectscar[i].phone

                    getcar_stat(global_var.objectscar[i], cust, order)
                    whether_cancel(cust, global_var.objectscar[i], order)

                    break


# 客户发起订单函数执行后，马上遍历所有提交了但未被接受的订单，寻找可接单的车辆
def search_carinol(time_passed):
    global wait_time
    for i in global_var.list_order:
        if i.state == 0:
            c = i.custkey
            clist = [x for x in global_var.objectscust if x.phone == c]
            cust = clist[0]
            if time.clock() - i.t0 <= wait_time:

                search_car(i, cust, cust.log, cust.lat, time_passed)
            elif time.clock() - i.t0 > wait_time:
                whether_move(i, cust, time_passed)

    return


# 遍历订单，对于每种到达目标格子后的订单状态进行刷新
"""def refresh_statinol():
    for i in list_order:
        order = i
        c = order.custkey
        d = order.drvkey
        clist = [x for x in objectscust if x.phone == c]
        cust = clist[0]
        dlist = [y for y in objectscar if y.phone == d]
        drv = dlist[0]
        if order.state==0:
            if time.clock-order.t0>30:
                whether_move(order,cust)
        elif order.state == 1:
            if meet(drv, cust) == 1:
                meet_stat(drv, cust, order)
        elif order.state == 2:
            if meet(drv, order) == 1:
                reach_stat(drv, cust, order)"""


# 定义了一个车去到目标格子的函数，用于接客和载客
def goto_aim(drv, aim, aimname):
    log_withinrange = aim.log // 10 == drv.log // 10 or aim.log // 10 == drv.log / 10 - 1 or aim.log // 10 == drv.log / 10 + 1
    lat_withinrange = aim.lat // 10 == drv.lat // 10 or aim.lat // 10 == drv.lat / 10 - 1 or aim.lat // 10 == drv.lat / 10 + 1
    if log_withinrange:

        if lat_withinrange:

            if aimname == 'cust':
                if whether_delay():
                    meet_stat(drv, aim)
                    drv.wait_time = global_var.current_time
                    drv.state = 3
                else:
                    meet_stat(drv, aim)
            elif aimname == 'order':
                reach_stat(drv, aim)
        elif aim.lat > drv.lat:
            drv.refresh_location1(0, 1)
        elif aim.lat < drv.lat:

            drv.refresh_location1(0, -1)

    elif lat_withinrange:

        if aim.log > drv.log:
            drv.refresh_location1(1, 0)

        elif aim.log < drv.log:
            drv.refresh_location1(-1, 0)

    elif aim.log < drv.log:
        drv.refresh_location1(-1, 0)

        if aim.lat < drv.lat:
            drv.refresh_location1(0, -1)

        elif aim.lat > drv.lat:
            drv.refresh_location1(0, 1)


    elif aim.log > drv.log:
        drv.refresh_location1(1, 0)

        if aim.lat < drv.lat:
            drv.refresh_location1(0, -1)


        elif aim.lat > drv.lat:
            drv.refresh_location1(0, 1)


# 判断是否到达目标格子
def meet(drv, aim):
    if (aim.log // 10 == drv.log // 10 or (aim.log // 10) * 10 == drv.log - 10) & (
                aim.lat // 10 == drv.lat // 10 or (aim.lat // 10) * 10 == drv.lat - 10):
        return 1


# 计算订单价格，基于车载客经过的路程 Total Step
def prize(ts):
    if ts <= 50:
        return 11
    else:
        return round(11 + (ts - 50) * 0.1, 1)


# 将车刷新到格子中央
def center(drv, aim):
    drv.pos.left = (aim.log // 10) * 10 + 5
    drv.pos.top = (aim.lat // 10) * 10 + 5


# 接到乘客之后，车和乘客和订单状态再刷新
# 默认将车刷新到格子中央
def meet_stat(drv, cust):
    order1 = [x for x in global_var.list_order if ((x.drvkey == drv.phone) & (x.custkey == cust.phone))]
    order = order1[0]
    refresh_stat(drv, 'drv', 2)
    refresh_stat(cust, 'cust', 2)
    refresh_stat(order, 'order', 2)
    center(drv, cust)
    print('drv' + drv.phone + ' ' + "get customer!")


# 送到目的地之后，车和乘客以及订单状态刷新
# 默认将车刷新到格子中央，订单进入Completed Order列表
def reach_stat(drv, order):
    cust_l = [x for x in global_var.objectscust if x.phone == order.custkey]
    cust = cust_l[0]
    refresh_stat(drv, 'drv', 0)
    drv.carry_image = None
    refresh_stat(cust, 'cust', 0)
    whether_pay(order)
    create_corder(order)


# 将已完成的订单移入 Completed Order 列表
def create_corder(order):
    drv = [x for x in global_var.objectscar if x.phone == order.drvkey][0]
    cust = [x for x in global_var.objectscust if x.phone == order.custkey][0]

    i = global_var.list_order.index(order)
    new_corder = order
    global_var.list_corder.append(new_corder)
    global_var.list_order.pop(i)
    mysql = 'insert into corders values("{orderkey}","{custkey}","{drvkey}",{log},{lat},{prize},{stat})'
    mysql_command = mysql.format(orderkey=new_corder.orderkey, custkey=new_corder.custkey, drvkey=new_corder.drvkey,
                                 log=new_corder.log, lat=new_corder.lat, stat=new_corder.state, prize=new_corder.prize)
    pay(drv, cust, order)
    try:
        db = MySQL()
        db.execute(mysql_command)
        db.connection.commit()
    except:
        db.connection.rollback()

        # 调用过程，把mysql中对应的order删掉，插入到c_order中去


def ccancel_order(cust, drv, order):
    refresh_stat(drv, 'drv', 0)
    refresh_stat(cust, 'cust', 0)
    order.state = 5  # 代表订单状态异常
    create_corder(order)  # 订单进入完成列表


def dcancel_order(cust, drv, order):
    refresh_stat(drv, 'drv', 0)
    refresh_stat(cust, 'cust', 3)
    c = cust.phone
    o = Order.create_id(c)
    d = 0
    t0 = time.clock()
    longitude = order.log
    latitude = order.lat
    amount = order.prize
    new_order = Order(o, c, d, longitude, latitude, 0, prize, t0)
    global_var.list_order.append(new_order)

    mysql = 'insert into orders values("{orderkey}","{custkey}","{drvkey}",{log},{lat},{prize},{stat})'
    mysql_command = mysql.format(orderkey=o, custkey=c, drvkey=d, log=longitude, lat=latitude, stat=0, prize=amount)
    db = MySQL()
    db.execute(mysql_command)
    db.connection.commit()
    order.state = 5  # 订单状态变为订单异常（接单后取消）
    create_corder(order)  # 订单进入完成列表


# 定义了一个函数判断是否取消订单,嵌套在search_car()内
def whether_cancel(cust, drv, order):
    pr = random.random()
    if pr < 0.1:
        refresh_stat(order, 'order', 5)
        ccancel_order(cust, drv, order)
    else:
        whether_crush(cust, drv, order)


# 客户有20%概率在司机到达格子之后拖延5秒再上车
# 定义了一个函数判断是否延迟上车
def whether_delay():
    pr = random.random()
    if pr < 0.2:
        return 1


# 客户有5%概率在到达后拒不付钱
# 定义了一个函数判断是否付钱
def whether_pay(order):
    pr = random.random()
    if pr >= 0.05:

        refresh_stat(order, 'order', 3)

    else:
        refresh_stat(order, 'order', 4)


def pay(drv, cust, order):
    if order.state == 3:
        if cust.acctbal >= order.prize:
            cust.acctbal -= round(order.prize, 1)
            drv.acctbal += round(order.prize, 1)
        else:
            pass
            # 乘客坐了霸王车


def whether_move(order, cust, time_passed):
    prob = random.random()
    if prob < 0.3:
        move_next(order, cust, time_passed)


# 定义了一个动身去往随机相邻格子的函数
def move_next(order, cust, time_passed):
        cust.state = 4
        search_car(order, cust, cust.log, cust.lat, time_passed)


# 定义了一个函数判断是否因撞车而取消订单
def whether_crush(cust, drv, order):
    pr = random.random()
    if pr < 0.05:
        dcancel_order(cust, drv, order)


# 司机有10%概率在去机场格子（中心格子）时因被交管局抓损失所有累计账户余额
# 这里把被交管局抓定义为罚款，停留10s，但可以继续完成当前订单
def caught_RTA(drv):
    drv.acctbal = 0

    sql = "UPDATE dida.driver SET acctbal = 0 WHERE drvkey ='{drvkey}' "
    sql_c = sql.format(drvkey=drv.phone)
    db = MySQL()
    db.execute(sql_c)
    db.connection.commit()

    drv.caught_time = global_var.current_time
    drv.state = 4  # 4代表被警察抓，罚款


# 定义了一个函数判断是否因被交管局抓而损失所有余额
def whether_RTA(drv):
    pr = random.random()
    if pr < 0.1:
        caught_RTA(drv)