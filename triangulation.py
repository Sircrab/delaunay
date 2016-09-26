import triangle

class Triangulation:
    def __init__(self):
        self.triangles = []
        self.halfEdges = {}

    def addTriangle(self,tri):
    	#Add reverse of edge pointing to this tri
    	e1 = Edge(tri.e1.second,tri.e1.first)
    	e2 = Edge(tri.e2.second,tri.e1.first)
    	e3 = Edge(tri.e3.second, tri.e1.first)
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
        	if tri.e1 in halfEdges:
        		return halfEdges[tri.e1]
        	return None
        elif secondEdgeTest < 0:
        	if tri.e2 in halfEdges:
        		return halfEdges[tri.e2]
        	return None
        else:
            if tri.e3 in halfEdges:
            	return halfEdges[tri.e3]
            return None

    def getNeighbour(self,edge):
    	if(edge in self.halfEdges):
    		return self.halfEdges[edge]
    	return None


