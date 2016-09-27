from delaunayT import DelaunayT
from point import Point
import random

def main():
	#delaunayTri = DelaunayT([Point(0,0)])
	num = 100
	points = []
	xRange = 1000
	yRange = 1000
	for i in range(0,num):
		points.append(Point(random.randint(-xRange,xRange),random.randint(-yRange,yRange)))
	delaunayTri = DelaunayT(points)
	# for i in range(0,num):
	# 	for j in range(0,num):
	# 		points.append(Point(i * xRange/num, j * yRange/num))
	# delaunayTri = DelaunayT(points)


if __name__ == "__main__":
	main()
