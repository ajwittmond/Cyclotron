#! python
import math

class Vec2:
	def __init__(self,x=0.0,y=0.0):
		self.x=float(x)
		self.y=float(y)
	
	def __getitem__(self,item):
		if(item==0):
			return self.x
		elif(item==1):
			return self.y
		else:
			raise Exception("not a valid vector index: "+item);
		
	def __setitem__(self,item,value):
		if(item==0):
			self.x = value
		elif(item==1):
			self.y = value
		else:
			raise Exception("not a valid vector index: "+item);
			
	def __len__(self):
		return 2
		
	def __neg__(self):
		return Vec2(-self.x,-self.y)
	
	def __add__(self,other):
		try:
			return Vec2(self.x+other[0],self.y+other[1]) 
		except: 
			return Vec2(self.x+other,self.y+other)
			
	def __radd__(self,other):
		return self+other
		
	def __iadd__(self,other):
		self.x+=other[0]
		self.y+=other[1]
		return self
		
	def __sub__(self,other):
		try:
			return Vec2(self.x-other[0],self.y-other[1]) 
		except: 
			return Vec2(self.x-other,self.y-other)
			
	def __rsub__(self,other):
		return self+other
		
	def __isub__(self,other):
		self.x-=other[0]
		self.y-=other[1]
		return self
		
	def __mul__(self,other):
		return Vec2(self.x*other,self.y*other)
		
	def __rmul__(self,other):
		return self*other
		
	def __imul__(self,other):
		self.x*=other
		self.y*=other
		return self
		
	def __div__(self,other):
		return Vec(self.x/other,self.y/other)
		
	def __rdiv__(self,other):
		return self/other
		
	def __idiv__(self,other):
		self.x/=other
		self.y/=other
		return self
		
	def normalize(self):
		return self * (1/self.length)
	
	@property
	def length(self):
		return math.sqrt(self.x**2 + self.y**2)
	
	@length.setter
	def length(self,val):
		l = self.length
		self.x = (self.x/length)*val
		self.y = (self.y/length)*val
	
	@property
	def dir(self):
		return math.atan2(self.y,self.x)
		
	@dir.setter
	def dir(self,val):
		l = self.length
		self.x = math.cos(val)*l
		self.y = math.sin(val)*l
	
	def set(self,val):
		self.x = val[0]
		self.y = val[1]
	
	def __str__(self):
		return "["+str(self.x)+" "+str(self.y)+"]"
		
	@staticmethod
	def dot(v1,v2):
		return (v1.x*v2.x)+(v1.y*v2.y)
	
	@staticmethod
	def dist(v1,v2):
		return math.sqrt((v1[0]-v2[0])**2 + (v1[1]-v2[1])**2)

Point = Vec2
		
class Rect:
	def __init__(self,position,dimensions):
		self.pos = position
		self.dim = dimensions
	
	@property
	def x(self):
		return self.pos[0]
		
	@x.setter
	def x(self,val):
		self.pos[0] = val
	
	@property
	def y(self):
		return self.pos[1]
		
	@y.setter
	def y(self,val):
		self.pos[1] = val
	
	@property
	def width(self):
		return self.dim[0]
		
	@width.setter
	def width(self,val):
		self.dim[0] = val
	
	@property
	def height(self):
		return self.dim[1]
		
	@height.setter
	def height(self,val):
		self.dim[1] = val
		
	@property	
	def cx(self):
		return self.x + self.width/2
		
	@cx.setter
	def cx(self,val):
		self.x = val - (self.width/2)
		
	@property	
	def cy(self):
		return self.y + self.height/2
		
	@cy.setter
	def cy(self,val):
		self.y = val - (self.height/2)
	
	def getCenter(self):
		return Vec2(self.cx,self.cy)
	
	def setCenter(self,val):
		self.cx = val[0]
		self.cy = val[1]

class Circle:
	def __init__(self,center,radius):
		self.center = center
		self.radius = radius
	
	@property
	def x(self):
		return self.center[0] - self.radius
		
	@x.setter
	def x(self,val):
		self.center[0] = val+self.radius
		
	@property
	def y(self):
		return self.center[1] - self.radius
		
	@y.setter
	def y(self,val):
		self.center[1] = val+self.radius
	
	@property
	def cx(self):
		return self.center[0]
		
	@cx.setter
	def cx(self,val):
		self.center[0] = val
		
	@property
	def cy(self):
		return self.center[1]
		
	@cy.setter
	def cy(self,val):
		self.center[1] = val
		
	@property
	def width(self):
		return self.radius+self.radius
		
	@width.setter
	def width(self,val):
		self.radius = val/2
		
	@property
	def height(self):
		return self.radius+self.radius
		
	@height.setter
	def height(self,val):
		self.radius = val/2
	
class Line:
	LINE = 0
	SEGMENT = 1
	RAY = 2
	def __init__(self,p1=Vec2(),p2=Vec2(),type=SEGMENT):
		self.p1 = p1
		self.p2 = p2
		self.type = type
		
	@property
	def x(self):
		return min(self.p1.x,self.p2.x)
	
	@x.setter
	def x(self,val):
		dif = val-self.x
		self.p1.x+=dif
		self.p2.x+=dif
	
	@property
	def y(self):
		return min(self.p1.y,self.p2.y)
	
	@y.setter
	def y(self,val):
		dif = val-self.y
		self.p1.y+=dif
		self.p2.y+=dif
	
	@property
	def cx(self):
		return (self.p1.x + self.p2.x)/2
		
	@cx.setter
	def cx(self,val):
		dif = val - self.cx;
		self.p1.x+=dif
		self.p2.x+=dif
		
	@property
	def cy(self):
		return (self.p1.y + self.p2.y)/2
		
	@cy.setter
	def cy(self,val):
		dif = val - self.cy;
		self.p1.y+=dif
		self.p2.y+=dif
		
	@property
	def width(self):
		return abs(self.p1.x-self.p2.x)
	
	@width.setter
	def width(self,val):
		scale = val/self.width
		cx = self.cx
		self.p1.x = cx + (self.p1.x-cx)*scale
		self.p2.x = cx + (self.p2.x-cx)*scale
		
	@property
	def height(self):
		return abs(self.p1.y-self.p2.y)
	
	@height.setter
	def height(self,val):
		scale = val/self.height
		cy = self.cy
		self.p1.y = cy + (self.p1.y-cy)*scale
		self.p2.y = cy + (self.p2.y-cy)*scale
	
	@property
	def length(self):
		return Vec2.dist(self.p1,self.p2)
	
	#scale around p1
	@length.setter
	def length(self,val):
		scale = val/self.length
		self.p2.x = self.p1.x + (self.p2.x-self.p1.x)*scale
		self.p2.y = self.p1.y + (self.p2.y-self.p1.y)*scale
	
	#the direction from the first point
	@property
	def dir(self):
		return math.atan2(self.p2.y-self.p1.y,self.p2.x-self.p1.x)
	
	#rotates around the first point
	@dir.setter
	def dir(self, val):
		v = Vec2(self.p2.x-self.p1.x,self.p2.y-self.p1.y)
		v.dir = val;
		self.p2.x = self.p1.x+v.x;
		self.p2.y = self.p1.y+v.y
	
	@property
	def normal(self):
		return Vec2((self.p2.y - self.p1.y), -(self.p2.x - self.p1.x))
		
	def getPoint(self,u):
		return self.p1 + ((self.p2-self.p1)*u)
		
	def onLine(self,u):
		return self.type is Line.LINE or (u>0 and (self.type is Line.RAY))
	
class Polygon:
	"class for a simple 2d convex polygon"
	def __init__(self,verts,inward=False):
		if(len(verts)<3):
			raise Exception("cannot have a polygon with less than three vertices")
		self.verts = verts
		lines = []
		for i in range(1,len(verts)):
			lines.append(Line(verts[i-1],verts[i]))
		lines.append(Line(verts[len(verts)-1],verts[0]))
		self.lines = lines	
		
		self.set_dimensions()
	
	def set_dimensions(self):
		"call after direct vertex modifications if box dimensions are to be used.  iterates through the vertices to find the polygon's dimensions and center of mass"
		minx = self.verts[0].x
		maxx = minx
		miny = self.verts[0].y
		maxy = miny
		
		cm = Vec2()
		
		for v in self.verts :
			minx = min(minx,v.x)
			maxx = max(maxx,v.x)
			miny = min(miny,v.y)
			maxy = min(maxy,v.y)
			cm += v
		
		cm *= 1.0/len(self.verts)
		
		self.cm = cm
		
		self.__box = Rect((minx,miny),(maxx-minx,maxy-miny))
		
	def __getitem__(self,item): 
		return self.verts[item//2][item%2]
	
	def __setitem__(self,item,val):
		self.verts[item//2][item%2] = val
		
	def __len__(self):
		return len(self.verts)*2
		
	@property
	def x(self):
		return self.__box.x
		
	@x.setter
	def x(self,val):
		dif = val - self.__box.x
		self.__box.x = val
		self.cm.x+=dif
		for v in self.verts:
			v.x += dif
		
	@property
	def y(self):
		return self.__box.y
		
	@y.setter
	def y(self,val):
		dif = val - self.__box.y
		self.__box.y = val
		self.cm.y+=dif
		for v in self.verts:
			v.y += dif
	
	@property
	def cx(self):
		return self.__box.cx
		
	@cx.setter
	def cx(self,val):
		dif = val - self.__box.cx
		self.__box.cx = val
		self.cm.x+=dif
		for v in self.verts:
			v.cx += dif
		
	@property
	def cy(self):
		return self.__box.cy
		
	@cy.setter
	def cy(self,val):
		dif = val - self.__box.cy
		self.__box.cy = val
		self.cm.cy+=dif
		for v in self.verts:
			v.cy += dif	
	
	
	@property
	def width(self):
		return self.__box.width
	
	@property
	def height(self):
		return self.__box.height
	
class Tracer:
	def __init__(self,polygon,pos):
		self.polygon = polygon
		self.pos = pos
		self.currentIndex = 0
		self.linepos = 0
		self.currline = polygon.lines[0]
		pos.set(self.currline.p1)
	
	def setPos(self):
		self.pos.set(self.currline.getPoint(self.linepos))
		
	def move(self,dist):
		length = self.currline.length
		self.linepos+= dist/length
		if(self.linepos>1):
			dif = (self.linepos-1)*length
			self.linepos = 0
			self.currentIndex = (self.currentIndex+1)%len(self.polygon.lines)
			self.currline = self.polygon.lines[self.currentIndex]
			self.move(dif)
		elif(self.linepos<0):
			dif = self.linepos*length
			self.linepos = 1
			self.currentIndex = (self.currentIndex-1)
			if(self.currentIndex<0):
				self.currentIndex=len(self.polygon.lines)-1
			self.currline = self.polygon.lines[self.currentIndex]
			self.move(dif)
		
def bounds(a,b):
	return (a.x <= b.x+b.width) and (a.x+a.width >= b.x) and (a.y <= b.y+b.height) and (a.y+a.height >= b.y)

boxBox = bounds
	
def circleRect(c,b):
	if(bounds(c,b)):
		print(bounds)
		return (pointInCircle((b.x,b.y),c) or pointInCircle((b.x+b.width,b.y),c) or 
				pointInCircle((b.x+b.width,b.y+b.height),c) or pointInCircle((b.x,b.y+b.height),c))	
	else:
		return False
	
def circleCircle(a,b):
	return Vec2.dist(a.center,b.center)<(a.radius+b.radius)

def circlePolygon(c,p):
	if(bounds(c,p)):
		if(pointInPolygon(c.center,p)):
			return True
		else:
			for l in p.lines :
				if(lineCircle(l,c)):
					return true
	return False
		
def lineLine(a,b):
	if((a.type is not Line.SEGMENT or  b.type is not Line.SEGMENT) or bounds(a,b)):
		denom = (((b.p2.y-b.p1.y)*(a.p2.x-a.p1.x))-((b.p2.x-b.p1.x)*(a.p2.y-a.p1.y)));
		if(not denom == 0):
			ua = 	(((b.p2.x-b.p1.x)*(a.p1.y-b.p1.y))-
						((b.p2.y-b.p1.y)*(a.p1.x-b.p1.x)))/denom;
			ub = 	(((a.p2.x-a.p1.x)*(a.p2.y-b.p1.y))-
						((a.p2.y-a.p1.y)*(a.p1.x-b.p1.x)))/denom;
			if(((a.type is Line.LINE) or (ua>=0 and (ua<=1 or a.type is Line.RAY))) and ((b.type is Line.LINE) or (ub>=0 and (ub<=1 or b.type is Line.RAY)))):
				return (a.getPoint(ua),ua,ub)	
	return False;
	
def lineRect(l,r):
	if(bounds(l,r)):return True
	side = lineRect.line
	side = Line()
	if(l.type is not Line.SEGMENT or bounds(l,r)):
		side.p1.set((r.x,r.y))
		side.p2.set((r.x+r.width,r.y))
		v = lineLine(l,side)
		if(v):
			return True
		side.p1.set((r.x+r.width,r.y))
		side.p2.set((r.x+r.width,r.y+r.height))
		v = lineLine(l,side)
		if(v):
			return True
		side.p1.set((r.x+r.width,r.y+r.height))
		side.p2.set((r.x,r.y+r.height))
		v = lineLine(l,side)
		if(v):
			return True
		side.p1.set((r.x,r.y+r.height))
		side.p2.set((r.x,r.y))
		v = lineLine(l,side)
		if(v):
			return True
	return False
lineRect.line = Line()
		
def lineCircle(l,c):
	if(l.type is not Line.SEGMENT or bounds(l,c)):
		p1 = l.p1 - c.center
		p2 = l.p2 - c.center
		pdif = p2 - p1
		
		a = (pdif[0]*pdif[0])+(pdif[1]*pdif[1])
		b = 2 * ((pdif[0]*p1[0])+(pdif[1]*p1[1]))
		c = (p1[0]*p1[0]) + (p1[1]*p1[1]) - (c.radius*c.radius)
		delta = (b*b) - (4*a*c)
		
		if(delta>=0):
			if(delta<0):
				u = -b/(2*a)
				if(l.isOnLine(u)):
					return (l.getPoint(u),);
			else:
				u1 = (-b + math.sqrt(delta))/(2*a)
				u2 = (-b - math.sqrt(delta))/(2*a)
				if(l.isOnLine(u1) and l.isOnLine(u2)):
					return (l.getPoint(u1),l.getPoint(u2));
					
	return False
	
def linePolygon(l,p):
	if(l.type is not Line.SEGMENT or bounds(l,p)):
		res = False
		for line in p.lines:
			a = lineLine(l,line)
			if(a and (not res or Vec2.dist(res[0],l.p1)>Vec2.dist(a,l.p1))):
				res = (a[0],a[1],a[2],line)
		return res
	return false
	
def pointInRect(p,b):
	return p.x>=b.x and p.x<=b.x+b.width and p.y>=b.y and p.y<=b.y+b.height
	
def pointInCircle(p,c):
	return (p-c.center).length < c.radius
	
def pointInPolygon(p,poly):
	pass
	
def pointOnLine(p,l):
	pass
	
def polygonRect(p,r):
	return polygonPolygon(p,Polygon([
		Vec2(r.x,r.y),
		Vec2(r.x+r.width,r.y),
		Vec2(r.x+r.width,r.y+r.height),
		Vec2(r.x,r.y+r.height)
	]))

#takes face normal and projects all of the points onto it getting the min and max values for each polygon
#then it compares min and max values to look for overlap
def polygonPolygonAxisTest(axis,c,a,b):
	mina=None
	maxa=None
	
	minb=None
	maxb=None
	for i in range(0,len(a),2):
		val = Vec2.dot(axis,Vec2(a[i],a[i+1])-c)
		if mina is None:
			mina = val
			maxa = val
		else:
			if mina>val:
				mina = val
			
			if maxa<val:
				maxa = val
	
	for i in range(0,len(b),2):
		val = Vec2.dot(axis,Vec2(b[i],b[i+1])-c)
		if minb is None:
			minb = val
			maxb = val
		else:
			if minb>val:
				minb = val
			
			if maxb<val:
				maxb = val
				
	return (mina<=maxb and maxa>=minb) 
	
def polygonPolygon(a,b):
	v = False
	for i in range(0,len(a),2):
		c = Vec2(a[i],a[i+1])
		temp = Vec2(a[(i+2)%len(a)],a[(i+3)%len(a)])-c
		axis = Vec2(temp.y,-temp.x).normalize()
		if(not polygonPolygonAxisTest(axis,c,a,b)):
			return False
	
	for i in range(0,len(b),2):
		c = Vec2(b[i],b[i+1])
		temp = Vec2(b[(i+2)%len(b)],b[(i+3)%len(b)])-c
		axis = Vec2(temp.y,-temp.x).normalize()
		if(not polygonPolygonAxisTest(axis,c,a,b)):
			return False
			
	return True

collisionTable = {
	Point:{
		Point: lambda a,b: a==b,
		Rect: pointInRect,
		Circle: pointInCircle,
		Polygon: pointInPolygon,
		Line: pointOnLine
	},
	Rect:{
		Rect: boxBox,
		Point: lambda r,p: pointInRect(p,r),
		Circle: lambda r,c: circleRect(c,r),
		Line: lambda r,l: lineRect(l,r),
		Polygon: lambda r,p: polygonRect(p,r)
	},
	Circle:{
		Rect: circleRect,
		Point: lambda c,p: pointInCircle(p,c),
		Line: lambda c,l: lineCircle(l,c),
		Circle: circleCircle,
		Polygon: circlePolygon
	},
	Line:{
		Point: lambda l,p: pointOnLine(p,l),
		Rect: lineRect,
		Circle: lineCircle,
		Line: lineLine,
		Polygon: linePolygon
	},
	Polygon:{
		Point: lambda po,p: pointInPolygon(p,po),
		Rect: polygonRect,
		Circle: lambda p,c: circlePolygon(c,p),
		Line: lambda p,l: linePolygon(l,p),
		Polygon: polygonPolygon
	}
	
}

	
def collision(a,b):
	return collisionTable[a.__class__][b.__class__](a,b)
		