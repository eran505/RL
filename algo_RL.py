import numpy as np
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
        self.eligibility_table={}
        self.gama_learning=0
        self.lamda=0
        self.discount_factor=0.7
        self.epslion=0.01
        self.step_size = 0.01
        self.matrix_q = None

    def e_greedy_policy(self):
        self.q_table


    def init_q_matrix(self,action_size,state_size):
        self.matrix_q = np.zeros((state_size,action_size))

if __name__ == "__main__":
    rl = SarsaLamda()
    rl.init_q_matrix(3,10)
    print (rl.matrix_q)
    print('policy_script')
