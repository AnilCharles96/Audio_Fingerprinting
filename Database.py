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
        self.drop_hash_table()
        self.drop_song_table()
        self.create_tables()
        

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
        
        try:          
            self.mycursor.execute('INSERT INTO %s values(%s,\'%s\')' %(self.song_table,index,filename))
            self.mydb.commit()            
        except:
            print('error inserting values in song_table')
        
    def insert_values_into_hash_table(self,index,hashes):
       
        try:           
            self.mycursor.execute('INSERT INTO %s values(%d,\'%s\')' %(self.hash_table,index,hashes))
            self.mydb.commit()            
        except:            
            print('error inserting values in hash_table')
            
    def drop_song_table(self):
        self.mycursor.execute('DROP TABLE IF EXISTS %s' %(self.song_table))
    
    def drop_hash_table(self):
        self.mycursor.execute('DROP TABLE IF EXISTS %s' %(self.hash_table))
    
