import pygame
from pygame.locals import *
import sys, subprocess, os, pickle, select, socket, time, json, asyncore, random
from pathlib import Path

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Side-scrolling Multiplayer Online Platformer")
    clock = pygame.time.Clock()
    font = pygame.font.Font("./font/cour.ttf", 50)
    hotkey_font = pygame.font.Font("./font/cour.ttf",20,bold=pygame.font.Font.bold)
    hotkey_info_surface = hotkey_font.render("ENTER : Select",True,(255,255,255))

    buttons = ["GAME", "MULTIPLAYER", "OPTIONS", "QUIT"]
    menu_item = [0,1,2,3]
    current_item = 0

    screen.fill('Black')
    menu_item[0] = font.render(buttons[0], True, "Black")
    menu_item[1] = font.render(buttons[1], True, "White")
    menu_item[2] = font.render(buttons[2], True, "White")
    menu_item[3] = font.render(buttons[3], True, "White")
    pointer = font.render(">", True, "White")
    highlight = pygame.Surface((400, 60))
    highlight.fill('White')

    pointer_y = 100

    screen.blit(highlight,(140,100+(60*current_item)))

    ## loop to check for mouse action and its position ##
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if pointer_y < 280:
                        screen.fill('Black')
                        pointer_y += 60
                        current_item += 1
                        screen.blit(highlight,(140,100+(60*current_item)))
                        menu_item[current_item] = font.render(buttons[current_item], True, "Black")
                        menu_item[current_item-1] = font.render(buttons[current_item-1], True, "White")

                if event.key == pygame.K_RETURN:
##                    if current_item == 2:
##                        import data.menus.options
                    
                    if current_item == 3:
                        print("Selected QUIT")
                        pygame.quit()
                        sys.exit()

                    if current_item == 0:
                        print("Selected GAME")
                        import singleplayer
                        singleplayer.main()

                    if current_item == 1:
                        print("Selected MULTIPLAYER")
                        import multiplayer
                        multiplayer.main()
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    if pointer_y > 100:
                        screen.fill('Black')
                        pointer_y -= 60
                        current_item -= 1
                        screen.blit(highlight,(140,100+(60*current_item)))
                        menu_item[current_item+1] = font.render(buttons[current_item+1], True, "White")
                        menu_item[current_item] = font.render(buttons[current_item], True, "Black")

        screen.blit(menu_item[0],(150,100+(60*0)))
        screen.blit(menu_item[1],(150,100+(60*1)))
        screen.blit(menu_item[2],(150,100+(60*2)))
        screen.blit(menu_item[3],(150,100+(60*3)))
        screen.blit(pointer,(100,pointer_y))
        screen.blit(hotkey_info_surface,(10,450))

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
