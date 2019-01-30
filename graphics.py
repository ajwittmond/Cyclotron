#! python 
import pyglet
import time
from pyglet.gl import *

drawables = []
removes = []

window = pyglet.window.Window(1280,720)

last_time = 0



class Camera:
	def __init__(self,target=[0,0,0],position=[0,0,0],up=[0,0,0]):
		self.target = target
		self.position = position
		self.up = up
	
	def do_transformation(self):
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(60,1280.0/720.0,1,100000)
		gluLookAt(self.position[0],self.position[1],self.position[2],
				self.target[0],self.target[1],self.target[2],
				self.up[0],self.up[1],self.up[2])



class Drawable(object):
	def __init__(self):
		self.__visible = False

	@property
	def visible(self):
		return self.__visible
	
	@visible.setter
	def visible(self,visible):
		if (self.visible and not visible) :
			removes.append(self)
		elif (not self.visible and visible) :
			drawables.append(self)
		self.__visible = visible
		
	def draw(self,delta):
		pass

		
def start():
	last_time = time.time()
	pyglet.app.run()
	
	
camera = Camera()

@window.event
def on_draw():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glEnable(GL_DEPTH_TEST )
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
	# glMatrixMode(GL_PROJECTION)
	# glLoadIdentity()
	# gluPerspective(60,1280.0/720.0,1,1000)
	# gluLookAt(640,360,700,640,360,0,0,1,0)
	camera.do_transformation()
	glMatrixMode(GL_MODELVIEW)
	global last_time
	t = time.time()
	delta = t-last_time
	last_time = t
	for d in drawables:
		d.draw(delta)
		
	while(len(removes)>0):
		drawables.remove(removes.pop())