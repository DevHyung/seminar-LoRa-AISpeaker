import math
class Shape:
    def __init__(self,shpid,shptype,color):
        self.id = shpid
        self.color = color
        self.type = shptype

    def __str__(self):
        rep = "Shape ID: {}\tType: {}\tColor: {}\n".format(self.id,self.type,self.color)
        return rep

class Line(Shape):
    def __init__(self,shpid,shptype,color,x1,y1,x2,y2):
        super().__init__(shpid,shptype,color)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def getLength(self):
        return math.sqrt((self.x2-self.x1)**2+(self.y2-self.y1)**2)

class Polygon(Shape):
    def __init__(self,shpid,shptype,color,width,height=0):
        super().__init__(shpid,shptype,color)
        self.width = width
        self.height = height

class Circle(Polygon):
    def getArea(self):
        return math.pi*self.width*self.width

class Rectangle(Polygon):
    def getArea(self):
        return self.width*self.height

class Triangle(Polygon):
    def getArea(self):
        return 0.5*self.width*self.height
    
