
import os,re

def walk_rec(root, list_res, rec="", file_t=True, lv=-800, full=True):
    if root[-1]=='/':
        root=root[:-1]
    size = 0
    ctr = 0
    class_list = list_res
    if lv == 0:
        return list_res
    lv += 1
    for path, subdirs, files in os.walk(root):
        ctr += 1
        if file_t:
            for name in files:
                tmp = re.compile(rec).search(name)
                if tmp == None:
                    continue
                size += 1
                if full:
                    class_list.append(os.path.join(path, name))
                else:
                    class_list.append(str(name))
        else:
            for name in subdirs:
                tmp = re.compile(rec).search(name)
                if tmp == None:
                    continue
                size += 1
                if full:
                    class_list.append(os.path.join(path, name))
                else:
                    class_list.append(str(name))
        for d_dir in subdirs:
            walk_rec("{}/{}".format(path, d_dir), class_list, rec, file_t, lv, full)
        break
    return class_list

def mkdir_system(path_root, name, is_del=True):
    if path_root is None:
        raise Exception("[Error] passing a None path --> {}".format(path_root))
    if path_root[-1] != '/':
        path_root = path_root + '/'
    if os.path.isdir("{}{}".format(path_root, name)):
        if is_del:
            os.system('rm -r {}{}'.format(path_root, name))
        else:
            #print "{}{} is already exist".format(path_root, name)
            return '{}{}'.format(path_root, name)
    print( '[OS] mkdir {}{}'.format(path_root, name))
    os.system('mkdir {}{}'.format(path_root, name))
    return '{}{}'.format(path_root, name)




if __name__ == "__main__":
    import pandas as pd
    from util import walk_rec
    path_dir = '/home/ise/games/catch'
    res_budget_folder = walk_rec(path_dir,[],'budget',False,lv=-1)
    for item in res_budget_folder:
        res_csv = walk_rec(item,[],'.csv')
        all_df_list = []
        for item_csv in res_csv:
            n = str(item_csv )[:-4].split('N_')[1]
            df_i = pd.read_csv(item_csv)
            df_i['size_N']=n
            all_df_list.append(df_i)
        df_all = pd.concat(all_df_list)
        df_all.to_csv('{}/all.csv'.format(item))
    exit()
