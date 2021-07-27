import pygame,sys,json,time,os

def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode([640,480])
    base_font = pygame.font.Font("./font/cour.ttf",50,bold=pygame.font.Font.bold)
    hotkey_font = pygame.font.Font("./font/cour.ttf",20,bold=pygame.font.Font.bold)
    user_text = ''

    input_rect = pygame.Rect(140,100,200,59)
    delete_rect = pygame.Rect(30,300,440,59)
    color_active = pygame.Color('White')
    color_passive = pygame.Color(128,128,128)
    color = color_passive

    active = False
    written = False
    deleted = False
    ip = True

    old_user_text = user_text
    written_text_surface = base_font.render("",True,(255,255,255))
    ip_text_surface = base_font.render("IP:",True,(255,255,255))
    delete_text_surface = base_font.render("Delete Config?",True,(255,255,255))
    hotkey_info_surface = hotkey_font.render("ESC : Back  ENTER : Save Config",True,(255,255,255))

    frame = 0

    def file_write(old_user_text, written, ip, user_text):
        if user_text != "":
            user_text_lowercase = user_text.lower()
            user_text_uppercase = user_text.upper()
            is_not_ip = user_text_lowercase.islower()
            is_not_ip_2 = user_text_uppercase.isupper()
##            print(user_text_lowercase)
##            print(user_text_uppercase)
            if is_not_ip_2:
                print("IP Error: not a valid IP address.")
            elif is_not_ip:
                print("IP Error: not a valid IP address.")
            elif old_user_text != user_text and ip:
                with open('ipconfig.txt','a') as file:
                    json.dump("ip=" + user_text,file)
                    file.write("\n")
                    json.dump("port=4321",file)
                    file.write("\n")
                print("IP Config Written.")
                written = True
                old_user_text = user_text
        else:
            written = False
        ip = True
        return written

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                    deleted = False
                else:
                    if active:
                        active = False
                        written = file_write(old_user_text, written, ip, user_text)
                    if deleted:
                        deleted = False
                if delete_rect.collidepoint(event.pos):
                    try:
                        os.remove("ipconfig.txt")
                        print("Deleted Config")
                        deleted = True
                    except FileNotFoundError:
                        print("Config not found.")
            
            if event.type == pygame.KEYDOWN:
                if active == True:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        if active:
                            active = False
                            written = file_write(old_user_text, written, ip, user_text)
                    else:
                        user_text += event.unicode
                if event.key == pygame.K_ESCAPE:
                    import multiplayer
                    multiplayer.main()

        screen.fill((0,0,0))

        if active:
            color = color_active
        else:
            color = color_passive

        if deleted:
            color_del = color_active
        else:
            color_del = color_passive
            
        pygame.draw.rect(screen,color,input_rect,2)
        pygame.draw.rect(screen,color_del,delete_rect,2)
        
        text_surface = base_font.render(user_text,True,(255,255,255))

        if written and deleted == False:
            written_text_surface = base_font.render("Appended IP Config",True,(255,255,255))

        if deleted:
            written_text_surface = base_font.render("Deleted IP Config",True,(255,255,255))

        screen.blit(written_text_surface,(40,160))
        screen.blit(text_surface,(input_rect.x + 10,input_rect.y + 0))
        screen.blit(ip_text_surface,(40,100))
        screen.blit(delete_text_surface,(40,300))
        screen.blit(hotkey_info_surface,(10,450))

        input_rect.w = max(400,text_surface.get_width() + 10)

        frame += 1
        pygame.display.flip()
        clock.tick(60)
