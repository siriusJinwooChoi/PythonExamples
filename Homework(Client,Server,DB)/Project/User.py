class User:
    def __init__(self, ID, Password):
        self.ID = ID
        self.Password = Password
    def lastID(self):
        return self.ID.split()[-1]

if __name__ == '__main__':
    bob = User('Bob Smith', 42)
    sue = User('Sue Jones', 45)
    print(bob.ID)

    print(bob.lastID())
