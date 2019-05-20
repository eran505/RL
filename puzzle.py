import puzzle_state

class Puzzle:

    def __init__(self,name, x ,y):
        self.name = name
        self.x_size = x
        self.y_size= y
        self.grid=[]
        self.end_goal=[]
        self.start_bad=[]
        self.start_good = []
        self.constructor_function()
        self.graph_grid=None

    def get_state_goals_str(self):
        str_goalz = ''
        for end_goal_i in self.end_goal:
            str_goalz+='({},{}) '.format(end_goal_i[0],end_goal_i[1])
        return str_goalz[:-1]

    def get_state_puzzle(self,x,y):
        return self.grid[x][y]

    def is_occupied(self,x,y):
        box_b = self.grid[x][y]
        res = []
        for p in box_b.palyer:
            res.append(p)
        if len(res) == 0 :
            return None
        return res
    def constructor_function(self):
        self.set_grid()

        #self.set_end_goal(8,7)

    def __str__(self):
        str_grid=''
        for x in self.grid:
            str_grid+='\n'
            for y in x:
                str_grid+="|{}".format(str(y))
        return str_grid

    def set_player_box(self,player_p):
        cord_pair = player_p.get_coordinates()
        puz_stata_s = self.grid[cord_pair[0]][cord_pair[1]]
        puz_stata_s.add_player(player_p)

    def clean_player_box(self,player_p):
        cord_pair = player_p.get_coordinates()
        puz_stata_s = self.grid[cord_pair[0]][cord_pair[1]]
        puz_stata_s.clean_player(player_p)

    def set_start_point_bad(self,x_coordinate,y_coordinate):
        self.grid[x_coordinate][y_coordinate].set_start_bad()
        self.start_bad.append([x_coordinate,y_coordinate])

    def set_start_point_good(self,x_coordinate,y_coordinate):
        self.grid[x_coordinate][y_coordinate].set_start_good()
        self.start_good.append([x_coordinate,y_coordinate])

    def set_grid(self):
        for i in range(self.x_size):
            tmp_list = []
            for j in range(self.y_size ):
                tmp_list.append(puzzle_state.Puzzle_State(' ',i,j))
            self.grid.append(tmp_list)



    def set_end_goal(self,x_coordinate,y_coordinate):
        self.grid[x_coordinate][y_coordinate].set_goal()
        self.end_goal.append([x_coordinate,y_coordinate])

    def get_gaols(self):
        return self.end_goal

    def is_vaild_move(self,x,y,diagonal=True):
        if x<0 or x>=self.x_size:
            return False
        if y<0 or y>=self.y_size:
            return False
        return True

    def get_the_shortest_path(self,x,y):
        pass

    def get_adjacency_state(self,state,diagonal=True):
        '''
                   North
                     |
             West -  -  - East
                     |
                   South

        :return: list of state
        '''
        x = state.x
        y = state.y
        adjacency_pos=[]
        wind_direction={'NW':{'ctr':0,'pos':[x-1,y+1]},'NE':{'ctr':0,'pos':[x+1,y+1]},'SW':{'ctr':0,'pos':[x-1,y-1]},'SE':{'ctr':0,'pos':[x+1,y-1]}}
        adjacency_pos.append([x,y])
        if x > 0:
            adjacency_pos.append([x-1,y])
            wind_direction['NW']['ctr']+=1
            wind_direction['SW']['ctr']+=1
        if x < self.x_size-1:
            adjacency_pos.append([x+1,y])
            wind_direction['NE']['ctr'] += 1
            wind_direction['SE']['ctr'] += 1
        if y > 0:
            adjacency_pos.append([x,y-1])
            wind_direction['SW']['ctr'] += 1
            wind_direction['SE']['ctr'] += 1
        if y< self.y_size-1:
            wind_direction['NW']['ctr'] += 1
            wind_direction['NE']['ctr'] += 1
            adjacency_pos.append([x,y+1])
        if diagonal:
            if len(adjacency_pos)==5:
                list_diagonal=[[x+1,y+1],[x+1,y-1],[x-1,y-1],[x-1,y+1]]
                adjacency_pos.extend(list_diagonal)
            else:
                valids=[v['pos'] for k, v in wind_direction.items() if v['ctr'] == 2]
                adjacency_pos.extend((valids))

        return adjacency_pos




if __name__ == "__main__":
    exit(0)
    print('......')
    obj = Puzzle('bla',15,10)
    print (obj)
    state_i = puzzle_state.Puzzle_State('A',9,5)
    ans = obj.get_adjacency_state(state_i)
    for x in ans:
        print (x)
    print ("size:\t",len(ans))