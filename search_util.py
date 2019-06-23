from math import sqrt

from queue import PriorityQueue


class A_star_node:

    def __init__(self,h_val,g_val,father_node,data_node):
        self.g=g_val
        self.h = h_val
        self.father = father_node
        self.data=data_node

    def get_g(self):
        return self.g

    def get_data(self):
        return self.data

    def get_f(self):
        return self.g+self.h

    def __str__(self):
        return str(self.data)

    def __lt__(self, other):
          return self.h < other.h

    def __eq__(self, other):
        return other.data == self.data

class A_star:

    def __init__(self,puzzle,func=None):
        self.search_space = puzzle
        self.open_list=PriorityQueue()
        self.close_list={}
        self.set_goals=[]
        self.agg_function = func
        self.candid_nodes={}
        # true == open list AND false == close list
        self.nodes_list_status={}

    def set_goal(self,goal):
        self.set_goals.append(goal)

    def set_list_goal(self,list_goalz):
        self.set_goals.extend(list_goalz)

    def start(self,node_start_data):
        ctr_expand=0
        h = self.calc_heuristic(node_start_data)
        g = 0
        s_node = A_star_node(h,g,None,node_start_data)
        self.open_list.put((h+g,s_node))
        while not self.open_list.empty():
            val  = self.is_end()
            if val is not None:
                print ("ctr_expand: ",ctr_expand)
                return val
            item = self.open_list.get()
            node_expend = item[1]
            g = node_expend.get_g()
            childs_list = self.search_space.generated_children(node_expend.get_data())
            ctr_expand+=1
            for child in childs_list:
                if str(child ) in self.nodes_list_status:
                    continue
                h = self.calc_heuristic(child)
                g_i = g + 1
                node_i  =  A_star_node(h,g_i,node_expend,child)
                f_val = node_i.get_f()
                if self.is_goal(child):
                    print("ctr_expand: ", ctr_expand)

                    print (node_i,end='\tF= ')
                    print (f_val,end='\tG= ')
                    print (node_i.g,end='\tH= ')
                    print (node_i.h)
                    self.unroll_sol(node_i)
                    print()
                    self.candid_nodes[str(node_i)]=node_i

                #self.nodes_list_status[str(node_i)]=True
                self.open_list.put((f_val,node_i))
            self.nodes_list_status[str(item)] = False
           #self.close_list[str(item)]=True
        print("ctr_expand: ", ctr_expand)
        return None

    def unroll_sol(self,sol_node):
        if sol_node is None:
            return
        self.unroll_sol(sol_node.father)
        print (sol_node,end=' -> ')

    def is_end(self):
        if len(self.candid_nodes)==0:
            return None
        res = []
        min_node = self.open_list.get()
        for candid in self.candid_nodes.values():
            if candid.get_f()<min_node[1].get_f():
                res.append(candid)
        self.open_list.put(min_node)
        if len(res) == 0:
            return None
        #debug
        for x in res:
            print(x)
        #debug
        return res

    def is_in_close_list(self,node_str):
        if node_str in self.close_list:
            return True
        return False

    def is_goal(self,node_data):
        for goal in self.set_goals:
            if goal == node_data:
                return True
        return False


    def calc_heuristic(self,data_node):
        res = []
        for goal_i in self.set_goals:
            res.append(data_node.heuristic(goal_i))
        h = min(res)
        return h


class Node:

    def __init__(self,x,y,t):
        self.x = x
        self.y = y
        self.time_step=t

    def set_time(self,time_step_t):
        self.time_step = time_step_t

    def __str__(self):
        return "({},{})-({})".format(self.x,self.y,self.time_step)

    def __eq__(self, other):
        if self.x == other.x and self.y==other.y and self.time_step == other.time_step:
            return True
        return False


    def heuristic(self,goal):
        if goal.time_step < self.time_step:
            return float('inf')
        res = sqrt( (goal.x - self.x )**2 + (goal.y - self.y)**2 )
        ###if goal.time_step < res
        return res

class Puzzle_search:

    def __init__(self,x,y):
        self.size_x = x
        self.size_y = y

    def generated_children(self,state_cur,diagonal=True):
        arr_child=[]
        x=state_cur.x
        y=state_cur.y
        time_t = state_cur.time_step
        if x + 1 < self.size_x:
            arr_child.append(Node(x+1,y,time_t+1))
        if x-1 >= 0:
            arr_child.append(Node(x - 1, y, time_t + 1))
        if y-1 >=0:
            arr_child.append(Node(x , y-1, time_t + 1))
        if y+1 < self.size_y:
            arr_child.append(Node(x , y+1, time_t + 1))
        if diagonal:
            if y+1 < self.size_y and x+1 < self.size_x:
                arr_child.append(Node(x+1, y + 1, time_t + 1))
            if y-1 >=0 and x+1 <self.size_x:
                arr_child.append(Node(x+1, y - 1, time_t + 1))
            if y+1<self.size_y and x-1 >=0:
                arr_child.append(Node(x-1, y + 1, time_t + 1))
            if y-1 >=0 and x-1 >= 0:
                arr_child.append(Node(x-1, y - 1, time_t + 1))

        return arr_child


def agg_min(list):
    return min(list)

if __name__ == "__main__":

    a = Node(0,9,0)
    path = [Node(9,7,0),Node(8,6,1),Node(7,5,2),Node(6,4,3),Node(5,3,4),Node(4,2,5)
            ,Node(3,1,6),Node(2,1,7),Node(1,1,8)]

    puzz = Puzzle_search(10,10)
    algo = A_star(puzz)
    algo.set_list_goal(path)
    algo.start(a)
    exit()

    res = puzz.generated_children(Node(9,5,3))
    for x in res:
        print (x)

