import os
import sys

def get_import_dict(path=None, walk=False):
    if path==None:
        path = os.getcwd()
        
    files = [fn for fn in os.listdir(path) if os.path.isfile(os.path.join(path, fn))]
    dirs = [os.path.join(path, d) for d in os.listdir(path) if os.path.isdir(os.path.join(path,d))]
    
    
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
            p = []
            p.append(path)
            return (i_dict, p)
        else:
            new_dirs = []
            for d in dirs:
                p = os.path.join(path,d)
                (x,y) = get_import_dict(p, True)
                i_dict.update(x)
                new_dirs+=y
                
            dirs+=new_dirs
     
    dirs = list(set(dirs))       
    return (i_dict, dirs)

def output_results(import_tuple):
    for k,v in import_tuple[0].iteritems():
            print k + " : "
            for i in v:
                print "\t"+str(i).rstrip()
            print   
    
    if len(import_tuple[0]):    
        print str(len(import_tuple[0].keys())) + " files found | " + str(len(import_tuple[1])) + " directories scanned"
    else:
        print " 0 files found | " + str(len(import_tuple[1])) + " directories scanned"
        
            
    

def main():
    path = None
    if len(sys.argv)==2:
        path = sys.argv[1]
        (x,y) = get_import_dict(path, walk= True)
        output_results((x,y))
        
    elif len(sys.argv) > 2:
        print "too many command line arguments"
    
    else:
        path = None
        (x,y) = get_import_dict(path, walk= True)
        output_results((x,y))
            
        
if __name__=='__main__':
    status = main()
    sys.exit(status)