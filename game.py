import policies
import puzzle
import player
import matplotlib.pyplot as plt
import algo_RL
import numpy as np
from os import getcwd
import actions
from datetime import datetime
import util
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
        self.track_reward={}
        self.graveyard=[]
        self.constructor()

    def is_equal_cord_x_y(self,cord_a,cord_b):
        for i in range(len(cord_a)):
            if cord_b[i] != cord_a[i]:
                return False
        return True

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
            p_player.rest_game()

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


    def check_if_player_at_goal(self,cord_x_y,p_player):
        '''
        check if player at one of the Goals
        :return: boolean var
        '''
        if p_player.is_adversarial:
            for goal_i in self.grid_world.get_gaols():
                if goal_i[0] == cord_x_y[0] and goal_i[1] == cord_x_y[1]:
                    return True
        return False


    def check_collusion_in_box(self,cord_x_y):
        list_player_collusion=[]
        for p in self.all_player:
            cord_x_y_of_p = p.get_coordinates()
            if self.is_equal_cord_x_y(cord_x_y_of_p,cord_x_y):
                list_player_collusion.append(p)

        acc = 0
        sign_array = [x.is_adversarial for x in list_player_collusion]
        acc = sum(sign_array)
            # add the new player
        if acc < len(sign_array) and acc > 0:
            return True,list_player_collusion
        return False,None


    def check_collusion(self,player_p,cord_x_y):
        '''
        check if collusion
        :return: boolean and the list_of the player name or none if there is no collusion
        '''
        players_name = self.grid_world.is_occupied(cord_x_y[0],cord_x_y[1])
        if players_name is not None:
            acc = 0
            sign_array = [x.is_adversarial for x in players_name]
            acc = sum(sign_array)
            # add the new player
            acc += player_p.is_adversarial
            if acc < len(sign_array)+1 and acc > 0:
                return True,players_name
        return False,None

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
        if self.check_if_player_at_goal(cord_x_y,player_p):
            # adversarial palyer is at the goal
            self.remove_player(player_p)
            msg='#Adversarial player is at the Goal - {}'.format(player_p.name)
            print(msg)
            return False,msg

        #check fo collusion
        bol,players_name_list = self.check_collusion_in_box(cord_x_y)
        if bol is True:
            str_names=''
            for p in players_name_list:
                if p == player_p:
                    continue
                self.grid_world.clean_player_box(p)
                str_names += '{}, '.format(p.name)
                r_reward = self.reward_calc(p)
                self.remove_player(p,r_reward)
            self.remove_player(player_p)
            str_names += '{}'.format(player_p.name)
            msg = '#Collusion - {}'.format(str_names)
            print(msg)
            return False, msg


        return True,None

    def set_graph_grid(self):
        self.grid_world.graph_grid = policies.grid_to_graph(self.grid_world)

    def is_end_no_player(self):
        '''
        The game is ending only if the are no bad player at the grid
        '''
        bad_ctr=0
        good_ctr=0
        for p in self.all_player:
            if p.is_adversarial:
                bad_ctr+=1
            else:
                good_ctr+=1
        if bad_ctr==0: # or good_ctr==0:
            return True
        return False

    def remove_player(self,player_p,r_reward=None,die=True):
        player_p.add_state_to_history(player_p.get_cur_state())
        print (player_p.history)

        # clean state
        #self.grid_world.clean_player_box(player_p)

        if r_reward is not None:
            # up date before death
            player_p.before_die(r_reward)

        if die:
            # set a dead sate
            player_p.set_dead_state()


        self.all_player.remove(player_p)
        self.graveyard.append(player_p)


    def reward_calc(self,player_p):
        '''
        This reward function
        case:
        1) out of grid
        2) collusion
        3) at the gaol (only for adversarial)
        4) out of budget

        :return: float
        '''
        reward=0
        cord_x_y = player_p.get_coordinates()


        if self.check_vaild_state(cord_x_y,player_p) is False:
            reward = -0.1
            return reward
        # check if the bad at the one of the goals
        if player_p.is_adversarial:
            bol = self.check_if_player_at_goal(cord_x_y,player_p)
            if bol is True:
                reward = 1
                return reward

        bol,l_p = self.check_collusion_in_box(cord_x_y)
        if bol is True:
            if player_p.is_adversarial:
                reward = -1
            else:
                reward = 1
            return reward

        #if player_p.budget <= 0.0:
        #    reward = -1
        #    return reward

        return reward

    def init_average_reward(self):
        '''
        init the tracker after the reward
        '''
        d_avg_reward={}
        d_avg_reward['ctr']=0
        for p in self.all_player :
            d_avg_reward[p.name]=0
        self.track_reward=d_avg_reward

    def start_the_game(self):
        self.init_average_reward()
        round_ctr=0
        is_end = False
        while(True):
            if is_end is True:
                break
            round_ctr+=1
            print (self)
            for player_i in self.all_player:
                wall=False
                is_alive = True
                old_state = player_i.get_cur_state()

                #clean state
                self.grid_world.clean_player_box(player_i)

                # add to the history
                player_i.add_state_to_history(old_state)

                # take a action acrodding the policy
                if player_i.is_dog:
                    a = player_i.play(self.grid_world.graph_grid)
                else:
                    a = player_i.play()
                # check for legal move

                #
                r = self.reward_calc(player_i)

                cord_x_y = player_i .get_coordinates()

                #up date if need
                #self.grid_world.set_player_box(player_i)

                if self.check_vaild_state(cord_x_y,player_i) is False:
                    # need to return to the old state
                    #self.grid_world.clean_player_box(player_i)
                    player_i.roll_back_old_state(old_state,player_i.name)
                    wall=True
                    #self.grid_world.set_player_box(player_i)

                player_i.update_policy(old_state, a, r)

                if wall is False:
                    is_alive,info = self.check_condition(cord_x_y, player_i)
                    if is_alive is False:
                        if self.is_end_no_player():
                            is_end=True
                            # add to the history
                            break

                if is_alive is True:

                    # add the player to the box if need it
                    self.grid_world.set_player_box(player_i)


            print ('End Round {}'.format(round_ctr))
        for player_live in  self.all_player:
            self.grid_world.clean_player_box(player_live)
        print("End Of Episode")
        return round_ctr,info


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

def trail_game(size,budget,iter_num,d_rl=None,path_data=None):
    m=size
    list_d_record=[]
    bad_starting_pos = [0,m]
    goal_pos = [(1,0),(m-1,0)]
    good_starting_pos = [int(m/2),0]

    my_game = Game('test_01',init_grid_bord(m+1,m+1,bad_starting_pos,good_starting_pos ,goal_pos))

    all_pathz=[]
    for goal_i in goal_pos:
        pathz_i = policies.get_short_path_from_grid(my_game.grid_world,(bad_starting_pos[0],bad_starting_pos[1])
                                    ,(goal_i[0],goal_i[1]))
        all_pathz.extend(pathz_i)


    for p in get_player(bad_start=(bad_starting_pos[0],bad_starting_pos[1],0)
            ,good_start=(good_starting_pos[0],good_starting_pos[1],0),budget=budget,policy_bad=all_pathz
            ,size_grid=size,dico_rl=d_rl):
        my_game.add_palyer(p)

    p=None

    #policy
    my_game.set_graph_grid()



    for i in range(iter_num):
        my_game.start_game()
        time_step ,info = my_game.start_the_game()
        list_d_record.append(get_info_out_state(my_game,info,time_step,i+1))


    df = pd.DataFrame(list_d_record)
    date_time = str(datetime.now()).replace('-','_').replace(' ','_').split('.')[0]
    df['acc_sum_collusion']=df['collusion'].cumsum()
    df['acc_sum_at_goal'] = df['at_goal'].cumsum()




    if d_rl is not None:
        index_conf=d_rl['index']
    else:
        index_conf="N_{}".format(size)
    if path_data is not None:
        df.to_csv('{}/game_C_{}.csv'.format(path_data,index_conf))

        # plotting
        polt_path = util.mkdir_system(path_data,'plots',False)
        plotting(df, index_conf, polt_path,['acc_sum_collusion','acc_sum_at_goal'])

        #### moving average
        for i in [200, 1000]:
            df['Reward_MA{}'.format(i)] = df['p1_good_acc_reward'].rolling(window=i).mean()
            df['TD_error_MA{}'.format(i)] = df['p1_good_acc_td_error'].rolling(window=i).mean()
            plotting(df, "{}_RL_acc_MA{}".format(index_conf,i), polt_path, ['Reward_MA{}'.format(i),'TD_error_MA{}'.format(i)])
        ######


    res_d ={ 'out_of_budget_p1':df['out_of_budget_p1'].sum(),'budget':budget,
            'collusion':df['collusion'].sum(),'at_goal':df['at_goal'].sum()
             ,'index_conf':index_conf}





    return res_d

def read_csv_config(path_p_conf):
    df_conf = pd.read_csv(path_p_conf)
    dict_df = df_conf.to_dict('index')
    return dict_df

def experiment_producer(path_p_conf='/home/ise/games/conf/config.csv',
                        out_path='/home/ise/games/catch'):
    d_conf = read_csv_config(path_p_conf)
    path_exp = util.mkdir_system(out_path,'exp')
    path_data = util.mkdir_system(path_exp ,'data')
    path_summ = util.mkdir_system(path_exp , 'summary')
    d_info=[]
    for entry_config in d_conf:
        init_exp(d_conf[entry_config],d_info,path_data)

    df = pd.DataFrame(d_info)
    df.to_csv('{}/game.csv'.format(path_summ))

def init_exp(d_param,d_l,path_data):
    iter_num = d_param["iter"]
    size_grid = d_param['size_grid']
    budget = d_param['budget']
    tmp_d = trail_game(size_grid, budget,iter_num,d_param,path_data)
    d_l.append(tmp_d)
    return d_l

def plotting(df,conf_num,path_save,list_line):
    list_color=['blue','green','red','black','magenta','cyan']
    if len(list_line)>len(list_color):
        print ('Cant output plot no color ')
        return
    for i in range(len(list_line)):
        plt.plot(df.index, list_line[i] , data=df, marker='', color=list_color[i], linewidth=1, label=list_line[i] )

    # Add title and axis names
    plt.title('Catch Game')
    plt.xlabel('Number of Episode ')
    plt.ylabel('Value')
    plt.legend()
    plt.savefig('{}/conf_{}.png'.format(path_save,conf_num))
    plt.close()

def get_info_out_state(game,info,time_step,episode_num):
    # check
    d={'X':game.grid_world.x_size,'Y':game.grid_world.y_size,
       'goals':game.grid_world.get_state_goals_str()}
    sum_dis=0
    ctr_p=0

    # get the RL data
    list_p  = game.get_all_player()
    for p in list_p:
        res_info_rl = p.get_RL_info()
        if res_info_rl is None:
            continue
        for k in res_info_rl.keys():
            d['{}_{}'.format(p.name,k)]=res_info_rl[k]

    for player_p in game.get_all_player():
        ctr_p+=1
        d["{}-point".format(player_p.name)]=str(player_p).split('\t')[0]
        d["{}-angle".format(player_p.name)] = str(player_p).split('\t')[1]
        d["{}-budget".format(player_p.name)] = str(player_p).split('\t')[2]

        #sum_dis += player_p.get_sum_distance()

    #d['distance']=float(sum_dis)/float(ctr_p)
    d['end'] = info
    d['episode_num']=episode_num
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



def get_player(bad_start,good_start,policy_bad=None,
               policy_good='RL',budget=15,size_grid=8,dico_rl=None):
    player_array=[]
    d_action = Game.basic_moves(cost_function_test)

    p1_good = player.Player('p1_good',d_action['king'],budget,is_bad=False)
    p1_good.set_starting_point(good_start[0],good_start[1],good_start[2])
    if policy_good =='dog':
        p1_good.is_dog=True
    if policy_good =='RL':
        rl = algo_RL.SarsaLamda()
        rl.init_q_matrix(size_grid,num_player=2)
        if dico_rl is not None:
            rl.set_variable(dico_rl)
        p1_good.RL_algo =  rl
    player_array.append(p1_good)

    #p3_good = player.Player('p3_good', d_action['king'], 15, is_bad=False)
    #p3_good.set_starting_point(0, 0, 90)
    #player_array.append(p3_good)

    p1_bad = player.Player('p2_bad', d_action['king'], budget*1.5, is_bad=True)
    p1_bad.set_starting_point(bad_start[0],bad_start[1],bad_start[2])
    if policy_bad is not None:
        if policy_bad[0] =='RL':
            rl_2 = algo_RL.SarsaLamda()
            rl_2.init_q_matrix(size_grid, num_player=2)
            p1_bad.RL_algo = rl_2
        else:
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


def cost_function_test(x,y,const=0.001):
    #return 0
    return float(abs(x-y))*const+0.2


# todo: if all good player die check if the bad plaer can get to the goal
if __name__ == "__main__":
    path_repo = getcwd()
    path_to_conf = '{}/{}/config.csv'.format(path_repo,'conf')
    print ('Starting.....')
    experiment_producer(path_p_conf=path_to_conf)
    exit()
