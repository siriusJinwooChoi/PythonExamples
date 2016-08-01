import shelve
from person import User
from manager import Manager

bob = User('Bob Smith', 42, 30000, 'software')
sue = User('Sue Jones', 45, 40000, 'hardware')
tom = Manager('Tom Doe',  50, 50000)

db = shelve.open('Chatting-shelve')
db['bob'] = bob
db['sue'] = sue
db['tom'] = tom
db.close()
