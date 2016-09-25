from point import Point
from edge import Edge
from operator import itemgetter,attrgetter, methodcaller

class Triangle:
    def __init__(self, points):
        'TODO: Ensure that the points are passed in CCW order, to do this'
        'sort the points based on x coordinate, if equal then by y coordinate'
        points = ccwSort(points)

        # pointer to each point
        self.p1 = points[0]
        self.p2 = points[1]
        self.p3 = points[2]

        #Generate edges for each triangle
        self.e1 = Edge(self.p1,self.p2)
        self.e2 = Edge(self.p2,self.p3)
        self.e3 = Edge(self.p3,self.p1)

    def show(self):
        return "(" + self.p1.show() + ", " + self.p2.show() + ", " + self.p3.show() + ")" 


    def onEdge(self,point,eps):
        firstEdgeTest = self.e1.orientation_test(point,eps)
        secondEdgeTest = self.e2.orientation_test(point,eps)
        thirdEdgeTest = self.e3.orientation_test(point,eps)
        if firstEdgeTest == 0:
            return self.e1
        if secondEdgeTest == 0:
            return self.e2
        if thirdEdgeTest == 0:
            return self.e3
        return None

    def opposingVertex(self, edge):
        if (edge == self.e1):
            return self.p3
        if (edge == self.e2):
            return self.p1
        if (edge == self.e3):
            return self.p2
        return None

    def ccwSort(self,points):
        center = Point((points[0].x + points[1].x + points[2].x)/3,(points[0].y + points[1].y + points[2].y)/3)
        sortedPoints = []
        for i in range(0,3):
            ang = atan2(points[i].y - center.y,points[i].x - center.x)
            sortedPoints.append((ang,points[0]))
        sortedPoints.sort()
        return [sortedPoints[0][1],sortedPoints[1][1],sortedPoints[2][1]]


