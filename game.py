import policies
import puzzle
import player
import actions
from datetime import datetime
from numpy import sum
import  pandas as pd
from markov_state import Markov_State

class Game:

    def __init__(self,name,puzzle):
        self.name = name
        self.good_players=[]
        self.grid_world = puzzle
        self.adversarial_player=[]
        self.moves=None
        self.all_player=[]
        self.graveyard=[]
        self.constructor()

    def get_all_player(self):
        list_player=[]
        list_player.extend(self.graveyard)
        list_player.extend(self.all_player)
        return list_player

    def constructor(self):
        pass

    def start_game(self):

        for i in range(len(self.graveyard)):
            self.all_player.append(self.graveyard[i])
        self.graveyard=[]


        genric_state = Markov_State()
        for p_player in self.all_player:
            genric_state.set_player(p_player.name,p_player.get_starting_point(),p_player.start_angle)
            genric_state.set_budget_by_name(p_player.name,p_player.start_budget)

        for p_player in self.all_player:
            starting_state = genric_state
            p_player.set_state(starting_state)
            self.grid_world.set_player_box(p_player)
            p_player.reset_budget()

    def add_palyer(self,player):
        for player_i in self.all_player:
            if player_i.name == player.name:
                print('the player is all ready exists')
        self.all_player.append(player)


    #def add_bad_player(self,player):
    #    for player_i in self.adversarial_player:
    #        if player_i.name == player.name:
    #            print('the player is all ready exists')
    #    self.adversarial_player.append(player)

    #def add_good_player(self, player):
    #    for player_i in self.good_players:
    #        if player_i.name == player.name:
    #            print('the player is all ready exists')
    #    self.good_players.append(player)
    @staticmethod
    def basic_moves(func):
        '''
        define two types of action set
        '''
        N_move = actions.Action_North('N', func)
        S_move = actions.Action_South('S', func)
        E_move = actions.Action_East('E', func)
        W_move = actions.Action_West('W', func)
        NE_move = actions.Action_North_East('NE', func)
        NW_move = actions.Action_North_West('NW', func)
        SE_move = actions.Action_South_East('SE', func)
        SW_move = actions.Action_South_West('SW', func)
        basic_moves = [N_move, S_move, E_move, W_move]
        king_moves = [N_move, S_move, E_move, W_move,
                      NE_move, NW_move, SE_move, SW_move]
        return  {'basic': basic_moves, 'king': king_moves}



    def check_vaild_state(self,cord_x_y,player_p):
        '''
        deal with ilegal moves
        :return: True or False
        '''
        # check if the move is legal
        return self.grid_world.is_vaild_move(cord_x_y[0],cord_x_y[1])


    def check_condition(self,cord_x_y,player_p):
        '''
        End the game in case of:
            1. no budget
            2. collusion
        :return: True or False
        '''



        # check if out of budget
        if player_p.budget<=0.0:
            #assert (self.remove_player(player_p)==True,'cant remove player -> {}'.format(player_p.name))
            self.remove_player(player_p)
            msg='#Out of Budget - {}'.format(player_p.name)
            print(msg)

            return False,msg


        #check if the player at the Goal:
        if player_p.is_adversarial:
            for goal_i in self.grid_world.get_gaols():
                if goal_i[0] == cord_x_y[0] and goal_i[1] == cord_x_y[1]:
                    # adversarial palyer is at the goal
                        self.remove_player(player_p)
                        msg='#Adversarial player is at the Goal - {}'.format(player_p.name)
                        print(msg)
                        return False,msg

        #check fo collusion
        players_name = self.grid_world.is_occupied(cord_x_y[0],cord_x_y[1])
        # a player found in the same box
        if players_name is not None:
            acc = 0
            str_names = ''
            sign_array = [x.is_adversarial for x in players_name]
            acc = sum(sign_array)
            # add the new player
            acc+=player_p.is_adversarial
            if acc < len(sign_array) or acc > 0:
                for p in players_name :
                    self.grid_world.clean_player_box(p)
                    str_names+='{}, '.format(p.name)
                    self.remove_player(p)
                self.remove_player(player_p)
                str_names+='{}'.format(player_p.name)
                msg='#Collusion - {}'.format(str_names)
                print(msg)
                return False,msg


        return True,None

    def set_graph_grid(self):
        self.grid_world.graph_grid = policies.grid_to_graph(self.grid_world)

    def is_end_no_player(self):
        bad_ctr=0
        good_ctr=0
        for p in self.all_player:
            if p.is_adversarial:
                bad_ctr+=1
            else:
                good_ctr+=1
        if bad_ctr==0 or good_ctr==0:
            return True
        return False

    def remove_player(self,player_p):
        player_p.add_state_to_history(player_p.get_cur_state())
        print (player_p.history)
        self.all_player.remove(player_p)
        self.graveyard.append(player_p)

    def start_the_game(self):
        round_ctr=0
        is_end = False
        while(True):
            if is_end is True:
                break
            round_ctr+=1
            print (self)
            for player_i in self.all_player:
                old_state = player_i.get_cur_state()

                #clean state
                self.grid_world.clean_player_box(player_i)

                # add to the history
                player_i.add_state_to_history(old_state)

                # take a action acrodding the policy
                if player_i.is_dog:
                    r = player_i.play(self.grid_world.graph_grid)
                else:
                    r = player_i.play()
                # check for legal move
                cord_x_y = player_i .get_coordinates()
                if self.check_vaild_state(cord_x_y,player_i) is False:
                    # need to return to the old state
                    player_i.roll_back_old_state(old_state,player_i.name)

                else:
                    not_end,info = self.check_condition(cord_x_y, player_i)
                    if not_end is False:
                        if self.is_end_no_player():
                            is_end=True
                            # add to the history

                            break
                # add the player to the box if need it
                self.grid_world.set_player_box(player_i)


            print ('End Round {}'.format(round_ctr))
        for player_live in  self.all_player:
            self.grid_world.clean_player_box(player_live)
        print("End Of Episode")
        return round_ctr,info

    def remove_player_by_name(self,name):
        for player_i in self.all_player:
            if player_i.name == name:
                self.all_player.remove(player_i)
                return True
        return False

    def __str__(self):
        str_res = str(self.grid_world)
        str_res+='\n\n'
        for p in self.all_player:
            str_res+="{}" \
                     "- \t".format(p.name)
            str_res+=str(p)
            str_res+='\n'

        return str_res


######################################################################################################
######################################################################################################
######################################################################################################

#from policies import get_short_path_from_grid

def trail_game(size,budget):
    m=size
    list_d_record=[]
    bad_starting_pos = [0,m]
    goal_pos = [(1,0),(m,0)] #,
    good_starting_pos = [0,0]

    my_game = Game('test_01',init_grid_bord(m+1,m+1,bad_starting_pos,good_starting_pos ,goal_pos))

    all_pathz=[]
    for goal_i in goal_pos:
        pathz_i = policies.get_short_path_from_grid(my_game.grid_world,(bad_starting_pos[0],bad_starting_pos[1])
                                    ,(goal_i[0],goal_i[1]))
        all_pathz.extend(pathz_i)


    for p in get_player(bad_start=(bad_starting_pos[0],bad_starting_pos[1],0)
            ,good_start=(good_starting_pos[0],good_starting_pos[1],0),policy_bad=all_pathz,budget=budget):
        my_game.add_palyer(p)

    p=None

    #policy
    my_game.set_graph_grid()



    for i in range(100):
        my_game.start_game()
        time_step ,info = my_game.start_the_game()
        list_d_record.append(get_info_out_state(my_game,info,time_step))

    df = pd.DataFrame(list_d_record)
    date_time = str(datetime.now()).replace('-','_').replace(' ','_').split('.')[0]
    #df.to_csv('/home/ise/games/catch/budget/game_{}.csv'.format(size))
    res_d ={'mean_dist':df['distance'].mean(), 'out_of_budget_p1':df['out_of_budget_p1'].sum(),
            'collusion':df['collusion'].sum(),'at_goal':df['at_goal'].sum()}
    return res_d

def get_info_out_state(game,info,time_step):
    # check
    d={'X':game.grid_world.x_size,'Y':game.grid_world.y_size,
       'goals':game.grid_world.get_state_goals_str()}
    sum_dis=0
    ctr_p=0

    for player_p in game.get_all_player():
        ctr_p+=1
        d["{}-point".format(player_p.name)]=str(player_p).split('\t')[0]
        d["{}-angle".format(player_p.name)] = str(player_p).split('\t')[1]
        d["{}-budget".format(player_p.name)] = str(player_p).split('\t')[2]

        sum_dis += player_p.get_sum_distance()

    d['distance']=float(sum_dis)/float(ctr_p)
    d['end'] = info

    d['out_of_budget_p1'] = 0
    d['collusion'] = 0
    d['at_goal']=0

    if str(info).startswith('#O'):
        d['out_of_budget_p1']=1
    elif str(info).startswith('#C'):
        d['collusion']=1
    elif str(info).startswith('#A'):
        d['at_goal'] = 1


    d['round'] = time_step
    return d



def get_player(bad_start,good_start,policy_bad=None,policy_good='dog',budget=15):
    player_array=[]
    d_action = Game.basic_moves(cost_function_test)

    p1_good = player.Player('p1_good',d_action['king'],budget,is_bad=False)
    p1_good.set_starting_point(good_start[0],good_start[1],good_start[2])
    if policy_good =='dog':
        p1_good.is_dog=True
    player_array.append(p1_good)

    #p3_good = player.Player('p3_good', d_action['king'], 15, is_bad=False)
    #p3_good.set_starting_point(0, 0, 90)
    #player_array.append(p3_good)

    p1_bad = player.Player('p2_bad', d_action['king'], budget*1.2, is_bad=True)
    p1_bad.set_starting_point(bad_start[0],bad_start[1],bad_start[2])
    if policy_bad is not None:
        p1_bad.set_policy(policy_bad)
    player_array.append(p1_bad)
    return player_array


def init_grid_bord(x,y,start_bad,start_good,end_goal):
    gird = puzzle.Puzzle('grid', x, y)
    gird.set_start_point_bad(start_bad[0],start_bad[1])
    gird.set_start_point_good(start_good[0], start_good[1])
    for end_i in end_goal:
        gird.set_end_goal(end_i [0],end_i [1])
    return gird


def cost_function_test(x,y,const=0.01):
    return float(abs(x-y))*const+0.5


# todo: if all good player die check if the bad plaer can get to the goal
if __name__ == "__main__":
    print('puzzle_sate class')
    for n in range (10,11):
        d_l=[]
        for i in range(15,26):
            tmp_d = trail_game(n,i)
            tmp_d['k']=i
            d_l.append(tmp_d)

        df = pd.DataFrame(d_l)
        df.to_csv('/home/ise/games/catch/game_res_N_{}.csv'.format(n))
    #print (d)
