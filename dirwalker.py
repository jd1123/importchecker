import os
import sys

def get_import_dict(path=None, walk=False):
    if path==None:
        path = os.getcwd()
        
    files = [fn for fn in os.listdir(path) if os.path.isfile(os.path.join(path, fn))]
    dirs = [os.path.join(path, d) for d in os.listdir(path) if os.path.isdir(os.path.join(path,d))]
    #print path + ": " + str(dirs)
    i_dict = {}
    for f in files:
        with open(os.path.join(path,f)) as fname:
            lines = fname.readlines()
            for l in lines:
                if l.startswith("import") or l.startswith("from"):
                    try:
                        i_dict[os.path.join(path, f)].append(l)
                    except (KeyError):
                        i_dict[os.path.join(path,f)] = []
                        i_dict[os.path.join(path,f)].append(l)
    if walk:
        if dirs == []:
            return (i_dict, None)
        else:
            new_dirs = []
            for d in dirs:
                p = os.path.join(path,d)
                (x,y) = get_import_dict(p, True)
                i_dict.update(x)
                new_dirs.append(y)
            dirs+=new_dirs
    
    return (i_dict, dirs)

def main():
    (x,y) = get_import_dict(walk= True)
    for k,v in x.iteritems():
        print k + " : " + str(v)
        
    #for i in y:
    #    print i
    
if __name__=='__main__':
    status = main()
    sys.exit(status)