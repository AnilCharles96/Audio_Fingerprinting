import argparse
import sys
from Database import Database
from fingerprint import Fingerprint
from recognize import Recognize
import os
import time
import progressbar




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Audio fingerprinting\n',formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-db','--database',help='connect to mysql database by entering hostname,username and passwd  \neg: localhost,username,password\n\n')
    parser.add_argument('-f','--fingerprint',help='Enter the directory which contains songs\nconvert each songs to corresponding hashes and store in database\n\n')
    parser.add_argument('-r','--recognize',help='record the soundtrack, will return if it find any match\n\n',action='store_true')
    

    args, unknown = parser.parse_known_args()
    if unknown:
        print('\nunknown argument please try the following arguments\n\n')
        parser.print_help()
    if len(sys.argv[1:])==0:
        parser.print_help()
        
    
    if args.database:
        
        config = args.database
        config = config.split(',')
        hostname = config[0]
        user = config[1]
        passwd = config[2]           
        dbobject = Database(hostname=hostname,user=user,passwd=passwd)
        
        if args.fingerprint:
            
            
            if args.recognize:
                print('either do fingerprinting or recognizing')
                sys.exit(0)
             
            dbobject.drop_hash_table()
            dbobject.drop_song_table()            
            dbobject.create_tables()
            
        #print(args.fingerprint)
            fobject = Fingerprint(args.fingerprint)
            a = fobject.fo
            a = list(a)
            #print(a)
            count = 0
            for name,index in a[0].items():
                count += 1
                #print(name,index)
                try:
                    dbobject.insert_values_into_song_table(index,os.path.splitext(name)[0])
                except:
                    
                    sys.exit(0)
                    
                
            
            store_hash = []   
            for i in range(count):
                store_hash.append(fobject.ungenerate(fobject.produce_hashes(a[1][i])))
            
            store_hash_length = 0
            for i in range(count):
                store_hash_length += len(store_hash[i])
            
            bar = progressbar.ProgressBar(max_value=store_hash_length)
            print('\storing fingerprints in database')
            iterate = 0
            for i in range(count):
                for j in range(len(store_hash[i])):                        
                    dbobject.insert_values_into_hash_table(i+1,store_hash[i][j])
                    iterate += 1
                    time.sleep(0.1)                   
                    bar.update(iterate)    
            print('\nfinished storing')
            
           # print(store_hash)
            
        elif args.recognize:
            robject = Recognize()
            robject.identify(dbobject)
        
        else:
            print('\nplease perform fingerprinting once, if you have already done it then perform recognize to identify songs\n')
        
    else:
        print('\nenter the database login credentials\n')
    
            
       


     
    














