import os
import sys
import re

def get_import_dict(path=None, walk=False):
    if path==None:
        path = os.getcwd()
        
    files = [fn for fn in os.listdir(path) if os.path.isfile(os.path.join(path, fn))]
    dirs = [os.path.join(path, d) for d in os.listdir(path) if os.path.isdir(os.path.join(path,d))]
    
    
    i_dict = {}
    for f in files:
        if f.split('.')[-1] == "py":
            
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

def output_results(import_tuple, verbose = False, full_import = False):
    if verbose:
        for k,v in import_tuple[0].iteritems():
                print k + " : "
                for i in v:
                    print "\t"+str(i).rstrip()
                print
    
    if len(import_tuple[0]):    
        print str(len(import_tuple[0].keys())) + " files found | " + str(len(import_tuple[1])) + " directories scanned"
    else:
        print " 0 files found | " + str(len(import_tuple[1])) + " directories scanned"
    
    depends = set()    
    for v in import_tuple[0].values():
        for i in v:
            depends.add(i.split()[1])
    
    new_depends = depends.copy()
    for d in depends:
        d_s = d.split('.')
        if len(d_s) > 1:
            new_depends.remove(d)
            new_depends.add(d_s[0])
            
    if not full_import:
        depends = new_depends.copy()
        return depends
    
    else:
        if depends:    
            print "\nYour project depends on: "
            for i in sorted(depends):
                print i

            
def get_requirements(path_to_filename):
    with open(path_to_filename) as f:
        for l in f.readlines():
            yield re.split('==|>=|<=' , l)[0]


def run_imports(args):
    path = None
    verbose = False
    if len(args)==2:
        path = args[1]
        (x,y) = get_import_dict(path, walk= True)
        if '-v' in args:
            verbose=True
        
        output_results((x,y), verbose)
        
    elif len(args) > 2:
        print "too many command line arguments"
    
    else:
        path = None
        (x,y) = get_import_dict(path, walk= True)
        output_results((x,y))

def main():
    depends = run_imports(sys.argv)
    for l in get_requirements('/home/jw/Documents/dev/python/openspending/requirements.txt'):
        if l in depends:
            print str(l) + " is used in your project"
        else:
            print str(l) + " is not used in your project"    
        
if __name__=='__main__':
    status = main()
    sys.exit(status)