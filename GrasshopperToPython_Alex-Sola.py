"""Provides a scripting component.
    Inputs:
        x: The x script variable
        y: The y script variable
    Output:
        f: Surface Output
        g: Mesh Output"""

import Rhino.Geometry as rg
import ghpythonlib.treehelpers as th
import math


#----------------------------------------------------------
#1.- create first series of points -
#start by initializing an empty list and fill it with points 
#by creating points with a for loop. The number of points should come 
#from a grasshopper slider
#Increment the X coordinate of the point at each iteration so to create
#a series of points along the X axis line
#store that point to the list
#output this list to grasshopper to verify the result should look like gh component (1.)

pointList1 = []

xAxis = range(x)
yAxisGrid = range(y)
yAxis = y

for i in xAxis:
    xPoints=rg.Point3d(i,0,0)
    pointList1.append(xPoints)
print (xPoints)

a = pointList1

#----------------------------------------------------------
#2. - create second series of points -
#create a second list of points  by copying the code above, but this time
#assign the Y coordinate of each point to a value that comes from an 
#external input which can be a slider in grasshopper
#output that list as well, the result should look like component (2.) 

#___GRID CREATION___________________________________________
#pointList2 = []

#for i in xAxis:
#    for v in yAxisGrid:
#        b=rg.Point3d(i,v,0)
#        pointList2.append(b)
#print (b)

#b=pointList2

#___POINTS CREATION___________________________________________
pointList2 = []

for i in xAxis:
    yPoints=rg.Point3d(i,yAxis,0)
    pointList2.append(yPoints)
print (yPoints)

b = pointList2

#----------------------------------------------------------
#3. - create lines from two serie of points - 
#initialize another empty list to store some lines
#make another for loop that iterates through each point in any of the list BY INDEX
#within this loop, make a line that draws from points in both lists with the same index
#and append that line to the line list. output the result
#hint: you only need one for loop for this

lineList = []

for i in range(len(pointList1)):
    lines = rg.LineCurve(a[i],b[i])
    lines.Domain = rg.Interval(0,1)
    lineList.append(lines)
    

c = lineList

#----------------------------------------------------------
#4.- divide curve -
#initialize another empty list to store some curves
#interate through every line in the line list with a for loop 
#inside the scope of this for loop, create an empty list to store the division points
#inside the for loop, convert each line to a nurbs curve, like shown in class
#divide the new curve into 10 points by applying DivideByCount() method (see rhinocommo) and store the result
#this returns a list of parameters in the line which correspond to each parameter
#you need to iterate through the list of params with another for loop and get the point per each param 
#using Line.PointAt(), and there the points in the list of divison points

allDivPts = []
for lines in lineList:
    linePts = []
    divLine = lines.ToNurbsCurve()
    params = rg.Curve.DivideByCount(divLine,yAxis,True)
    for p in params:
        divPt = rg.LineCurve.PointAt(lines,p)
        linePts.append(divPt)
    allDivPts.append(linePts)

d = th.list_to_tree(allDivPts) #this is how you output nested lists to gh trees

#----------------------------------------------------------
#5.- apply sine function to points
#here we will use the sin() the math library to move the points in Z, 
#it makes sense to follow the logic of group 5. of gh components
#first, create a nested for loop to iterate the nested list by index (I´ve done that for you)
#second, transfor the pt to a vector3d
#third, get the vector length (it´s one of it´s properties)
#forth, create a variable that will be the magnitude o*****************f displacement, by passign the vector length to the math.sin() function
#fifth, create another 3d vector, which is is the Z vector times the previous variable
#sixth, get a new point by substracting the point to the vector (literally, a point - a vector results in another point)
#finally, append that point to a list, and then append that list to the nested list

allMovedPts = []
for list in allDivPts:
    movedPts= []
    for k in list:
        vector = rg.Vector3d(k)
        length = vector.Length
        zAxis = math.sin(length) 
        zVector = rg.Vector3d(0,0,zAxis)
        newPts = k + zVector
        movedPts.append(newPts)
    allMovedPts.append(movedPts)
    print(pt)

d = th.list_to_tree(allMovedPts)

#----------------------------------------------------------
#6.- make a curve from a list of points
#again, initialize a en empty list which will contain curves
#interate through the list of list of points with a for loop
#create a curve with rg.Curve.CreateInterpolatedCurve() as in 6. (see rhinocommon)
#append that curve to the list of curves and output it to gh

#make a curve from list of points

curveList = []
for list in allMovedPts:
    intCurve = rg.Curve.CreateInterpolatedCurve(list,3)
    curveList.append(intCurve)

e= curveList

#----------------------------------------------------------
# 7.- create a loft surface from curves
#use rg.Brep.CreateFromLoft() (see rc) to create a surface from loft
#store it in a variable and output it to gh

surface = rg.Brep.CreateFromLoft(curveList,rg.Point3d.Unset,rg.Point3d.Unset,0,False)

f = surface

#----------------------------------------------------------
#8.- create a mesh from Brep
#The last step is to create a mesh from a Brep using rg.Mesh
#There are different ways to approach this, but the suggestion is to use allMovedPts
#and find a way to create mesh faces from that list and merge them into a larger mesh

#IMPORTANT TO NOTE THAT I DID THIS WITH AITOR'S HELP

newMesh = rg.Mesh()

for i in range(len(allMovedPts)):
    for j in range(len(allMovedPts[i])):
        newMesh.Vertices.Add(allMovedPts[i][j])

def coord_to_indexes (column, row):
    index = column * (len(allMovedPts[0])) + row
    return index

for i in range(1, len(allMovedPts)):
    
    for j in range(0, len(allMovedPts[i])-1):
        newMesh.Faces.AddFace(coord_to_indexes(i, j), coord_to_indexes(i, j+1), coord_to_indexes(i-1, j+1), coord_to_indexes(i-1, j))

g = newMesh

#THE END