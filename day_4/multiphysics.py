import pygame, sys, pymunk
from pygame.locals import *
import pickle
import select
import socket

WIDTH = 400
HEIGHT = 400
BUFFERSIZE = 2048

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Game')

clock = pygame.time.Clock()

space = pymunk.Space()
space.gravity = (0,100)

serverAddr = '127.0.0.1'
if len(sys.argv) == 2:
  serverAddr = sys.argv[1]

##sprite1 = pygame.image.load('images/BlueThing/BlueThing_front.png')
##sprite2 = pygame.image.load('images/Ladette/Ladette_front.png')
##sprite3 = pygame.image.load('images/TrashPanda/TrashPanda_front.png')
##sprite4 = pygame.image.load('images/Tubby/Tubby_front.png')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((serverAddr, 4321))

playerid = 0

##sprites = { 0: sprite1, 1: sprite2, 2: sprite3, 3: sprite4 }

segment_shape1 = pymunk.Segment(space.static_body, (0,0), (WIDTH,0), 2)
segment_shape1.body.position = 0, HEIGHT
segment_shape1.elasticity = 0.8
segment_shape1.friction = 0.1
space.add(segment_shape1)

class Minion:
  def __init__(self, x, y, id):
    self.id = id
    self.body = pymunk.Body(1,100,body_type = pymunk.Body.DYNAMIC)
    self.body.position = (x,y)
    self.shape = pymunk.Circle(self.body,20)
    space.add(self.body,self.shape)

  def update(self):
##    if self.body.position.x > WIDTH - 50:
##      self.body.position.x = WIDTH - 50
##    if self.body.position.x < 0:
##      self.body.position.x = 0
##    if self.body.position.y > HEIGHT - 50:
##      self.body.position.y = HEIGHT - 50
##    if self.body.position.y < 0:
##      self.body.position.y = 0

    if self.id == 0:
      self.id = playerid

  def render(self):
    pygame.draw.circle(screen,(0,0,0),self.body.position,20)


#game events
#['event type', param1, param2]
#
#event types: 
# id update 
# ['id update', id]
#
# player locations
# ['player locations', [id, x, y], [id, x, y] ...]

#user commands
# position update
# ['position update', id, x, y]

##class GameEvent:
##  def __init__(self, vx, vy):
##    self.vx = vx
##    self.vy = vy

cc = Minion(50, 50, 0)

minions = []

while True:
  ins, outs, ex = select.select([s], [], [], 0)
  for inm in ins: 
    gameEvent = pickle.loads(inm.recv(BUFFERSIZE))
    if gameEvent[0] == 'id update':
      playerid = gameEvent[1]
      print(playerid)
    if gameEvent[0] == 'player locations':
      gameEvent.pop(0)
      minions = []
      for minion in gameEvent:
        if minion[0] != playerid:
          minions.append(Minion(minion[1], minion[2], minion[0]))
    
  for event in pygame.event.get():
    if event.type == QUIT:
    	pygame.quit()
    	sys.exit()
    if event.type == KEYDOWN:
      if event.key == K_LEFT: cc.vx = -10
      if event.key == K_RIGHT: cc.vx = 10
      if event.key == K_UP: cc.vy = -10
      if event.key == K_DOWN: cc.vy = 10
    if event.type == KEYUP:
      if event.key == K_LEFT and cc.vx == -10: cc.vx = 0
      if event.key == K_RIGHT and cc.vx == 10: cc.vx = 0
      if event.key == K_UP and cc.vy == -10: cc.vy = 0
      if event.key == K_DOWN and cc.vy == 10: cc.vy = 0

  clock.tick(60)
  screen.fill((255,255,255))

  cc.update()

  for m in minions:
    m.render()

  cc.render()

  space.step(1/50)

  pygame.display.flip()

  pygame.display.update()

  ge = ['position update', playerid, cc.body.position.x, cc.body.position.y]
  s.send(pickle.dumps(ge))
s.close()
