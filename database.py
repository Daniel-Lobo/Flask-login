from sqlite3 import connect
from secrets import token_hex

class Database():
    def __init__(self):
        self.__log: str = '' 
        self.__db       = connect('users.db').cursor()
        if not self.IsTable('users'):
            self.__log += 'User table does not exist on users.db database, creating table'
            self.__db.execute("CREATE TABLE users(email, secret, password, UNIQUE(email))")
            self.__db.connection.commit()
            if not self.IsTable('users'):
                self.__log += 'FATAL ERROR: user table could not be created on database'
            else: self.__log += 'user table created'         

        self.__log += 'Database intialized'
        return        

    def IsTable(self, table:str)->bool:
        tables  = self.__db.execute('SELECT name FROM sqlite_master').fetchall()        
        if len(tables) == 0: return False 
        for tb in tables:
            if table in tb: return True
        return False    

    def IsUser(self, user):
        users = self.__db.execute('SELECT * FROM users WHERE email=?', (user,)).fetchall()           
        if len(users) == 0: return False        
        return user in users[0]
    
    def AddUser(self, email, password):
        secret = token_hex(3)       
        data   = (email, secret, password) 
        self.__db.execute("INSERT INTO users (email, secret, password) VALUES(?, ?, ?);", data)
        self.__db.connection.commit() 
        return None
    
    def GetUser(self, user):
        users = self.__db.execute('SELECT * FROM users WHERE email=?', (user,)).fetchall()           
        if len(users) == 0: return None      
        user  = users[0]   
        print(user)
        return {'email' : user[0], 'secret': user[1], 'password' : user[2]}   

    def UpdateSecret(self, user):
        if not self.IsUser(user): return 'Not an user'
        secret = token_hex(3) 
        print(user)
        self.__db.execute(f'UPDATE users SET secret="{secret}" WHERE email="{user}"')
        self.__db.connection.commit()         
        return self.GetUser(user)
    
    def UpdatepassWord(self, user, password):
        if not self.IsUser(user): return 'Not an user'         
        self.__db.execute(f'UPDATE users SET password="{password}" WHERE email="{user}"')
        self.__db.connection.commit()         
        return self.GetUser(user)