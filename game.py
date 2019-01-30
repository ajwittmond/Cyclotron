#! python
import os
import sys
import traceback
import pyglet
import math
import random
import pdb

try: 
	import graphics
	from geometry import *
	from pyglet.window import key
	from pyglet.gl import *
	
	
	
	keys = key.KeyStateHandler()
	graphics.window.push_handlers(keys)
	
	polygonFinal = Polygon([Vec2(100,100),Vec2(1180,100),Vec2(1180,1180),Vec2(100,1180)],True)
	
	polygonCenter = Vec2()
	for p in polygonFinal.verts:
		polygonCenter += p
		
	polygonCenter *= 1/len(polygonFinal.verts)
	
	polygon = Polygon([Vec2(100,100),Vec2(1180,100),Vec2(1180,1180),Vec2(100,1180)],True)
	
	class PolyArtist(graphics.Drawable):
		def draw(self,delta):
			glLoadIdentity()
			glLineWidth(1)
			glColor3f(1,1,1)
			l = 100
			glTranslatef(0,0,-l/2)
			for i in range(0,9):
				glTranslatef(0,0,(l/8))
				pyglet.graphics.draw(4,pyglet.gl.GL_LINE_LOOP,('v2f',polygon))
	
	class Triangle(graphics.Drawable):
		def __init__(self):
			super(Triangle,self).__init__()
			self.lines = []
			self.triangle = None
			self.visible = True
			self.t = 1
			Triangle.curr = self
			
		def addLine(self,line):
			index = len(self.lines)
			if(index==0):
				 self.lines.append(line)
			elif(index==1):
				self.lines.append(line)
			elif(index==2):
				
				self.lines.append(line)
				if(collision(self.lines[0],line)):
					self.lines.append(line)
					points = []
					points.append((collision(self.lines[0],line))[0])
					points.append(self.lines[1].p1)
					points.append(self.lines[2].p1)
					self.triangle = Polygon(points)
					print("triangle")
					for p in points:
						print(p)
				else:
					self.visible = False
					Triangle.curr = None
					
			else:
				raise Exception()
		
		def draw(self,delta):
			if(self.triangle is None):
				for l in self.lines:	
					glLoadIdentity()
					glColor3f(1,1,1)
					pyglet.graphics.draw(2,pyglet.gl.GL_LINES,('v2f',(l.p1.x,l.p1.y,l.p2.x,l.p2.y)))
			else:
				self.t-=delta
				if(self.t<=0):
					self.visible = False
					Triangle.curr = None
					
				glLoadIdentity()
				glColor3f(random.random(),random.random(),random.random())
				pyglet.graphics.draw(3,pyglet.gl.GL_POLYGON,('v2f',self.triangle))				
				
			pass
	
	Triangle.curr=None
	
	class Player(graphics.Drawable):
		def __init__(self):
			super(Player,self).__init__()
			self.shape = Circle(Vec2(),30)
			self.pos = self.shape.center
			self.tracer = Tracer(polygon,self.pos)
			self.traceLine = Line(type=Line.RAY)
			self.ju = 0
			self.jumping = False
			self.turning = False
			self.turnSpeed = math.pi*2
			self.turnTime =1 
			self.tt = 0
			self.moveSpeed = 500
			self.jumpSpeed = 2500
			self.traceResult = None
			self.cooldown = 0
			self.turnEnabled = False
			self.turnKey = 0
			self.dir = 0
			self.ctran = 0
			self.tranTime = 0.1
			self.ctarget = Vec2()
			self.prevPoint = Vec2()
			self.prevPoint2 = Vec2()
			self.turns =0
			self.triangle = None
				
		def draw(self,delta):
		
			u = self.ctran/self.tranTime
			v = Vec2(640,640) + (self.ctarget-Vec2(640,640))*u
			graphics.camera.target[0] = v.x
			graphics.camera.target[1] = v.y
			graphics.camera.target[2] = 0
			
			
		
			graphics.camera.up = [0,0,1]
			if(not self.jumping):
				if((self.triangle is not None) and (len(self.triangle.lines) < 3)):
					self.triangle.visible=False
				
				self.ctran = max(self.ctran-delta,0)
				if(keys[key.LEFT]):
					self.tracer.move(-self.moveSpeed*delta)
				elif(keys[key.RIGHT]):
					self.tracer.move(self.moveSpeed*delta)
				
				self.tracer.setPos()
				self.dir = self.tracer.currline.normal.dir+math.pi
				self.doTrace()
				self.cooldown-=delta
				
				
				
				# v = Vec2(300,0)
				# v.dir = self.traceLine.dir+ math.pi
				# v+=self.pos
				
				v = Vec2(1040,0)
				v.dir = (self.pos - Vec2(640,640)).dir
				
				v+= Vec2(640,640)
				
				graphics.camera.position = (v.x,v.y,600)
				
				if(self.cooldown <= 0 and (keys[key.SPACE] or keys[key.UP])):
					self.jumping = True
					self.ju = 0
					self.triangle = Triangle()
					self.triangle.addLine(Line(Vec2(0,0)+self.pos,Vec2(0,0)+self.traceLine.p2))
					self.prevPoint = Vec2(graphics.camera.position[0],graphics.camera.position[1])
					self.traceLine.p1.set(self.pos)
					self.turnEnabled = False
					self.turns = 0
					if(keys[key.SPACE]):
						self.turnKey = key.SPACE
					else:
						self.turnKey = key.UP
			else:
				if(not keys[self.turnKey]):
					self.turnEnabled = True
				
				if(self.turns<2 and not self.turning and self.turnEnabled and (keys[key.SPACE] or keys[key.UP])):
					self.turning = True
					self.prevPoint = Vec2(graphics.camera.position[0],graphics.camera.position[1])
					self.prevPoint2 = Vec2(graphics.camera.position[0],graphics.camera.position[1])
					self.ju = 0
					self.turns+=1
					self.turnEnabled = False
					self.tt = self.turnTime
					if(keys[key.SPACE]):
						self.turnKey = key.SPACE
					else:
						self.turnKey = key.UP
					
				if (not self.turning):
					self.ctran = max(self.ctran-delta,0)
					self.ju += (self.jumpSpeed/self.traceLine.length)*delta
				
					
					if(self.ju>1):
						self.ju=1
						self.jumping = 0 
						r = self.traceResult
						t = self.tracer
						t.currentIndex = polygon.lines.index(r[3])
						t.currline = r[3]
						t.linepos  = r[2]
						self.jumping=False
						self.turning=False
						self.cooldown = 0
						
					self.pos.set(self.traceLine.getPoint(self.ju))
				else:
				
					#set camera target
					self.ctran= min(self.tranTime,self.ctran+delta)
					v = Vec2(640,0)
					v.dir = self.dir
					self.ctarget = self.pos+v
					#set camera position
					v = Vec2(640,0)
					v.dir = self.dir+math.pi
					v+=self.pos
					self.prevPoint = self.prevPoint2 + (v-self.prevPoint2)*u
					
					
					
					if(keys[key.LEFT]):
						self.dir+=self.turnSpeed*delta
					elif(keys[key.RIGHT]):
						self.dir-=self.turnSpeed*delta
					
					
					
					self.tt-=delta
					if(self.tt <= 0):
						self.ju = 0
						self.turning= False
						self.triangle.addLine(Line(Vec2(0,0)+self.pos,Vec2(0,0)+self.traceLine.p2))
						
					if(self.turnEnabled and (keys[key.SPACE] or keys[key.UP])):
						self.ju = 0
						self.turning= False
						self.turnEnabled = False
						self.triangle.addLine(Line(Vec2(0,0)+self.pos,Vec2(0,0)+self.traceLine.p2))
						if(keys[key.SPACE]):
							self.turnKey = key.SPACE
						else:
							self.turnKey = key.UP
						
						
					
					self.doTrace()
					
			
				v2 = Vec2(1040,0)
				v2.dir = (self.traceLine.p2 - Vec2(640,640)).dir
				v2+= Vec2(640,640)
				
				v = self.prevPoint + ((v2-self.prevPoint)*self.ju)
				
				graphics.camera.position = (v.x, v.y,700)
					
				
			#draw main thing
			glLoadIdentity()
			glTranslatef(self.pos.x,self.pos.y,0)
			glRotatef(((self.dir-math.pi/2) * (360/(math.pi*2))),0,0,1)
			glColor3f(0,1,0)
			pyglet.graphics.draw(3,pyglet.gl.GL_POLYGON,('v2f',(-30,0,0,30,30,0)))
			glColor3f(0,0,1)
			glRotatef(90,0,1,0)
			pyglet.graphics.draw(3,pyglet.gl.GL_POLYGON,('v2f',(-30,0,0,30,30,0)))
			
			glLoadIdentity()
			#draw trace line
			glColor3f(1,0,0)
			pyglet.graphics.draw(2,pyglet.gl.GL_LINES,('v2f',(self.traceLine.p1.x,self.traceLine.p1.y,self.traceLine.p2.x,self.traceLine.p2.y)))
			
		def doTrace(self):
			self.traceLine.p1.set(self.pos)
			
			v = Vec2(0,1);
			v.dir = self.dir
			
			self.traceLine.p1+=v
			self.traceLine.p2 = self.traceLine.p1+v
			
			result = collision(self.traceLine,polygon)
			
			self.traceResult = result
			
			if(not result):
				pass
				# raise Exception("trace failed")
			else:
				self.traceLine.p2 = result[0]

				
	class Block(graphics.Drawable):
		def __init__(self):
			super(Block,self).__init__()
			self.shape = Rect(Vec2(120 + 1040*random.random(),120 + 1040*random.random()),Vec2(50,50))
			self.velocity = Vec2(100,0)
			self.velocity.dir = math.pi*2*random.random()
			
		def draw(self,delta):
			if(Triangle.curr is not None and Triangle.curr.triangle is not None):
				if(collision(self.shape,Triangle.curr.triangle)):
					self.visible = False
					for i in  range(10):
						vel = Vec2(500,0)
						vel.dir = random.random()*math.pi*2
						spark = Spark(Vec2(self.shape.cx,self.shape.cy),vel)
						spark.visible = True
					
			
			if(player.jumping and bounds(self.shape,player.shape)):
				self.visible = False
				for i in  range(10):
					vel = Vec2(500,0)
					vel.dir = random.random()*math.pi*2
					spark = Spark(Vec2(self.shape.cx,self.shape.cy),vel)
					spark.visible = True
			delta = min(delta,1)
			self.shape.pos+=(self.velocity*delta)
			for line in polygon.lines:
				if(collision(self.shape,line)):
					n = line.normal
					nc = n*(Vec2.dot(n,self.velocity)/Vec2.dot(n,n))
					self.velocity+=-(nc*2)
			glLoadIdentity()
			glColor3f(0,0.5,1)
			b = self.shape
			pyglet.graphics.draw(24,pyglet.gl.GL_QUADS,('v3f',(	b.x,b.y,25, b.x+b.width,b.y,25, b.x+b.width,b.y+b.height,25, b.x,b.y+b.height,25, 
																b.x,b.y,-25, b.x+b.width,b.y,-25, b.x+b.width,b.y+b.height,-25, b.x,b.y+b.height,-25,
																b.x,b.y,25, b.x+b.width,b.y,25, b.x+b.width,b.y,-25, b.x,b.y,-25,
																b.x,b.y+b.height,25, b.x+b.width,b.y+b.height,25, b.x+b.width,b.y+b.height,-25, b.x,b.y+b.height,-25,
																b.x,b.y,25, b.x,b.y+b.height,25, b.x,b.y+b.height,-25, b.x,b.y,-25,
																b.x+b.width,b.y,25, b.x+b.width,b.y+b.height,25, b.x+b.width,b.y+b.height,-25, b.x+b.width,b.y,-25,
																)))
			
	
	class Spark(graphics.Drawable):
		def __init__(self, pos, vel):
			super(Spark,self).__init__()
			self.pos = pos
			self.vel = vel
			self.time = 1
			self.t = 1;
			self.line = Line(pos,pos+(vel.normalize()*50))
			self.color = (random.random(),random.random(),random.random())
			
		def draw(self,delta):
			self.t -=delta
			if(self.t<=0):
				self.visible = False
				return
			
			u = self.t/self.time
			
			self.pos += (self.vel*u)*delta
			self.line.p2.set(self.line.p1+(self.vel.normalize()*50))
			
			for line in polygon.lines:
				if(collision(self.line,line)):
					n = line.normal
					nc = n*(Vec2.dot(n,self.vel)/Vec2.dot(n,n))
					self.vel+=-(nc*2)
					self.pos.set(self.line.p2)
					break;
					
			glLoadIdentity()
			glLineWidth(2)
			r,g,b = self.color
			glColor4f(r,g,b,u)
			
			pyglet.graphics.draw(2,pyglet.gl.GL_LINES,('v2f',(self.line.p1.x,self.line.p1.y,self.line.p2.x,self.line.p2.y)))
	
	player = Player()
	
	player.visible = True
		
	p = PolyArtist()
	p.visible = True
	
	tm = 1
	tmr = 0
	
	wiggleT = 2
	wiggleTmr = 0
	
	wiggleLength = 100
	
	print(tmr,tm)
	def update(dt):
		global tmr
		global tm
		global wiggleT
		global wiggleTmr
		global wiggleLength
		global polygon
		global polygonFinal
		
		tmr-=dt
		if(tmr<=0):
			block = Block()
			block.visible = True
			tmr = tm
			
		wiggleTmr+=dt
		if wiggleTmr>wiggleT:
			wiggleTmr -= wiggleT
		u = wiggleTmr/wiggleT
		
		for i in range(len(polygon.verts)):
			v = (polygonCenter - polygonFinal.verts[i]).normalize()
			d = math.sin((math.pi*2*u)+(i*math.pi*(3.0/4.0)))*wiggleLength
			v*=d
			polygon.verts[i].set(polygonFinal.verts[i]+v)
	
	pyglet.clock.schedule_interval(update,1/60.0)
	
	graphics.start()
except:
	traceback.print_exc()

input("press Enter to close")