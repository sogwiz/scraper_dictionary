import getopt
import sys

class Configurator:
    def __init__(self,args):
        self.db_conn_string = ''
        self.unixOptions = "d:h"
        self.gnuOptions = gnuOptions = ["db_conn_string=","help"]
        self.processArgs(args,self.unixOptions,self.gnuOptions)

    def printUsage(self):
        print("Usage: --db_conn_string=<mongodb://user:passwd@db-host.com:5414/assyrian?ssl=true>")

    
    def processArgs(self,args,unixOptions,gnuOptions):
        try:
            opts, arguments = getopt.getopt(args, unixOptions, gnuOptions)
        except getopt.GetoptError:
            print("ERROR")
            self.printUsage()
            sys.exit(2)

        #mainly to check and enforce required args
        foundDBArg = False

        for opt, arg in opts:
            if opt in ("-d", "--db_conn_string"):
                self.db_conn_string = arg
                foundDBArg = True
            elif opt in ("-h", "--help"):
                self.printUsage()
                sys.exit(2)
        
        if not foundDBArg:
            self.printUsage()
            sys.exit(2)

