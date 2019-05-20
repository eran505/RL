import copy
class Markov_State:

    def __init__(self):
        self.player_position = {}
        self.player_angle = {}
        self.player_budget={}


    def get_pos_by_name(self,name):
        return self.player_position[name]

    def get_all_players_pos(self,suffix=None):
        if suffix is None:
            return self.player_position
        suffix_players_name = {k:v for (k,v) in self.player_position.items() if str(k).split('_')[1] == suffix}
        return suffix_players_name
    def update_budget(self,float_budget,name):
        self.player_budget[name]-=float_budget

    def get_angle_by_name(self,name):
        return self.player_angle[name]

    def set_budget_by_name(self,name,budget):
        self.player_budget[name]=budget

    def set_player(self,name,pos,angle):
        self.player_position[name]=pos
        #self.player_budget[name]=budget
        self.player_angle[name]=angle

    def __str__(self):
        to_string=''
        for name_i in self.player_position.keys():
            to_string+='{}:P_{}_D_{}  '.format(name_i,self.player_position[name_i],
                                    self.player_angle[name_i])
        return to_string


def get_deep_copy_state(class_instance):
    data = copy.deepcopy(class_instance)  # if deepcopy is necessary
    return (data)


if __name__ == "__main__":
    state_num_two = Markov_State()
    state_num_two.set_player('p1',[1,2],30)
    state_num_two.set_player('p2', [10, 12], 60)
    new_state = (Markov_State.get_deep_copy_state(state_num_two))
    new_state.my_budget=40
    print (new_state)
    print ('----')
    print (state_num_two)
    print('markov state class')

