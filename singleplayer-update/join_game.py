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
    hotkey_info_surface = hotkey_font.render("ESC : Back  ENTER : Select",True,(255,255,255))

    buttons = []
    menu_item = []
    count = -1

    ip = ""

    conf = Path("./ipconfig.txt")
    if conf.exists():
        with open("ipconfig.txt") as config:
            for line in config:
                if "ip=" in line:
                    line = line.replace("ip=", "")
                    count+=1
                    menu_item.append(count)
                    for char in line:
                        if char.isdigit() or "." in char:
                            ip = ip + str(char)
                    buttons.append(ip)
                    ip = ""
    else:
        buttons.append("127.0.0.1")
        menu_item.append("127.0.0.1")
    
    current_item = 0
    screen.fill('Black')
    
    menu_item[0] = font.render(buttons[0], True, "Black")

    for i in range(1,len(menu_item)):
        menu_item[i] = font.render(buttons[i], True, "White")

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
                        if len(menu_item)-1 != 0:
                            current_item += 1
                            pointer_y += 60
                        if current_item > len(menu_item)-1:
                            current_item -= 1
                            pointer_y -= 60
                        screen.blit(highlight,(140,100+(60*current_item)))
                        if len(menu_item)-1 > 0:
                            menu_item[current_item] = font.render(buttons[current_item], True, "Black")
                            menu_item[current_item-1] = font.render(buttons[current_item-1], True, "White")

                if event.key == pygame.K_RETURN:
                    import game
                    game.main(buttons[current_item])

                if event.key == pygame.K_ESCAPE:
                    import multiplayer
                    multiplayer.main()
                    
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    if pointer_y > 100:
                        screen.fill('Black')
                        current_item -= 1
                        pointer_y -= 60
                        screen.blit(highlight,(140,100+(60*current_item)))
                        if len(menu_item)-1 > 0:
                            menu_item[current_item+1] = font.render(buttons[current_item+1], True, "White")
                            menu_item[current_item] = font.render(buttons[current_item], True, "Black")

        screen.blit(menu_item[0],(150,100+(60*0)))
        for i in range(1,len(menu_item)):
            screen.blit(menu_item[i],(150,100+(60*i)))
        screen.blit(pointer,(100,pointer_y))
        screen.blit(hotkey_info_surface,(10,450))

        pygame.display.update()
        clock.tick(60)
