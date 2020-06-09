import os, glob, time
#from .Auto_Run_Monolith import Auto_Run_Monolith


def findcachedmodtimefile ( file_path ):  #bug, doesnt work when only 1 file is in there
    #find = operator.lt
    files = glob.glob ( file_path )
    #print ( len ( files ) )
    #files = [ 7, 2, 3, 4, 5 ]
    #if not files:
        #return None
    #newest = files [ 0 ], os.path.getctime ( files [ 0 ] )
    #newest = files [ 0 ], files [ 0 ]
    #i = 0
    #for i in range ( len ( files ) ):
        #age = os.path.getctime ( i )
        #age = i
        #print ( age )
        #if age < newest [ 1 ] :
            #newest = files [ i ], age
    #print ( newest )
    youngest = sorted ( files, key = os.path.getctime)
    #print ( youngest [ -1 ] )
    return os.path.getctime ( youngest [ -1 ] )

class runape ( object ):
    
    def __init__ ( self, file_path ):
        #self.cachedmodtime = os.path.getmtime ( '/home/nicholasarn/Print_With_APE' )
        self.cachedmodtime = findcachedmodtimefile ( file_path )
        #self.cachedmodtime = findfile ( 'time' )
        self.filepath = file_path
        self.running = True
    
    def findfile ( self, fileortime ):  #bug, doesnt work when only 1 file is in there
        #find = operator.lt
        files = glob.glob ( self.filepath )
        #files = [ 7, 2, 3, 4, 5 ]
        #if not files:
            #return None
        #newest = files [ 0 ], os.path.getctime ( files [ 0 ] )
        #newest = files [ 0 ], files [ 0 ]
        #i = 0
        #for i in range ( len ( files ) ):
            #age = os.path.getctime ( i )
            #age = i
            #if find ( age, newest [ 1 ] ):
                #newest = i, age
        youngest = sorted ( files, key = os.path.getctime)
        if fileortime == 'file':
            return youngest [ -1 ]
        if fileortime == 'time':
            return os.path.getctime ( youngest [ -1 ] )
    def runinback ( self ):
        while self.running:
            try:
                time.sleep ( 1 )
                if self.watchfolder ( ) == 'execute':
                    print ( 'execute stage 2' )
                    return ( 'execute' )
                
            except FileNotFoundError:
                print ( ' file not found ' )
            except None:
                None
            except:
                print ( ' unknown error ' )
    
    #print ( findfile ( ) )
    
    def watchfolder ( self ):
        modtime = self.findfile ( 'time' )
        #print ( modtime )
        #if modtime != self.cachedmodtime:
        if modtime != self.cachedmodtime:
            self.cachedmodtime = modtime
            #Auto_Run_Monolith ( )
            #exec ( open ( '/home/nicholasarn/Downloads/work/APE_master/Auto_Run_Monolith.py' ).read ( ) )
            print ( 'execute stage 1' )
            return ( 'execute' )
            
#ra = runape ( "/home/nicholasarn/Print_With_APE/*.gcode" )
#ra.runinback ( )
#print ( ra.runinback ( ) )

#print ( glob.glob ( "/home/nicholasarn/Print_With_APE/*.gcode" ) )
#print ( findcachedmodtimefile ( "/home/nicholasarn/Print_With_APE/*.gcode" ) )
#exec ( open ( '/home/nicholasarn/Downloads/work/APE_master/Auto_Run_Monolith.py' ).read ( ) )
#execfile ( '/home/nicholasarn/Downloads/work/APE_master/Auto_Run_Monolith.py' )
#subprocess.call ( '/home/nicholasarn/Downloads/work/APE_master/Auto_Run_Monolith.py', shell = True )
#with open ( '/home/nicholasarn/Downloads/work/APE_master/Auto_Run_Monolith.py' ) as pycode:
    #comp = compile ( pycode.read ( ), '/home/nicholasarn/Downloads/work/APE_master/Auto_Run_Monolith.py', 'exec' )
    #exec ( comp, globals ( ) )
#os.system ( '/home/nicholasarn/Downloads/work/APE_master/Auto_Run_Monolith.py' )
#subprocess.Popen ( '/home/nicholasarn/Downloads/work/APE_master/Auto_Run_Monolith.py', stdout=subprocess.PIPE, shell=True )
#Auto_Run_Monolith ( )












