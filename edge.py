from point import Point

#Utility class for edges
class Edge:
	def __init__(self,pointA,pointB):
		self.first = pointA
		self.second = pointB

	'Input: Point'
	'Output: Num'
	#Determinant of edge against point, used for orientation test.
	def det(self,point):
		return (self.first.x - point.x)*(self.second.y - point.y) - (self.first.y - point.y)*(self.second.x - point.x)


	'Input: Point, Num'
	'Output: 1 if the point is to the left of the edge, -1 if to the right, 0 if on the edge within epsilon value'
	#Orientation test, checks Edge against point.
	def orientation_test(self,point,eps):
		val = self.det(point)
		#print(val)
		if(abs(val) < eps):
			return 0
		elif val > eps:
			return 1
		else:
			return -1

	def getReverseEdge(self):
		return Edge(self.second,self.first)

	def show(self):
		return '[ ' + self.first.show() + ', ' + self.second.show() + ']'

	def __eq__(self,other):
		if isinstance(other,Edge):
			return self.first == other.first and self.second == other.second
		return NotImplemented
	def __key(self):
		return (self.first,self.second)
	def __hash__(self):
		return hash(self.__key())


