
from actions import Action
from actions import action_pos
import numpy as np
import random
from policies import shortest_path
import heuristic
from copy import deepcopy
from markov_state import Markov_State
import markov_state

class Player:

    def __init__(self,name,actions_list,budget_b,is_bad=False):
        self.name= name
        self.policy = None
        self.budget=budget_b
        self.cur_state=None
        self.start_angle=None
        self.action=actions_list
        self.short_paths=None
        self.RL_algo=None
        self.action_dico=None
        self.q_table={}
        self.is_dog=False
        self.history=[]
        self.is_adversarial=is_bad
        self.start_budget=budget_b
        self.starting_point = None
        self.get_action_list_to_dict()

    def __str__(self):
        x_y = self.get_coordinates()
        cur_angel = self.get_angel()
        return "x:{},y:{}\tangle:{}\tbudget:{}".format(x_y[0],x_y[1],cur_angel,round(self.budget,2))

    def set_starting_point(self,x,y,angle):
        self.starting_point=[x,y]
        self.start_angle=angle

    def get_RL_info(self,avg=True):
        if self.RL_algo is not None:
            d={}
            d['avg_td_error'] = self.RL_algo.cum_td_error/float(self.RL_algo.ctr_num_update)
            d['acc_td_error'] = self.RL_algo.cum_td_error
            d['acc_reward'] = self.RL_algo.cum_reward
            d['avg_reward'] = self.RL_algo.cum_reward/float(self.RL_algo.ctr_num_update)
            return d
        return None

    def get_starting_point(self):
        return deepcopy(self.starting_point)

    def get_cur_state(self):
        return markov_state.get_deep_copy_state(self.cur_state)

    def rest_game(self,clean_history=True):
        self.reset_budget()
        if clean_history:
            self.history=[]
        if self.RL_algo is not None:
            self.RL_algo.rest()

    def reset_budget(self):
        self.budget=self.start_budget
        if self.policy is not None:
            self.choose_policy()

    def set_policy(self,paths):
        self.short_paths=paths
        self.choose_policy()


    def choose_policy(self):
        '''
        choose one path out of the short_paths
        '''
        randomindex = random.randint(0, len(self.short_paths) - 1)
        choosen = self.short_paths[randomindex]
        d={}
        for i in range(len(choosen)):
            if i == len(choosen)-1:
                d[str(choosen[i])]=None
            else:
                d[str(choosen[i])]=choosen[i+1]
        self.policy=d

    def get_action_list_to_dict(self):
        d={}
        for action_a in self.action:
            d[action_a.name]=action_a
        self.action_dico=d


    def before_die(self,r):
        if self.RL_algo is not None:
            self.RL_algo.up_date_end_episode(r)

    def add_state_to_history(self,state_s):
        self.history.append(str(state_s))

    def get_coordinates(self):
        return self.cur_state.get_pos_by_name(self.name)

    def get_angel(self):
        return self.cur_state.get_angle_by_name(self.name)

    def set_state(self,state_a):
        self.cur_state=state_a

    def init_q_table(self):
        self.q_table={}

    def set_dead_state(self):
        self.cur_state.set_player(self.name,['nan','nan'],0)

    def set_player_first_pos(self,x,y,angle):
        pass

    def roll_back_old_state(self,old_state,name):
        old_x_y = old_state.get_pos_by_name(name)
        old_angle = old_state.get_angle_by_name(name)
        self.cur_state.set_player(name,old_x_y,old_angle)

    def max_q(self):
        return Action

    def dog_policy(self,G):
        all_player_ops = self.cur_state.get_all_players_pos()
        opennent_pos_list =[]
        key_word = 'good'
        if self.is_adversarial is False:
            key_word='bad'
        for key_name in all_player_ops.keys():
            if str(key_name).split('_')[1] == key_word:
                opennent_pos_list.append(all_player_ops[key_name])

        # assuming only one player in each side #TODO: fix that
        cur_pos = self.cur_state.get_pos_by_name(self.name)
        opnennt_pos = opennent_pos_list[0]
        pathz = shortest_path(G,(cur_pos[0],cur_pos[1]),(opnennt_pos [0],opnennt_pos [1]))
        self.set_policy(pathz)
        return Action

    def get_action_from_policy(self):
        pos = self.cur_state.get_pos_by_name(self.name)
        next_pos = self.policy["{}".format((pos[0],pos[1]))]
        action_str = action_pos(pos,next_pos)
        return self.action_dico[action_str]


    def play(self,G=None):

        if self.is_dog:
            self.dog_policy(G)
            action_a = self.get_action_from_policy()
        elif self.policy is not None:
            action_a=self.get_action_from_policy()
        else:
            action_a = self.get_action()
        self.take_action(action_a)

        return str(action_a)
        #if self.policy is None:
        #    self.update_q_table()

    def get_action(self,RL=True,epsilon=0.1):
        '''
        TODO: need to change the epsilon that will decid over time, that the policy will be detremanstic
        :param egreedy:
        :param epsilon:
        :return:
        '''
        state_str_s = str(self.cur_state)
        action_str = self.RL_algo.e_greedy_policy(state_str_s)
        action = self.action_dico[action_str]
        return action

    def get_sum_distance(self):
        d = self.get_dico_distance()
        return sum(d.values())


    def update_policy(self,old_state,old_action,r_reward):
        if self.RL_algo is not None:
            # get the max next action
            if str(old_state) == str(self.cur_state):
                # update
                self.RL_algo.update_out_of_bound_state(old_state,old_action,r_reward)
                return
            next_a = self.RL_algo.e_greedy_policy(str(self.cur_state),exploration=False)
            old_state_str = str(old_state)
            cur_state_str = str(self.cur_state)
            self.RL_algo.update_q_table(old_state_str,old_action,cur_state_str ,next_a,r_reward)

    def get_dico_distance(self):
        keyword_suffix = 'bad'
        if self.is_adversarial:
            keyword_suffix='good'
        my_pos = self.cur_state.get_pos_by_name(self.name)
        opponent_pos_list = self.cur_state.get_all_players_pos(keyword_suffix)
        d_dist={}
        for name in opponent_pos_list.keys():
            if opponent_pos_list[name][0] == 'nan':
                continue
            dis_i = heuristic.euclidean_distance(my_pos,opponent_pos_list[name])
            d_dist[name]= dis_i
        return d_dist





    # TODO::cum as integer insted of an object
    def take_action(self,action_a):
        '''
        This function take action and output new state and the correspond cost in the budget
        '''
        self.privous_state = str(self.cur_state)
        cost_budget = action_a.get_cost(self.get_angel())
        new_state = action_a.apply_action(self.cur_state, self.name)
        self.cur_state = new_state
        self.cur_state.update_budget(float(cost_budget),self.name)
        self.budget=float(self.budget)-float(cost_budget)
        return


    def cal_reward(self):
        '''
        two child in the same time can collide
        :return:
        '''
        # out of budget
        reward_sum = 0
        if self.budget<=0:
            reward_sum =- 1
        # if collusion
        dico_dist = self.get_dico_distance()
        ctr_collide=0
        for k in dico_dist.keys():
            if dico_dist[k]==0:
                ctr_collide+=1
        reward_sum += (1.0)*ctr_collide




if __name__ == "__main__":
    pass
