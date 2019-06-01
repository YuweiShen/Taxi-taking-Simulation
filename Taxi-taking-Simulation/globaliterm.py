import random

global screensize

screensize = 410
picturewidth1 = 32
pictureheight1 = 20
picturewidth2 = 7
pictureheight2 = 15

wait_time = 10



class global_var():
    objectscust = []
    list_order = []
    objectscar = []
    list_corder= []
    current_time=None
    def get_objectscust(self):
        return global_var.objectscust
    def get_list_order(self):
        return global_var.list_order
    def get_objectscar(self):
        return global_var.objectscar

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
