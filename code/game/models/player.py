from models.property import Property

class Player:
    
    def __init__(self,name):
        self.name = name
        self.money = 1500
        self.location = 0
        self.properties = []
        
    def move(self,num_spaces):
        self.location+=num_spaces
        if self.location >=40:
            self.location -=40
            self.money+=200
        #return self.location
    
    def buy_property(self,property:Property):
        self.properties.append(property)
        
    def remove_property(self,property:Property):
        self.properties.remove(property)
        
    def pay(self,amount:int,receiver:Player):
        self.money-=amount
        receiver.money+=amount
    
    
    