

import networkx as nx

def shortest_path(G,strat_point,end_point):
    paths = nx.all_shortest_paths(G,source=strat_point,target=end_point)
    all_paths =[]
    for p in paths:
        all_paths.append(p)

    return all_paths

def shortest_path_plus(G,start,end,plus=1):
    path_gen = shortest_path(G,start,end)
    res = []
    for p in path_gen:
        res.append(add_detour_to_path(G,p,detour_len=plus+1))
    return res

def add_detour_to_path(G,path_p,detour_len):
    all_paths_gen=[]
    for j in range(len(path_p)):
        if j+1==len(path_p):
            break
        start_p = path_p[j]
        end_p = path_p[j+1]
        res = nx.all_simple_paths(G,start_p,end_p,detour_len)
        for x in res:
            combain_p = path_p[:j] + x + path_p[j+2:]
            all_paths_gen.append(combain_p)
    return all_paths_gen

def add_diagonal_edges(graph_g,x,y):
    list_node = graph_g.nodes()
    for node_i in list_node:
        x_i = node_i[0]
        y_i = node_i[1]
        if x_i + 1 < x and y_i + 1 < y:
            graph_g.add_edge((x_i, y_i), (x_i+1, y_i+1))

        if x_i-1 >= 0 and y_i - 1>=0:
            graph_g.add_edge((x_i, y_i), (x_i -1, y_i -1))

        if x_i + 1 < x and y_i - 1>=0:
            graph_g.add_edge((x_i, y_i), (x_i + 1, y_i -1))

        if x_i-1 >= 0 and y_i + 1 < y:
            graph_g.add_edge((x_i, y_i), (x_i -1, y_i + 1))

def grid_to_graph(gird,is_diagonal=True):
    x=gird.x_size
    y=gird.y_size
    G = nx.grid_2d_graph(x,y)
    if is_diagonal:
        add_diagonal_edges(G,x,y)
    return G



def get_short_path_from_grid(grid,s,e):
    G = grid_to_graph(grid)
    res = shortest_path(G,s,e)
    return res


if __name__ == "__main__":

    print('policy_script')

