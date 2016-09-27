from triangle import Triangle
from edge import Edge

from tkinter import *

class Triangulation:
    def __init__(self):
        self.triangles = []
        self.halfEdges = {}
        self.origTriangle = None

    def addTriangle(self,tri):
    	#Add reverse of edge pointing to this tri
    	e1 = Edge(tri.e1.second,tri.e1.first)
    	e2 = Edge(tri.e2.second,tri.e2.first)
    	e3 = Edge(tri.e3.second, tri.e3.first)
    	self.halfEdges[e1] = tri
    	self.halfEdges[e2] = tri
    	self.halfEdges[e3] = tri
    	self.triangles.append(tri)
    	return tri

    #We don't need to erase edges because either other triangles will update those edges or they will never be called upon.
    def eraseTriangle(self,tri):
    	if tri in self.triangles:
    		self.triangles.remove(tri)


    'Input: point to check if its inside or out of this triangle, epsilon for orientation test'
    'Output: This triangle if it contains the point or lies in one of its edges, closest adjacent triangle if it lies outside of it.'
    def triangle_containing_point(self,tri,point,eps):
        #Orientation tests
        firstEdgeTest = tri.e1.orientation_test(point,eps)
        secondEdgeTest = tri.e2.orientation_test(point,eps)
        thirdEdgeTest = tri.e3.orientation_test(point,eps)
        if firstEdgeTest >= 0 and secondEdgeTest >= 0 and thirdEdgeTest >= 0:
            return tri
        elif firstEdgeTest < 0:
        	if tri.e1 in self.halfEdges:
        		return self.halfEdges[tri.e1]
        	return None
        elif secondEdgeTest < 0:
        	if tri.e2 in self.halfEdges:
        		return self.halfEdges[tri.e2]
        	return None
        else:
            if tri.e3 in self.halfEdges:
            	return self.halfEdges[tri.e3]
            return None

    def getNeighbour(self,edge):
    	if(edge in self.halfEdges):
    		return self.halfEdges[edge]
    	return None

    def toCanvasCoords(self, point):
    	xdif = abs(self.minx-self.maxx)
    	ydif = abs(self.miny-self.maxy)
    	return ((point.x - self.minx)/xdif*self.width,self.height-((point.y - self.miny)/ydif * self.height))

    def draw(self,drawOrigLines):
    	master = Tk()
    	self.width = 800
    	self.height = 800
    	w = Canvas(master, width = self.width, height = self.height)
    	w.pack()

    	self.minx = 10000000000
    	self.maxx = -10000000000
    	self.miny = 10000000000
    	self.maxy = -10000000000

    	for t in self.triangles:
    		self.minx = min(t.p1.x,t.p2.x,t.p3.x,self.minx)
    		self.maxx = max(t.p1.x,t.p2.x,t.p3.x,self.maxx)
    		self.miny = min(t.p1.y,t.p2.y,t.p3.y,self.miny)
    		self.maxy = max(t.p1.y,t.p2.y,t.p3.y,self.maxy)
    	origPointSet = set()
    	if self.origTriangle != None:
    		origPointSet.add(self.origTriangle.p1)
    		origPointSet.add(self.origTriangle.p2)
    		origPointSet.add(self.origTriangle.p3)
    	for t in self.triangles:
    		p1 = self.toCanvasCoords(t.p1)
    		p2 = self.toCanvasCoords(t.p2)
    		p3 = self.toCanvasCoords(t.p3)
    		if(self.origTriangle == None or drawOrigLines or (t.p1 not in origPointSet and t.p2 not in origPointSet)):
    			w.create_line(p1[0],p1[1],p2[0],p2[1])
    		if(self.origTriangle == None or drawOrigLines or (t.p2 not in origPointSet and t.p3 not in origPointSet)):
    			w.create_line(p2[0],p2[1],p3[0],p3[1])
    		if(self.origTriangle == None or drawOrigLines or (t.p3 not in origPointSet and t.p1 not in origPointSet)):
    			w.create_line(p3[0],p3[1],p1[0],p1[1])
    		#print(p1[0],p1[1],p2[0],p2[1])
    		#print(p2[0],p2[1],p3[0],p3[1])
    		#print(p3[0],p3[1],p1[0],p1[1])
    	mainloop()

    



