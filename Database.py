import mysql.connector as conn
import sys
#from fingerprint import Fingerprint

class Database():
    
    def __init__(self,hostname,user,passwd):
        
        
        self.hostname = hostname
        self.user = user
        self.passwd = passwd
        self.mydb = ' '
        self.mycursor = ' '
        self.database = 'fingerprint_database'
        self.song_table = 'song_table'
        self.hash_table = 'hash_table'
        self.connection()
        self.create_database_if_not_exist()     
        #self.drop_hash_table()
        #self.drop_song_table()           
        #self.create_tables()
        

    def connection(self):
        try:
            self.mydb = conn.connect(host=self.hostname,user=self.user,passwd=self.passwd)
            print('\nconnection established')
        except:
            print('\ncant connect to database, Entered details might be wrong or the server is not running \n')
            sys.exit(0)

    def create_database_if_not_exist(self):        
        
        try:
            self.mycursor = self.mydb.cursor()
            self.mycursor.execute('CREATE DATABASE IF NOT EXISTS %s' %(self.database))
            self.mydb = conn.connect(host='localhost',user='root',passwd='helloworld',database=self.database)
            self.mycursor = self.mydb.cursor()
            #self.mycursor.execute('SHOW DATABASES LIKE \'%s\'' %(self.database))
            print('\n%s created\n' %(self.database))
            self.mycursor.execute('USE %s' %(self.database))
        except:
            print('error creating database\n')
        
            
            
    def create_tables(self):
        #mycursor = self.mydb.cursor(buffered=True)
        try:
            
            self.mycursor.execute('CREATE TABLE IF NOT EXISTS %s\
                              (song_id int AUTO_INCREMENT not null,\
                              song_name varchar(200),\
                              primary key(song_id))' %(self.song_table))
        

            self.mycursor.execute('CREATE TABLE IF NOT EXISTS %s \
                              (song_id int AUTO_INCREMENT not null,\
                              hash varchar(100),\
                              foreign key (song_id) references song_table(song_id))' %(self.hash_table))
            print('song_table and hash_table created')
        except:
           print('Error creating tables\n')
                
    def insert_values_into_song_table(self,index,filename): 
        #print('INSERT INTO %s values(%s,\'%s\')' %(self.song_table,index,filename))
        try:          
            self.mycursor.execute('INSERT INTO %s values(%s,\'%s\')' %(self.song_table,index,filename))
            self.mydb.commit()            
        except:
            pass
            #print('error inserting values in song_table')
            #sys.exit(0)
        
    def insert_values_into_hash_table(self,index,hashes):
       
        #print('INSERT INTO %s values(%d,\'%s\')' %(self.hash_table,index,hashes))
        try:           
            self.mycursor.execute('INSERT INTO %s values(%d,\'%s\')' %(self.hash_table,index,hashes))
            self.mydb.commit()            
        except: 
            pass
            #print('error inserting values in hash_table')
            #sys.exit(0)
            
    def drop_song_table(self):
        self.mycursor.execute('DROP TABLE IF EXISTS %s' %(self.song_table))
    
    def drop_hash_table(self):
        self.mycursor.execute('DROP TABLE IF EXISTS %s' %(self.hash_table))
        
    def select_song_table(self,id):
        #print('SELECT song_name FROM %s WHERE song_id = %s'%(self.song_table,id))
        self.mycursor.execute('SELECT song_name FROM %s WHERE song_id = %s'%(self.song_table,id))
        return self.mycursor
    
    def select_hash_table(self,hash):
        
        self.mycursor.execute('SELECT song_id FROM %s WHERE hash=\'%s\'' %(self.hash_table,hash))
        return self.mycursor
    
r'''    
'INSERT INTO song_table values(%s,\"%s\")' %(index,filename)  
from fingerprint import Fingerprint   
dbobject = Database(hostname='localhost',user='root',passwd='helloworld')
dbobject.drop_hash_table()
dbobject.drop_song_table()
dbobject.create_tables()
index = 2
name = 'linkin park'
dbobject.insert_values_into_song_table(1,'1-01 Survival')
dbobject.insert_values_into_hash_table(1,'t6575756765')

dbobject.select_song_table()
from collections import Counter
showcount = Counter()
dbobject = Database(hostname='localhost',user='root',passwd='helloworld')        
s = dbobject.select_hash_table('0008CA42AD9A599D3DD7')
for item in s:
        showcount.update(item)

fobject = Fingerprint('C:\\Users\\Anil\\Desktop\\tick')
a = fobject.fo
a = list(a)
#print(a)
count = 0
for name,index in a[0].items():
    count += 1
    dbobject.insert_values_into_song_table(2,"hans zimmer")
    dbobject.insert_values_into_song_table
    #print(name,index)
            
    store_hash = []   
    for i in range(count):
        store_hash.append(fobject.ungenerate(fobject.produce_hashes(a[1][i])))
            
    for i in range(count):
        dbobject.insert_values_into_hash_table(i,store_hash[i])




object.connection()
object.create_database_if_not_exist()
object.create_songs_table()


string = 'fingerprint_database'

mydb = conn.connect(host='localhost',user='root',passwd='helloworld')
mycursor = mydb.cursor(buffered=True)
mycursor.execute('CREATE DATABASE IF NOT EXISTS %s' %(string))
mydb = conn.connect(host='localhost',user='root',passwd='helloworld',database='fingerprint_database')
mycursor = mydb.cursor(buffered=True)
mycursor.execute('SHOW DATABASES LIKE \'%s\'' %(string))
mycursor.execute('USE %s' %(string))
mycursor.execute('SHOW TABLES')
for i in mycursor:
    for j in i:      
        print(j)
mycursor.execute('USE audio')
mycursor.execute('SHOW TABLES')
mycursor.execute('drop table songs_table,hash_table')

    
mycursor.execute('CREATE TABLE IF NOT EXISTS %s\
                              (song_id int AUTO_INCREMENT not null,\
                              song_name VARCHAR(200),\
                              primary key(song_id))' %('songs_table'))    


mycursor.execute('CREATE TABLE IF NOT EXISTS %s \
                              (song_id INT,\
                              hash varchar(100),\
                              foreign key (song_id) references songs_table(song_id))' %('hash_table'))


    
index = 2
filename = 'drop dead' 
mycursor.execute('INSERT INTO song_table values(%s,\'%s\')' %(index,filename))
mycursor.execute('select * from song_table')
for i in mycursor:
    print(i)
mydb.commit()

'''