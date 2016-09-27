class Point:
    def __init__(self, x, y):
        self.x = x # coord x
        self.y = y # coord y

    def show(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __eq__(self,other):
    	if isinstance(other,Point):
    		return self.x == other.x and self.y == other.y
    	if isinstance(other,tuple):
    		return self.x == other[0] and self.y == other[1]
    	return NotImplemented
    def __key(self):
    	return (self.x,self.y)
    def __hash__(self):
    	return hash(self.__key())
