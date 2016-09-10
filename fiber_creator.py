# fiber creator. turns DTI cloud point into obj mesh
# roger anguera, 09/2016 - roger.anguera@gazzaleylab.ucsf.edu

import random

class Vector3:
	x = 0.0
	y = 0.0
	z = 0.0

	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	def mult(scalar):
		x*=scalar
		y*=scalar
		z*=scalar

	def sum(v2):
		x+=v2.x
		y+=v2.y
		z+=v2.z


def mult (v,scalar):
	temp = Vector3(0,0,0)
	temp.x = v.x*scalar
	temp.y = v.y*scalar
	temp.z = v.z*scalar
	return temp


def sum(v1, v2):
	temp = Vector3(0,0,0)
	temp.x = v1.x+v2.x
	temp.y = v1.y+v2.y
	temp.z = v1.z+v2.z
	return temp


def map(s,a1,a2,b1,b2):
	return b1 + (s-a1)*(b2-b1)/(a2-a1);


def SmoothCurve(pointList, smoothness):
	curvedPoints = []

	if( smoothness < 1.0 ):
		smoothness = 1.0

	pointsLength = len(pointList)
	curvedLength = (pointsLength*int(smoothness))-1
	t = 0.0

	for x in range(curvedLength+1):
		t = map(x,0.0,curvedLength+1,0.0,1.0)
		points = pointList
		for j in range(pointsLength-1,0,-1):
			for k in range(0,j):
				points[k] = sum(mult(points[k],(1-t)), mult(points[k+1],t))

		curvedPoints.append(points[0])

	return curvedPoints


def WriteMesh(content, output):
	j = 0
	h = 0
	total_vertices = 0

	structural_divider = 20
	connective_divider = 1
	width = 0.2

	vertex_lines = []
	tri_lines = []

	for line in content:
		if(j == 0):
			print("processing line: " + str(h) + " - Content: " + str(len(content)))
			h+=1
			this_vertices = total_vertices
			width = random.uniform(width/2.0, width + (width/2.0))
			parsed_fields = line.split(' ')
			points = parsed_fields[3].split('|')
			tempVec = []
			if( len(points) > 10):
				for i in range(0,len(points)):
					vertices = points[i].split(';')
					tempVec.append(Vector3(
						float(vertices[0]), 
						float(vertices[1]), 
						float(vertices[2])))

				smoothed = SmoothCurve(tempVec, 1.5)
				this_vertices+=1
				w = smoothed[0]
				iw = this_vertices
				this_vertices+=1
				w1 = Vector3(smoothed[0].x + width,smoothed[0].y - 1.4,smoothed[0].z)

				iw1 = this_vertices
				this_vertices+=1
				w2 = Vector3(smoothed[0].x - width,smoothed[0].y - 1.4,smoothed[0].z)
				iw2 = this_vertices

				WriteVertex(w,vertex_lines)
				WriteVertex(w1,vertex_lines)
				WriteVertex(w2,vertex_lines)

				for i in range(0,len(smoothed)-1):
					v = w
					v1 = w1
					v2 = w2
					iv = iw
					iv1 = iw1
					iv2 = iw2

					this_vertices+=1
					w = smoothed[i+1]
					iw = this_vertices
					this_vertices+=1
					w1 = Vector3(smoothed[i+1].x + width,smoothed[i+1].y - 1.4,smoothed[i+1].z)
					iw1 = this_vertices
					this_vertices+=1
					w2 = Vector3(smoothed[i+1].x - width,smoothed[i+1].y - 1.4,smoothed[i+1].z)
					iw2 = this_vertices

					WriteVertex(w,vertex_lines)
					WriteVertex(w1,vertex_lines)
					WriteVertex(w2,vertex_lines)

					WriteFace(iv,iv1,iw,tri_lines)
					WriteFace(iv1,iw,iw1,tri_lines)
					WriteFace(iv1,iw1,iv2,tri_lines)
					WriteFace(iv2,iw2,iw1,tri_lines)
					WriteFace(iv2,iw2,iw,tri_lines)
					WriteFace(iv2,iv,iw,tri_lines)

				total_vertices=this_vertices

		if(j == connective_divider):
			j = 0
		else:
			j+=1

	for x in vertex_lines:
		output.write(x)

	for x in tri_lines:
		output.write(x)



def WriteVertex(v, ar):
	ar.append("v " + str(v.x) + " " + str(v.y) + " " + str(v.z) + "\n");


def WriteFace(v1,v2,v3,ar):
	ar.append("f " + str(v1) + " " + str(v2) + " " + str(v3)  + "\n");


def CreateMeshes():
	connected = 'streamlines_connected.txt'
	structural = 'streamlines_structural_long.txt'

	fc = open(connected)
	connected_content = fc.readlines()

	fs = open(structural)
	structural_content = fs.readlines()

	connected_output = open('connected_output.obj', 'w')
	structural_output = open('structural_output.obj', 'w')

	WriteMesh(connected_content,connected_output)
	WriteMesh(structural_content,structural_output)


CreateMeshes()