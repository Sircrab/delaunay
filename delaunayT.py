import random
from collections import deque
from operator import attrgetter
from point import Point
from triangle import Triangle
from triangulation import Triangulation

class DelaunayT(Triangulation):

    ' LIST[POINT] -> VOID '
    ' Initialize the Delaunay triangulation '
    def __init__(self, points):
        # set the initial triangle
        addTriangle(self.triangles[0])
        # compute a random permutation of points
        random.shuffle(points)

        # insert points into the triangulation
        for p in points:
            self.insertPoint(p)

    ' LIST[POINT] -> TRIANGLE '
    ' Return a triangle that contain a set of points '
    def auxTriangle(self, points):
        # get the boundary of the set
        eps = 20
        minX = min(points, key=attrgetter('x')).x
        minY = min(points, key=attrgetter('y')).y
        maxX = max(points, key=attrgetter('x')).x
        maxY = max(points, key=attrgetter('y')).y

        # calculate the points of the triangle
        p1 = Point(minX - eps,
                   minY - eps)
        p2 = Point(maxX + maxY - minY + eps,
                   minY - eps)
        p3 = Point(minX - eps,
                   maxY + maxX - minX + eps)

        # set the triangle
        vertexs = [p1, p2, p3]
        
        return Triangle(vertexs)

    ' POINT -> TRIANGLE '
    ' Find the triangle that contain a point in a triangulation'
    def findTriangle(self, point, eps):

        curTriangle = random.choice(self.triangles)
        while(curTriangle != triangle_containing_point(curTriangle,point,eps) and curTriangle != None):
            curTriangle = triangle_containing_point(curTriangle,point,eps)
        if(curTriangle == None):
            raise NameError("Point lies outside any triangle")
        return curTriangle


    ' POINT -> VOID'
    ' Adds a point to the triangulation'
    def insertPoint(self, point):
        eps = 0.00001
        if self.triangles:
            t = findTriangle(point,eps)
            auxEdge = t.onEdge(point,eps)
            #point on edge!
            q = deque()
            if(auxEdge != None):
                eraseTriangle(t)
                reverseEdge = auxEdge.getReverseEdge()
                t = getNeighbour(auxEdge)
                t2 = getNeighbour(reverseEdge)
                op1 = t.opposingVertex(reverseEdge)
                op2 = t2.opposingVertex(auxEdge)
                toAdd = addTriangle(Triangle([reverseEdge.first,point,op1]))
                q.append(toAdd)
                toAdd = addTriangle(Triangle(point,reverseEdge.second,op1))
                q.append(toAdd)
                toAdd = addTriangle(Triangle(op2,auxEdge.first,point))
                q.append(toAdd)
                toAdd = addTriangle(Triangle(point,auxEdge.second,op2))
                q.append(toAdd)
            else:
                #3 new triangle
                toAdd = addTriangle(Triangle([t.p1,point,t.p2]))
                q.append(toAdd)
                toAdd = addTriangle(Triangle([t.p2,point,t.p3]))
                q.append(toAdd)
                toAdd = addTriangle(Triangle([t.p3,point,t.p1]))
                q.append(toAdd)
                eraseTriangle(t)
            #Triangles added, now to check delaunay
            visitedSet = set()
            while q:
                curTri = q.popLeft()
                if curTri.circleTest(curTri.opposingVertex(curTri.e1),eps) > 0:
                    pass
                elif curTri.circleTest(curTri.opposingVertex(curTri.e2),eps) > 0:
                    pass
                elif curTri.circleTest(curTri.opposingVertex(curTri.e3),eps) > 0:
                    pass
                visitedSet.add(curTri)




            
            




        else:
            raise NameError("need at least one triangle")
