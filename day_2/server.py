import socket, pygame, pickle, pygame.gfxdraw
pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('server')
mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 1000
while True:
    try:
        mysocket.bind((socket.gethostname(), port))
        break
    except:
        port += 1
print(f'hosting server on {socket.gethostname()}:{port}')
def player(pos, color):
    x1, y1 = pos
    x2 = x1+10
    y2 = y1
    x3 = x1+10
    y3 = y1+10
    x4 = x1
    y4 = y1+10
    pygame.gfxdraw.filled_polygon(screen, [(x1, y1), (x2, y2), (x3, y3), (x4, y4)], color)
player1 = (0, 0)
up, down, left, right = False, False, False, False
running = True
while running:
    # socket actions here
    mysocket.listen()
    client, address = mysocket.accept()
    while True:
        try:
            player2 = pickle.loads(client.recv(1024))
            client.send(pickle.dumps(player1))
            if player2 == 'stop':
                break
        except:
            break
        # pygame actions here
        try:
            screen.fill(0)
            player(player1, (0, 255, 0))
            player(player2, (0, 0, 255))
            pygame.display.flip()
        except:
            pass
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    up = True
                if event.key == pygame.K_DOWN:
                    down = True
                if event.key == pygame.K_LEFT:
                    left = True
                if event.key == pygame.K_RIGHT:
                    right = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    up = False
                if event.key == pygame.K_DOWN:
                    down = False
                if event.key == pygame.K_LEFT:
                    left = False
                if event.key == pygame.K_RIGHT:
                    right = False
        if up:
            ychange = -1
        elif down:
            ychange = 1
        else:
            ychange = 0
        if left:
            xchange = -1
        elif right:
            xchange = 1
        else:
            xchange = 0
        x, y = player1
        x += xchange
        y += ychange
        player1 =(x, y)
    print('connection lost')
mysocket.close()
