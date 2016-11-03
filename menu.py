from libreria import *

if not pygame.display.get_init():
    pygame.display.init()

if not pygame.font.get_init():
    pygame.font.init()


if __name__ == "__main__":
    import sys
    surface = pygame.display.set_mode((854,480)) #0,6671875 and 0,(6) of HD resoultion
    surface.fill((51,51,51))
    menu = Menu()
    menu.set_fontsize(64)
    menu.init(['Start','Quit'], surface)
    menu.draw()
    pygame.key.set_repeat(199,69)
    pygame.display.update()
    while 1:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    menu.draw(-1)
                if event.key == K_DOWN:
                    menu.draw(1)
                if event.key == K_RETURN:
                    if menu.get_position() == 0:
                        print "sisas"
                    if menu.get_position() == 1:
                        pygame.display.quit()
                        sys.exit()
                if event.key == K_ESCAPE:
                    pygame.display.quit()
                    sys.exit()
                pygame.display.update()
            elif event.type == QUIT:
                pygame.display.quit()
                sys.exit()
        pygame.time.wait(8)
