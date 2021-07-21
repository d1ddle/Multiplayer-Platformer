import pygame, sys
from pygame.locals import *
import pickle
import select
import socket

class Minion(pygame.sprite.Sprite):
  def __init__(self, x, y, id):
    # Call the parent's constructor
    super().__init__()
 
    # Create an image of the block, and fill it with a color.
    # This could also be an image loaded from the disk.
    width = 40
    height = 60
    self.image = pygame.Surface([width, height])
    self.image.fill(RED)

    # Set a referance to the image rect.
    self.rect = self.image.get_rect()

    # Set speed vector of player
    self.change_x = 0
    self.change_y = 0

    # List of sprites we can bump against
    self.level = None
    self.id = id
    self.rect.x = x
    self.rect.y = y

  def update(self):
    """ Move the player. """
    # Gravity
    self.calc_grav()

    # Move left/right
    self.rect.x += self.change_x

    # See if we hit anything
    block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
    for block in block_hit_list:
        # If we are moving right,
        # set our right side to the left side of the item we hit
        if self.change_x > 0:
            self.rect.right = block.rect.left
        elif self.change_x < 0:
            # Otherwise if we are moving left, do the opposite.
            self.rect.left = block.rect.right

    # Move up/down
    self.rect.y += self.change_y

    # Check and see if we hit anything
    block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
    for block in block_hit_list:

        # Reset our position based on the top/bottom of the object.
        if self.change_y > 0:
            self.rect.bottom = block.rect.top
        elif self.change_y < 0:
            self.rect.top = block.rect.bottom

        # Stop our vertical movement
        self.change_y = 0

    if self.id == 0:
      self.id = playerid

  def calc_grav(self):
      """ Calculate effect of gravity. """
      if self.change_y == 0:
          self.change_y = 1
      else:
          self.change_y += .35

      # See if we are on the ground.
      if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
          self.change_y = 0
          self.rect.y = SCREEN_HEIGHT - self.rect.height

  def jump(self):
      """ Called when user hits 'jump' button. """

      # move down a bit and see if there is a platform below us.
      # Move down 2 pixels because it doesn't work well if we only move down 1
      # when working with a platform moving down.
      self.rect.y += 2
      platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
      self.rect.y -= 2

      # If it is ok to jump, set our speed upwards
      if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
          self.change_y = -10

  # Player-controlled movement:
  def go_left(self):
      """ Called when the user hits the left arrow. """
      self.change_x = -6

  def go_right(self):
      """ Called when the user hits the right arrow. """
      self.change_x = 6

  def stop(self):
      """ Called when the user lets off the keyboard. """
      self.change_x = 0

  def render(self):
    screen.blit(sprites[self.id % 4], (self.rect.x, self.rect.y))
    



class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """
 
    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this code.
            """
        super().__init__()
 
        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)
 
        self.rect = self.image.get_rect()
 
 
class Level():
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """
 
    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving
            platforms collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
 
        # How far this world has been scrolled left/right
        self.world_shift = 0
 
    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()
 
    def draw(self, screen):
        """ Draw everything on this level. """
 
        # Draw the background
        screen.fill(BLUE)
 
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
 
    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll
        everything: """
 
        # Keep track of the shift amount
        self.world_shift += shift_x
 
        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x
 
        for enemy in self.enemy_list:
            enemy.rect.x += shift_x
 
 
# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)
 
        self.level_limit = -1000
 
        # Array with width, height, x, and y of platform
        level = [[210, 70, 500, 500],
                 [210, 70, 800, 400],
                 [210, 70, 1000, 500],
                 [210, 70, 1120, 280],
                 ]
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

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


pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BUFFERSIZE = 2048

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Side-scrolling Platformer Multiplayer')


# Create the player
player = Minion(300, SCREEN_HEIGHT, 0)

# Create all the levels
level_list = []
level_list.append(Level_01(player))

# Set the current level
current_level_no = 0
current_level = level_list[current_level_no]

active_sprite_list = pygame.sprite.Group()
player.level = current_level

player.rect.x = 340
player.rect.y = SCREEN_HEIGHT - player.rect.height
active_sprite_list.add(player)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()


serverAddr = '127.0.0.1'
if len(sys.argv) == 2:
  serverAddr = sys.argv[1]

sprite1 = pygame.image.load('images/BlueThing/BlueThing_front.png')
sprite2 = pygame.image.load('images/Ladette/Ladette_front.png')
sprite3 = pygame.image.load('images/TrashPanda/TrashPanda_front.png')
sprite4 = pygame.image.load('images/Tubby/Tubby_front.png')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((serverAddr, 4321))

playerid = 0

sprites = { 0: sprite1, 1: sprite2, 2: sprite3, 3: sprite4 }


cc = player

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
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            player.go_left()
        if event.key == pygame.K_RIGHT:
            player.go_right()
        if event.key == pygame.K_UP:
            player.jump()

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT and player.change_x < 0:
            player.stop()
        if event.key == pygame.K_RIGHT and player.change_x > 0:
            player.stop()

  # Update the player.
  active_sprite_list.update()

  # Update items in the level
  current_level.update()

  # If the player gets near the right side, shift the world left (-x)
  if player.rect.right >= 500:
      diff = player.rect.right - 500
      player.rect.right = 500
      current_level.shift_world(-diff)

  # If the player gets near the left side, shift the world right (+x)
  if player.rect.left <= 120:
      diff = 120 - player.rect.left
      player.rect.left = 120
      current_level.shift_world(diff)

  # If the player gets to the end of the level, go to the next level
  current_position = player.rect.x + current_level.world_shift
  if current_position < current_level.level_limit:
      player.rect.x = 120
      if current_level_no < len(level_list)-1:
          current_level_no += 1
          current_level = level_list[current_level_no]
          player.level = current_level

  # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
  current_level.draw(screen)
  active_sprite_list.draw(screen)

  # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

  # Limit to 60 frames per second
  clock.tick(60)

  cc.update()

  for m in minions:
    m.render()

  cc.render()

  pygame.display.flip()

  ge = ['position update', playerid, cc.rect.x, cc.rect.y]
  s.send(pickle.dumps(ge))
s.close()
