import random
from collections import deque
from operator import attrgetter
from point import Point
from triangle import Triangle
from triangulation import Triangulation

class DelaunayT(Triangulation):


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

    ' LIST[POINT] -> VOID '
    ' Initialize the Delaunay triangulation '
    def __init__(self, points):
        # set the initial triangle
        super(DelaunayT,self).__init__()
        self.addTriangle(self.auxTriangle(points))
        self.origTriangle = self.triangles[0]
        print(self.origTriangle.show())
        # compute a random permutation of points
        random.shuffle(points)

        # insert points into the triangulation
        for p in points:
            self.insertPoint(p)
            #self.draw(True)
        self.draw(False)

    ' POINT -> TRIANGLE '
    ' Find the triangle that contain a point in a triangulation'
    def findTriangle(self, point, eps):

        curTriangle = random.choice(self.triangles)
        while(curTriangle != None and curTriangle != self.triangle_containing_point(curTriangle,point,eps)):
            curTriangle = self.triangle_containing_point(curTriangle,point,eps)
        if(curTriangle == None):
            raise NameError("Point lies outside any triangle")
        return curTriangle


    ' POINT -> VOID'
    ' Adds a point to the triangulation'
    def insertPoint(self, point):
        eps = 0.00001
        #print("Inserting now point: " + point.show())
        if self.triangles:
            t = self.findTriangle(point,eps)
            auxEdge = t.onEdge(point,eps)
            #point on edge!
            q = deque()
            if(auxEdge != None):
                #print("Point on edge")
                reverseEdge = auxEdge.getReverseEdge()
                t = self.getNeighbour(auxEdge)
                t2 = self.getNeighbour(reverseEdge)
                self.eraseTriangle(t)
                self.eraseTriangle(t2)
                if t != None:
                    op1 = t.opposingVertex(reverseEdge)
                if t2 != None:
                    op2 = t2.opposingVertex(auxEdge)
                if t != None:
                    toAdd = self.addTriangle(Triangle([reverseEdge.first,point,op1]))
                    #print("Adding triangle: " + toAdd.show())
                    q.append(toAdd)
                    toAdd = self.addTriangle(Triangle([point,reverseEdge.second,op1]))
                    #print("Adding triangle: " + toAdd.show())
                    q.append(toAdd)
                if t2 != None:
                    toAdd = self.addTriangle(Triangle([op2,auxEdge.first,point]))
                    #print("Adding triangle: " + toAdd.show())
                    q.append(toAdd)
                    toAdd = self.addTriangle(Triangle([point,auxEdge.second,op2]))
                    #print("Adding triangle: " + toAdd.show())
                    q.append(toAdd)
            else:
                #print("Point inside")
                #3 new triangle
                toAdd = self.addTriangle(Triangle([t.p1,point,t.p2]))
                #print("Adding triangle: " + toAdd.show())
                q.append(toAdd)
                toAdd = self.addTriangle(Triangle([t.p2,point,t.p3]))
                #print("Adding triangle: " + toAdd.show())
                q.append(toAdd)
                toAdd = self.addTriangle(Triangle([t.p3,point,t.p1]))
                #print("Adding triangle: " + toAdd.show())
                q.append(toAdd)
                self.eraseTriangle(t)
            #Triangles added, now to check delaunay
            visitedSet = set()
            while q:
                curTri = q.popleft()
                #print("Current triangle " + curTri.show())
                n1 = self.getNeighbour(curTri.e1)
                n2 = self.getNeighbour(curTri.e2)
                n3 = self.getNeighbour(curTri.e3)
                if n1 != None and curTri.circleTest(n1.opposingVertex(curTri.e1.getReverseEdge()),eps) >= 0:
                    #print("Circle Test Failed with: " + str(curTri.circleTest(n1.opposingVertex(curTri.e1.getReverseEdge()),eps)) + " Legalizing edge")
                    #print("Failing Triangle: " + curTri.show())
                    #print ("Failing point: " + n1.opposingVertex(curTri.e1.getReverseEdge()).show())
                    resultingTris = self.legalizeEdge(curTri,curTri.e1)
                    if resultingTris[0] not in visitedSet:
                        #print("Adding new triangle: " + resultingTris[0].show())
                        q.append(resultingTris[0])
                    if resultingTris[1] not in visitedSet:
                        #print("Adding new triangle: " + resultingTris[1].show())
                        q.append(resultingTris[1])
                elif n2 != None and curTri.circleTest(n2.opposingVertex(curTri.e2.getReverseEdge()),eps) >= 0:
                    #print("Circle Test Failed with: " + str(curTri.circleTest(n2.opposingVertex(curTri.e2.getReverseEdge()),eps)) + " Legalizing edge")
                    #print("Failing Triangle: " + curTri.show())
                    #print ("Failing point: " + n2.opposingVertex(curTri.e2.getReverseEdge()).show())
                    resultingTris = self.legalizeEdge(curTri,curTri.e2)
                    if resultingTris[0] not in visitedSet:
                        #print("Adding new triangle: " + resultingTris[0].show())
                        q.append(resultingTris[0])
                    if resultingTris[1] not in visitedSet:
                        #print("Adding new triangle: " + resultingTris[1].show())
                        q.append(resultingTris[1])
                elif n3 != None and curTri.circleTest(n3.opposingVertex(curTri.e3.getReverseEdge()),eps) >= 0:
                    #print("Circle Test Failed with: " + str(curTri.circleTest(n3.opposingVertex(curTri.e3.getReverseEdge()),eps)) + " Legalizing edge")
                    #print("Failing Triangle: " + curTri.show())
                    #print ("Failing point: " + n3.opposingVertex(curTri.e3.getReverseEdge()).show())
                    resultingTris = self.legalizeEdge(curTri,curTri.e3)
                    if resultingTris[0] not in visitedSet:
                        #print("Adding new triangle: " + resultingTris[0].show())
                        q.append(resultingTris[0])
                    if resultingTris[1] not in visitedSet:
                        #print("Adding new triangle: " + resultingTris[1].show())
                        q.append(resultingTris[1])
                visitedSet.add(curTri)

        else:
            raise NameError("need at least one triangle")

    def legalizeEdge(self,tri, edge):
        otherTri = self.getNeighbour(edge)
        opVert = otherTri.opposingVertex(edge.getReverseEdge())
        opVert2 = tri.opposingVertex(edge)
        self.eraseTriangle(tri)
        self.eraseTriangle(otherTri)
        t1 = self.addTriangle(Triangle([opVert,opVert2,edge.second]))
        t2 = self.addTriangle(Triangle([opVert2,opVert,edge.first]))
        return (t1,t2)

