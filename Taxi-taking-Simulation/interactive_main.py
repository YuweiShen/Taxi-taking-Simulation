# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 20:38:11 2018

@author: Administrator
"""
from pygame.locals import *
import numpy as np
from simulation import *
from sql import *
import pygame

import os
import threading

#             R    G    B
white = (255,255,255)
black = (0,0,0)
gray = (128,128,128)
red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)
blue = (0,200,255)
bright_blue=(0,0,255)
pink=(255,228,225)
bright_pink=(255,192,203)
bright_gray=(200,200,200)

car_width = 100

main_dir = os.path.split(os.path.abspath(__file__))[0]

    
class Cust():
    def __init__(self, image, log, lat, speed, name, acctbal, state, phone):
        self.image = pygame.transform.scale(image, (picturewidth2, pictureheight2))
        self.speed = speed
        self.name = name
        self.state = state
        self.phone = phone
        self.acctbal = acctbal
        self.log = log
        self.lat = lat
        self.pos = image.get_rect().move(log, lat)

    def move(self, time_passed):
        if self.state == 0:
            self.pos = self.pos.move(np.dot(self.speed, random_walk()))
            if self.pos.left < 0:
                self.pos.left = 0
            elif self.pos.left > screensize:
                self.pos.left = screensize
            if self.pos.top <= 0:
                self.pos.top = 0
            elif self.pos.top >= screensize:
                self.pos.top = screensize
        elif self.state == 1 or self.state == 3:
            pass
        elif self.state == 2:
            olist = [x for x in global_var.list_order if x.custkey == self.phone]
            order = olist[0]
            dlist = [y for y in global_var.objectscar if y.phone == order.drvkey]
            drv = dlist[0]
            self.pos.left = drv.log
            self.pos.top = drv.lat
        elif self.state == 4:  # 客户没等到车来接，变得愤怒
            self.pos = self.pos.move(np.dot(5, random_walk()))
            if self.pos.left < 0:
                self.pos.left = 0
            elif self.pos.left > screensize:
                self.pos.left = screensize
            if self.pos.top <= 0:
                self.pos.top = 0
            elif self.pos.top >= screensize:
                self.pos.top = screensize

        self.log = self.pos.left
        self.lat = self.pos.top

    def render(self):
        if self.state != 2:
            gameDisplay.blit(self.image, (self.log, self.lat))
            w, h = self.image.get_size()
            bar_x = self.log + w / 2
            bar_y = self.pos.top - h / 3
            smallText = pygame.font.SysFont('TimesNewRoman', 10)
            TextSurf, TextRect = text_objects(translate(self, 'cust'), smallText)
            TextRect.center = (bar_x, bar_y)  # 把标题设置在y/4处
            gameDisplay.blit(TextSurf, TextRect)
        else:
            pass


# 建立车的类
class Drv():
    def __init__(self, image, log, lat, speed, name, acctbal, state, phone):
        self.image = pygame.transform.scale(image, (picturewidth1, pictureheight1))
        self.speed = speed
        self.phone = phone
        self.lat = lat
        self.log = log
        self.pos = image.get_rect().move(log, lat)
        self.name = name
        self.state = state
        self.acctbal = acctbal
        self.carry_image = None
        self.caught_time = None
        self.wait_time = None

    def move(self, time_passed):
        if self.state == 0:
            self.pos = self.pos.move(np.dot(3, random_walk()))
            if self.pos.left < 0:
                self.pos.left = 0
            elif self.pos.left > screensize:
                self.pos.left = screensize
            if self.pos.top <= 0:
                self.pos.top = 0
            elif self.pos.top >= screensize:
                self.pos.top = screensize
        elif self.state == 1:
            olist = [x for x in global_var.list_order if x.drvkey == self.phone]
            order = olist[0]
            o = order.custkey
            clist = [y for y in global_var.objectscust if y.phone == o]
            cust = clist[0]
            goto_aim(self, cust, 'cust')
        elif self.state == 2:
            self.carry(transport)
            olist = [x for x in global_var.list_order if x.drvkey == self.phone]
            order = olist[0]
            goto_aim(self, order, 'order')
        elif self.state == 3:
            if global_var.current_time - self.wait_time >= 5:
                self.state = 2
                self.wait_time = None
        elif self.state == 4:
            if global_var.current_time - self.caught_time >= 10:
                self.state = 2
                self.caught_time = None
        self.log = self.pos.left
        self.lat = self.pos.top

    def carry(self, image_carry):
        self.carry_image = pygame.transform.scale(image_carry, (picturewidth1, pictureheight1))

    def refresh_location1(self, x, y):
        self.pos = self.pos.move(np.dot(self.speed, (x, y)))
        self.log = self.pos.left
        self.lat = self.pos.top

    def render(self):
        self.log = self.pos.left
        self.lat = self.pos.top
        w, h = self.image.get_size()
        gameDisplay.blit(self.image, (self.log, self.lat))
        bar_x = self.log + w / 2
        bar_y = self.pos.bottom - h / 2
        smallText = pygame.font.SysFont('TimesNewRoman', 10)
        TextSurf, TextRect = text_objects(translate(self, 'drv'), smallText)
        TextRect.center = (bar_x, bar_y)  # 把标题设置在y/4处
        gameDisplay.blit(TextSurf, TextRect)
        if self.carry_image:
            gameDisplay.blit(self.carry_image, (self.log, self.lat))


def load_image(name):
    path = os.path.join(main_dir, 'data', name)
    return pygame.image.load(path)
# 获取司机和客户的key和账户信息


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def message_display(text):
    gameDisplay.fill(white)
    largeText = pygame.font.SysFont('TimesNewRoman', 40)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((screensize / 2), (screensize / 3))  # 把标题设置在y/4处
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()


def text_display(text, x, y):
    smallText = pygame.font.SysFont('TimesNewRoman', 26)
    TextSurf, TextRect = text_objects(text, smallText)
    TextRect.center = (x, y)  # 把标题设置在y/4处
    gameDisplay.blit(TextSurf, TextRect)


# 定义按钮： 在(x,y)坐标上画宽为w，高为h的矩形，ic是点击前的颜色，ac是鼠标点击后的颜色
def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))

        if click[0] == 1 and action is not None:
            time.sleep(1)
            action()

    smallText = pygame.font.SysFont('comicsansms', 10)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)


def login_d():
    gameDisplay.fill(white)
    num = 0
    global ck
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
        while num == 0:
            p = ask(gameDisplay, "phone", 100, 100)
            n = ask(gameDisplay, 'name', 100, 210)
            flag = 0
            for i in global_var.objectscar:
                if (i.phone == p) & (i.name == n):
                    flag = 1
            if flag == 1:
                gameDisplay.fill(white)
                message_display("welcome back!")
                ck = p
                num += 1
            else:
                gameDisplay.fill(white)
                message_display("user not exists!")
                time.sleep(1)
                game_intro()
        drv_interface()


def login_c():
    gameDisplay.fill(white)
    state = 1
    num = 0
    global ck
    while state:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
        while num == 0:
            p = ask(gameDisplay, "phone", 100, 100)
            n = ask(gameDisplay, 'name', 100, 210)

            flag = 0
            for i in global_var.objectscust:
                if (i.phone == p) & (i.name == n):
                    flag = 1
            if flag == 1:
                message_display("welcome back!")
                ck = p
                num += 1
            else:
                message_display("user not exists!")
                time.sleep(1)
                game_intro()
        cust_interface()


def charge_cust():
    num = 0
    global ck
    global customer
    while num == 0:
        gameDisplay.fill(white)
        a = ask(gameDisplay, "Amount", 100, 100)
        num += 1
    a = float(a)
    for x in global_var.objectscust:
        if x.phone == ck:
            old = x.acctbal
    refresh(global_var.objectscust, 'acctbal', old + a, ck)
    message_display('charge successfully!')
    time.sleep(3)
    return


def log_out():
    global ck
    ck = 'c'
    game_intro()


def drv_interface():
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        drv = [x for x in global_var.objectscar if x.phone == ck][0]
        message_display('welcome back ' + drv.name + ' !')

        button('log out', 100, 300, 60, 50, pink, bright_pink, log_out)
        button("main", 210, 300, 60, 50, red, bright_red, main)
        button('information', 310, 300, 60, 50, bright_blue, blue, show_information_drv)

        pygame.display.update()
        clock.tick(1)


def show_information_cust():
    global ck
    for a in global_var.objectscust:
        if a.phone == ck:
            x = a
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        text_display("phone number:" + ck, 200, 150)
        text_display("account balance:" + str(x.acctbal), 200, 250)
        button("return", 300, 300, 60, 60, blue, bright_blue, cust_interface)
        pygame.display.update()


def show_information_drv():
    global ck
    for a in global_var.objectscar:
        if a.phone == ck:
            x = a
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        text_display("phone number:" + ck, 200, 150)
        text_display("account balance:" + str(x.acctbal), 200, 250)
        button("return", 300, 300, 60, 60, blue, bright_blue, drv_interface)
        pygame.display.update()


def cust_interface():
    gameDisplay.fill(white)
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        cust = [x for x in global_var.objectscust if x.phone == ck][0]

        message_display('welcome back ' + cust.name + ' !')

        button('information', 310, 300, 60, 50, blue, bright_blue, show_information_cust)
        button("charge", 120, 300, 60, 50, green, bright_green, charge_cust)
        button("main", 210, 300, 60, 50, red, bright_red, main)
        button('log out', 30, 300, 60, 50, pink, bright_pink, log_out)
        pygame.display.update()
        clock.tick(1)
        # 输入框函数部分


# 定义输入框 用于注册界面


def get_key():
    while 1:
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            return event.key
        else:
            pass


def display_box(screen, message, x, y):
    fontobject = pygame.font.Font(None, 18)
    pygame.draw.rect(screen, (0, 0, 0),
                     (x,
                      y,
                      200, 20), 0)
    pygame.draw.rect(screen, (255, 255, 255),
                     (x,
                      y - 10,
                      204, 24), 1)
    if len(message) != 0:
        screen.blit(fontobject.render(message, 1, (255, 255, 255)), (x, y))
    pygame.display.flip()


# 输入框界面的第二个函数
def ask(screen, question, x, y):
    # "ask(screen, question) -> answer"
    pygame.font.init()
    current_string = []
    display_box(screen, question + ": " + "".join(current_string), x, y)
    while 1:
        inkey = get_key()
        if inkey == K_BACKSPACE:
            current_string = current_string[0:-1]
            display_box(screen, question + ": " + "".join(current_string), x, y)
        elif inkey == K_RETURN:
            break
        elif inkey == K_MINUS:
            current_string.append("_")
        elif inkey <= 127:
            current_string.append(chr(inkey))
            display_box(screen, question + ": " + "".join(current_string), x, y)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

    return "".join(current_string)


# 创建客户账号
def create_caccount():
    pygame.display.set_caption('dida taxi')
    num = 1
    state = 1
    while state:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)

        while num:
            n = ask(gameDisplay, "name", 100, 50)
            p = ask(gameDisplay, "phone number", 100, 150)
            a = ask(gameDisplay, "account balance", 100, 250)
            a = float(a)  # 转成数字
            longitude = random.random() * screensize  # 生成一个0-41的横坐标,一位小数
            latitude = random.random() * screensize  # 生成纵坐标

            mysql = "insert into customer values('{name}', '{phone}',{acctbal},{log},{lat},{stat});"
            mysql_command = mysql.format(name=n, phone=p, acctbal=a, log=longitude, lat=latitude, stat=0)
            db = MySQL()
            try:
                db.execute(mysql_command)
                db.connection.commit()
                message_display("Welcome!" + n)
            except:
                db.connection.rollback()
                message_display('Not successful!')
            mysql1 = "CREATE VIEW VC_'{name}' AS \
                      SELECT * FROM orders O WHERE O.custkey = '{phone}'\
                      UNION SELECT * FROM corders CO WHERE CO.custkey = '{phone}';"
            mysql_command1 = mysql1.format(name=n, phone=p)
            db.execute(mysql_command1)
            db.connection.commit()

            customer = get_clist()
            print(customer)
            c = Cust(people, random.randint(0, screensize / 10), random.randint(0, screensize / 10), 3,
                     customer.loc[len(customer) - 1, 'custkey'], a, customer.loc[len(customer) - 1, "stat"], p)
            global_var.objectscust.append(c)
            num = 0

        time.sleep(3)
        game_intro()


# 定义了一个创建客户用户的函数 在界面上提示输出姓名、电话、账户余额
# custkey是自增的，所以用NULL，坐标是随机生成的，默认客户状态刚创建完之后为0
def create_daccount():
    state = 1
    num = 1
    while state:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)

        while num:
            n = ask(gameDisplay, "name", 100, 50)
            c = ask(gameDisplay, "car number", 100, 90)
            p = ask(gameDisplay, "phone number", 100, 130)
            a = ask(gameDisplay, "account balance", 100, 170)
            a = float(a)  # 转成数字
            carcolor = ask(gameDisplay, "car color", 100, 210)
            car_type = ask(gameDisplay, "car tyoe", 100, 250)
            longitude = random.random() * screensize  # 生成一个0-41的横坐标
            latitude = random.random() * screensize  # 生成纵坐标

            sql1 = 'insert into car values("{carno}","{cartype}", "{carcol}")'
            sql1_command = sql1.format(carno=c, carcol=carcolor, cartype=car_type)
            mysql = "insert into driver values('{name}', {phone},'{carno}',{acctbal},{log},{lat},{stat});"
            mysql_command = mysql.format(name=n, carno=c, phone=p, acctbal=a, log=longitude, lat=latitude, stat=0)
            db = MySQL()
            try:
                db.execute(mysql_command)
                db.execute(sql1_command)
                db.connection.commit()
                driver = get_dlist()
                d = Drv(car, random.randint(0, screensize / 10), random.randint(0, screensize / 10), 5,
                        driver.loc[len(driver) - 1, 'drvkey'], a, driver.loc[len(driver) - 1, "stat"], p)
                global_var.objectscar.append(d)
                gameDisplay.fill(white)
                message_display("welcome!" + n)
            except:
                db.connection.rollback()
                gameDisplay.fill(white)
                message_display("not successful!")

            mysql1 = "CREATE VIEW VD_'{name}' AS \
                      SELECT * FROM orders O WHERE O.drvkey = '{phone}'\
                      UNION SELECT * FROM corders CO WHERE CO.drvkey = '{phone}';"
            mysql_command1 = mysql1.format(name=n, phone=p)
            db.execute(mysql_command1)
            db.connection.commit()

            num = 0

        time.sleep(3)
        game_intro()


def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        message_display("dida taxi")
        button("REGISTER", 60, 300, 70, 40, green, bright_green, register)
        button("LOGIN", screensize / 2 - 70 / 2, 300, 70, 40, blue, bright_blue, login)
        button("BOSS", 290, 300, 70, 40, red, bright_red, boss)
        pygame.display.update()
        clock.tick(1)


"""
def check_boss():
    num=0
    while 1:
        gameDisplay.fill(white)
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                pygame.quit()  
                quit()  
        while num==0:        
            n=ask(gameDisplay,'name',100,150)
            p=ask(gameDisplay,'password',100,250)
            if( n=='liujiajun')&( p=='shujukuqiu4.0'):
                message_display('Welcome! My boss')
                time.sleep(2)
                num+=1


            else:
                gameDisplay.fill(white)
                message_display('Not Successful!')
                time.sleep(2)
                game_intro()
        boss()


"""


def boss():
    while 1:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        message_display('Welcome! My boss')
        button('main', screensize / 4 - 70 / 2, 300, 70, 40, blue, bright_blue, main)
        button('log', screensize / 2 - 20, 300, 70, 40, red, bright_red, log)
        button('driver', 290, 300, 70, 40, green, bright_green, new_windowD)
        button('customer', 290, 240, 70, 40, pink, bright_pink, new_windowC)
        button('order', 290, 180, 70, 40, gray, bright_gray, new_windowO)
        pygame.display.update()
        clock.tick(1)


def log():
    sql = 'select * from logs'
    db = MySQL()
    db.execute(sql)
    l=db.cursor.fetchall()
    log = []
    for row in l:
        new_inf = []
        for i in range(len(row)):
            new_inf.append(row[i])
        log.append(new_inf)
    show_table(l, ['ID', 'Time', 'LogContent'])
    clock.tick(2)


def new_windowD():
    driver_table1()


def new_windowC():
    customer_table1()


def new_windowO():
    order_table1()


def order_table1():
    while 1:
        gameDisplay.fill(white)
        button('', 400, 400, 10, 10, red, bright_red, boss)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        show_table(global_var.list_order, ['custkey', 'prize', 'state', 'drvkey', 'log', 'lat'])
        pygame.display.update()
        clock.tick(0.5)


def customer_table1():
    while 1:
        gameDisplay.fill(white)
        button('', 400, 400, 10, 10, red, bright_red, boss)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        show_table(global_var.objectscust, ['name', 'acctbal', 'state', 'log', 'lat', 'phone'])
        pygame.display.update()
        clock.tick(0.5)


def driver_table1():
    while 1:
        gameDisplay.fill(white)
        button(' ', 400, 400, 10, 10, red, bright_red, boss)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        show_table(global_var.objectscar, ['name', 'acctbal', 'state', 'log', 'lat', 'phone'])
        pygame.display.update()
        clock.tick(0.5)


'''
def show_table(table,tablename):
    size=13
    pygame.font.init()
    smallText = pygame.font.SysFont('arial',size)
    for column in range(len(tablename)):
        TextSurf, TextRect = text_objects(str(tablename[column]), smallText)  
        TextRect.center = (50+column*60,size)
        gameDisplay.blit(TextSurf, TextRect)  
    for row in range(1,len(table)):
        for column in range(len(table[0])):
            TextSurf, TextRect = text_objects(str(table[row][column]), smallText)  
            TextRect.center = (50+column*60,size*(1+row))  
            gameDisplay.blit(TextSurf, TextRect)  
'''


def show_table(objectlist, tablename):
    size = 13
    pygame.font.init()
    smallText = pygame.font.SysFont('arial', size)
    for column in range(len(tablename)):
        TextSurf, TextRect = text_objects(str(tablename[column]), smallText)
        TextRect.center = (50 + column * 60, size)
        gameDisplay.blit(TextSurf, TextRect)

    for row in range(len(objectlist)):
        for column in range(len(tablename)):
            TextSurf, TextRect = text_objects(str(getattr(objectlist[row], tablename[column])), smallText)
            print(str(getattr(objectlist[row], tablename[column])))
            TextRect.center = (50 + column * 60, size * (2 + row))
            gameDisplay.blit(TextSurf, TextRect)


def login():
    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        message_display("Choose a type to continue")
        button("customer", 60, 300, 70, 40, blue, bright_blue, login_c)
        button("driver", screensize / 2 - 70 / 2, 300, 70, 40, green, bright_green, login_d)
        button("register", 290, 300, 70, 40, red, bright_red, register)

        pygame.display.update()
        clock.tick(1)


def register():
    gameDisplay.fill(white)
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        message_display("Choose a type to continue")

        button("customer", 60, 300, 70, 40, blue, bright_blue, create_caccount)
        button("driver", screensize / 2 - 70 / 2, 300, 70, 40, green, bright_green, create_daccount)
        button("login", 290, 300, 70, 40, red, bright_red, login)
        pygame.display.update()
        clock.tick(1)


def main_houtai():
   
    TRANSMIT_SQL = pygame.USEREVENT + 1  # 定义了 一个向数据库传递坐标的事件，10秒触发一次
    pygame.time.set_timer(TRANSMIT_SQL, 10000)
    SUBMIT_ORDER = pygame.USEREVENT + 2
    pygame.time.set_timer(SUBMIT_ORDER, 1000)
    while 1:
        global time_count  # 记录游戏界面刷新了几次
        time_count += 1
        time_passed = clock.tick(5) / 1000.0
        global_var.current_time = time_count * time_passed
    
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == TRANSMIT_SQL:
                transmit()
            elif event.type == SUBMIT_ORDER:
                submit_order()

        if len(global_var.list_order) > 0:
            search_carinol(time_passed)

        for o in global_var.objectscar:
            o.move(time_passed)

        for p in global_var.objectscust:
            p.move(time_passed)
      
# 车和人跑路的主界面
def main():
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        button("", 400, 400, 10, 10, red, bright_red, boss)
        for o in global_var.objectscar:
            o.render()
        for p in global_var.objectscust:
            p.render()
        pygame.display.update()
    """
    TRANSMIT_SQL = pygame.USEREVENT+1   #定义了 一个向数据库传递坐标的事件，10秒触发一次
    pygame.time.set_timer(TRANSMIT_SQL,10000)
    SUBMIT_ORDER = pygame.USEREVENT+2
    pygame.time.set_timer(SUBMIT_ORDER,5000)
    while 1:
        global time_count   #记录游戏界面刷新了几次
        global current_time
        time_count += 1
        time_passed = clock.tick(5)/1000.0
        current_time = time_count*time_passed




        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()      
            elif event.type == TRANSMIT_SQL: 
                transmit()
            elif event.type == SUBMIT_ORDER:
                submit_order(time_passed)

        if len(global_var.list_order)>0:
            search_carinol(time_passed)
            """


if __name__ == '__main__':
    
    time_count = 0
    current_time = 0
    inuse = 0
    ck = "a"
    pygame.font.init()
    list_corder = []
    pygame.init() 
    # pygame.mixer.init()
    clock = pygame.time.Clock()
    # music = 'C:/Users/Administrator/Desktop/Zigeunerweisen.mp3'
    # pygame.mixer.music.load(music)
    # pygame.mixer.music.play()
    gameDisplay = pygame.display.set_mode( (screensize,screensize), RESIZABLE)
    
    pygame.display.set_caption('dida taxi')  
    
    initialization() 
    customer = get_clist()
    car = load_image('C:/Users/Administrator/Desktop/car.png').convert_alpha()
    transport = load_image('C:/Users/Administrator/Desktop/车和人.png').convert_alpha()
    people = load_image("C:/Users/Administrator/Desktop/人.png").convert_alpha()
    print(customer)
    for x in range(len(customer)):
        p = Cust(people, random.randint(0, screensize), random.randint(0, screensize), 3,
                 customer.loc[x, "name"].lower(), customer.loc[x, "acctbal"], customer.loc[x, "stat"],
                 customer.loc[x, 'phone'])
        global_var.objectscust.append(p)
    
    driver = get_dlist()
    print(driver)
    
    for y in range(len(driver)):
      
        o = Drv(car, random.randint(0, screensize), random.randint(0, screensize), 5, driver.loc[y, "name"].lower(),
                driver.loc[y, "acctbal"], driver.loc[y, "stat"], driver.loc[y, 'phone'])
        global_var.objectscar.append(o)
 
    t1=threading.Thread(target=main_houtai,args=())
    t1.start()
    print('start new thread!')
    game_intro()


