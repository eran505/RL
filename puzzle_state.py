


class Puzzle_State:

    def __init__(self,type_name,x,y):
        self.state_type = type_name
        self.x=x
        self.y=y
        self.palyer=[]

    def clean_player(self,player_p):
        self.palyer.remove(player_p)

    def add_player(self,player_p):
        self.palyer.append(player_p)

    def set_goal(self):
        self.state_type = 'G'

    def set_start_bad(self):
        self.state_type='S'

    def set_start_good(self):
        self.state_type = 'A'

    def set_wall(self):
        self.state_type='W'

    def __str__(self):
        if len(self.palyer)>0:
            str_p=''
            for p in self.palyer:
                str_p+=p.name[1]+','
            return "{}{}".format(self.state_type,str_p[:-1])
        return "{} ".format(self.state_type)

        #if len(self.palyer)>0:
        #    return self.state_type
        #else:
        #    return self.palyer


if __name__ == "__main__":
    print('puzzle_sate class')