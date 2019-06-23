import numpy as np
import random
import queue

class SarsaLamda:
    '''
    Repeat for each episode
        take action A observe R,S^
        Choose A^ from S^ using policy (e,g, e-greedy)
        Update rule :

        TD_error = R + discount_factor * Q(S^,A^) - Q(S,A)

        E(S,A) <-- E(S,A) + 1

        for all states :
            Q(s,a) <-- Q(s,a) + step_size * TD_error * E(s,a)
            E(s,a) <-- discount_factor * lamda *E(s,a)
        S<--S^ A<--A^
    '''
    def __init__(self):
        self.q_table={}
        self.eligibility_q = {}
        self.eligibility_table={}
        self.lamda=0.6
        self.discount_factor=0.7
        self.epslion=0.05
        self.step_size = 0.005
        self.matrix_q = None
        self.epslion_eligibility=0.0009
        self.ctr_state=0
        self.action_map={}
        self.cum_reward=0
        self.cum_td_error=0
        self.ctr_num_update=0
        self.time_seq=0

    def get_step_size(self):
        if isinstance(self.step_size, str):
            if self.step_size=='t':
                return 1.0/self.time_seq
            if self.step_size=='t^2':
                return 1.0 / pow(self.time_seq,2)

        return self.step_size

    def set_variable(self,d):
        if 'lambda' in d:
            self.lamda=float(d['lambda'])
        if 'discount_factor' in d:
            self.discount_factor = float(d['discount_factor'])
        if 'epsilon' in d:
            self.epslion=float(d['epsilon'])
        if 'step_size' in d:
            if str(d['step_size']) == 't':
                self.step_size = str(d['step_size'])
            elif str(d['step_size']) == 't^2':
                self.step_size = str(d['step_size'])
            else:
                self.step_size=float(d['step_size'])
        if 'eligibility' in d :
            self.epslion_eligibility=float(d['eligibility'])

    def rest(self):
        self.eligibility_q={}
        self.cum_reward = 0
        self.cum_td_error = 0
        self.ctr_num_update=0

    def calc_td_error(self,reward,q_vale,q_value_next=None):
        # time ctr ++
        self.time_seq+=1
        # update the number of updates that done
        self.ctr_num_update+=1
        # up date the acc reward
        self.cum_reward+=reward

        if q_value_next is None:
            td_error =  float(reward) - q_vale
        else:
            td_error= float(reward) + (self.discount_factor * q_value_next) - q_vale
        # update the td_error acc
        self.cum_td_error+=td_error
        return td_error

    def update_q_table(self,stat_cur,action_cur,next_state,next_action,reward):
        q_val_cur,cur_state_entry,cur_action_entry = self.get_q_value(stat_cur,action_cur)
        q_val_next,next_state_entry,next_action_entry = self.get_q_value(next_state, next_action)

        #td_error = float(reward) + self.discount_factor * q_val_next - q_val_cur
        td_error = self.calc_td_error(reward,q_val_cur,q_val_next)
        self.update_eligibility(cur_state_entry,cur_action_entry )
        self.update_all_recent_state(td_error)

    def update_out_of_bound_state(self,state_s,action_a,reward_r):
        q_val_cur, cur_state_entry, cur_action_entry = self.get_q_value(state_s, action_a)
        self.update_eligibility(cur_state_entry, cur_action_entry )
        self.up_date_end_episode(reward_r)

    def update_all_recent_state(self,td_error):
        '''
        this function goes itreativly over all state in the eligibility_q and update them according the
        TD error

        '''
        step_size_var = self.get_step_size()
        for k in self.eligibility_q:
            entry_array=str(k).split('_') #frist state , second action
            cur_state_entry=int(entry_array[0])
            cur_action_entry = int(entry_array[1])
            eligibility_val = self.eligibility_q[k]
            q_val = self.matrix_q[cur_state_entry,cur_action_entry ]
            self.matrix_q[cur_state_entry,cur_action_entry ] = q_val + float(step_size_var) * td_error * eligibility_val
        self.lower_eligibility_trace()

    def up_date_end_episode(self,reward):

        #TODO: need to look this up cuz it need to be the state in which the other players are and not the last one

        str_state_action = self.get_last_sate_action()
        state_entry = int(str(str_state_action ).split('_')[0])
        action_entry = int(str(str_state_action).split('_')[1])
        q_val = self.matrix_q[state_entry,action_entry]
        td_error = self.calc_td_error(reward,q_val,None)
        ##td_error =  (reward - q_val)
        self.update_all_recent_state(td_error)


    def get_last_sate_action(self):
        target_state_action = min(self.eligibility_q, key=self.eligibility_q.get)
        return target_state_action

    def update_eligibility(self,str_state,action_a):
        key_i = "{}_{}".format(str_state,action_a)
        if key_i not in self.eligibility_q:
            self.eligibility_q[key_i]=0
        self.eligibility_q[key_i]+=1

    def lower_eligibility_trace(self):
        '''
        lower all the Eligibility Trace for each state-action pair
        '''
        to_del = []
        for k in self.eligibility_q:
            if self.eligibility_q[k] <= self.epslion_eligibility:
                to_del.append(k)
            else:
                self.eligibility_q[k]=self.eligibility_q[k]*self.lamda*self.discount_factor
        for key_i in to_del:
            del self.eligibility_q[key_i]

    def e_greedy_policy(self,state_str_s,exploration=True):
        """
        @:param state_str_s to_string of a state
        """
        # check that the state in the matrix
        if state_str_s not in self.q_table:
            entry_state_val = self.set_state_q_table(state_str_s)
        else:
            entry_state_val = self.q_table[state_str_s]

        # draw a number for the exploration
        if np.random.rand() < self.epslion and exploration:
            # exploration a new action
            l_action = list(self.action_map.values())
        else:
            # in case there is two or more max q values
            all_action = np.argwhere(self.matrix_q[entry_state_val, :] == np.amax(self.matrix_q[entry_state_val, :]))
            l_action = all_action.flatten().tolist()

        # choose one action randomly
        action = random.choice(l_action)
        #action = l_action[action_num]
        return self.num_to_action(action)

    def num_to_action(self,num):
        for k,v in self.action_map.items():
            if num == v:
                return k
        raise Exception('no value in the action map that is map to action a {} -> {}'
                        .format(num,self.action_map))

    def get_q_value(self,state_str,action_a):
        state_str = str(state_str)
        entry_val_action = self.action_map[action_a]
        if state_str in self.q_table:
            entry_val_state = self.q_table[state_str]
            return self.matrix_q[entry_val_state,entry_val_action],entry_val_state,entry_val_action
        else:
            entry_val_state = self.set_state_q_table(state_str)
            return self.matrix_q[entry_val_state,entry_val_action],entry_val_state,entry_val_action


    def set_state_q_table(self,state_str):
        self.q_table[state_str]=self.ctr_state
        entry_val = self.ctr_state
        self.ctr_state+=1
        return entry_val

    def main_function(self):
        pass

        # get the current state of the agent
        # get the next action accroding the policy
        # get the next state
        # get the reward
        # boot strap from the next state , next action




    def init_q_matrix(self,size_grid,num_player,action_size=8,angle=8):
        boxes = size_grid+1
        state_size_overall = pow(pow(boxes,2)*angle,num_player) + 1
        self.matrix_q = np.zeros((state_size_overall,action_size))
        self.action_map={'N':0,'S':1,'E':2,'W':3
                         ,'NE':4,'NW':5,'SE':6,'SW':7}

        self.eligibility_q = queue.Queue(maxsize=size_grid)


if __name__ == "__main__":

    exit()
    rl = SarsaLamda()
    rl.init_q_matrix(3,10)
    print (rl.matrix_q)
    print('policy_script')
