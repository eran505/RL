
from abc import ABCMeta, abstractmethod


def action_pos(cur_point,to_point):
    x_cur = cur_point[0]
    y_cur= cur_point[1]
    x_to = to_point[0]
    y_to = to_point[1]
    if x_cur+1==x_to and y_cur+1==y_to:
        return 'SE'
    elif x_cur==x_to and y_cur+1==y_to:
        return 'E'
    elif x_cur==x_to and y_cur-1==y_to:
        return 'W'
    elif x_cur+1==x_to and y_cur==y_to:
        return 'S'
    elif x_cur - 1 == x_to and y_cur == y_to:
        return 'N'
    elif x_cur + 1 == x_to and y_cur-1 == y_to:
        return 'SW'
    elif x_cur -1  == x_to and y_cur + 1 == y_to:
        return 'NE'
    elif x_cur - 1 == x_to and y_cur - 1 == y_to:
        return 'NW'
    else:
        raise Exception('Cant find the Action between the {0} --> {1}'.format(cur_point,to_point))


class Action(object, metaclass=ABCMeta):

    @abstractmethod
    def __init__(self,name,cost_function,cost_number=0):
        self.name= name
        self.dico_direction={'N':90,'S':270,'E':0,'W':180,'NE':45,'NW':135,'SE':315,'SW':225}
        self.cost = cost_number
        self.player_func_cost=cost_function
        self.angle = self.dico_direction[self.name]

    @abstractmethod
    def apply_action(self):
        pass

    def get_cost(self,angle):
        res = self.player_func_cost(angle,self.dico_direction[self.name])
        #print ('cost of the action: {0}'.format(res))
        return res

    def __str__(self):
        return '{}'.format(self.name)




class Action_North(Action):

    def __init__(self,name,cost):
        super().__init__(name,cost)


    def apply_action(self,cur_direction,name):
        cur_direction.player_position[name][0]-=1
        cur_direction.player_angle[name]=self.dico_direction[self.name]
        return cur_direction


class Action_South(Action):

    def __init__(self,name,cost):
        super().__init__(name,cost)

    def apply_action(self,cur_direction,name):
        cur_direction.player_position[name][0]+=1
        cur_direction.player_angle[name]=self.dico_direction[self.name]
        return cur_direction

class Action_East(Action):

    def __init__(self,name,cost):
        super().__init__(name,cost)

    def apply_action(self,cur_direction,name):
        cur_direction.player_position[name][1]+=1
        cur_direction.player_angle[name]=self.dico_direction[self.name]
        return cur_direction

class Action_West(Action):

    def __init__(self,name,cost):
        super().__init__(name,cost)


    def apply_action(self,cur_direction,name):
        cur_direction.player_position[name][1]-=1
        cur_direction.player_angle[name]=self.dico_direction[self.name]
        return cur_direction

class Action_North_West(Action):

    def __init__(self, name, cost):
        super().__init__(name, cost)

    def apply_action(self,cur_direction,name):
        cur_direction.player_position[name][1] -= 1
        cur_direction.player_position[name][0] -= 1
        cur_direction.player_angle[name]=self.dico_direction[self.name]
        return cur_direction

class Action_North_East(Action):

    def __init__(self, name, cost):
        super().__init__(name, cost)

    def apply_action(self,cur_direction,name):
        cur_direction.player_position[name][1] += 1
        cur_direction.player_position[name][0] -= 1
        cur_direction.player_angle[name]=self.dico_direction[self.name]
        return cur_direction

class Action_South_East(Action):

    def __init__(self, name, cost):
        super().__init__(name, cost)

    def apply_action(self,cur_direction,name):
        cur_direction.player_position[name][1] += 1
        cur_direction.player_position[name][0] += 1
        cur_direction.player_angle[name]=self.dico_direction[self.name]
        return cur_direction


class Action_South_West(Action):

    def __init__(self, name, cost):
        super().__init__(name, cost)

    def apply_action(self,cur_direction,name):
        cur_direction.player_position[name][1] -= 1
        cur_direction.player_position[name][0] += 1
        cur_direction.player_angle[name]=self.dico_direction[self.name]
        return cur_direction


####################################################
def cost_function_test(x,y,const=0.01):

    return float(abs(x-y))*const

if __name__ == '__main__':

    a= Action_South('S',cost_function_test)
    print (a.get_cost())
    print (a)

