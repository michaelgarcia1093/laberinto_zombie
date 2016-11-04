try:
    import pygame,sys,random,threading,time,ConfigParser
    from pygame.locals import *
except (KeyboardInterrupt, SystemExit):
    raise
except:
    raise


def checkCollision(sprite1, sprite2):
    col = pygame.sprite.collide_rect(sprite1, sprite2)
    if col == True:
        return True
    else:
        return False

def cargar_fondo(archivo, ancho, alto, sin_canal=False):
    if(not sin_canal):
        imagen = pygame.image.load(archivo).convert_alpha()
    else:
        imagen = pygame.image.load(archivo)
    imagen_ancho, imagen_alto = imagen.get_size()
    tabla_fondos = []
    for fondo_x in range(0, imagen_ancho/ancho):
       linea = []
       tabla_fondos.append(linea)
       for fondo_y in range(0, imagen_alto/alto):
            cuadro = (fondo_x * ancho, fondo_y * alto, ancho, alto)
            linea.append(imagen.subsurface(cuadro))
    return tabla_fondos

def playsound(filez):
    pygame.mixer.init()
    pygame.mixer.music.load(filez)
    pygame.mixer.music.play(0,0)

class Elemento(pygame.sprite.Sprite):
    def __init__(self, x, y, archivo):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(archivo).convert()
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.contdin = 0
        self.bloqueo = "no"
        self.tipo = "ninguno"

    def update_rect(self,x,y):
        self.rect = self.image.get_rect()
        self.rect.x= x
        self.rect.y= y

def dibujarmapa(archivo):
    global images
    images = ["archivos/imagenes/cesped.jpeg","archivos/imagenes/muro.jpeg", "archivos/imagenes/puerta.png","archivos/imagenes/boss_1.png" ]
    interprete = ConfigParser.ConfigParser()
    interprete.read(archivo)
    try:
        mapa = interprete.get("map", "mapa").split("\n")
    except:
        print("Error en la lectura de la seccion")
        sys.exit(0)
    for ey, punto in enumerate(mapa):
        for ex,cd in enumerate(punto):
            if((interprete.get(cd, "muro") == "no") and (interprete.get(cd, "bloqueo") == "no") and (interprete.get(cd, "puerta") == "no")):
                m = Elemento(ex*25,ey*25, images[0])
                m.tipo=interprete.get(cd, "nombre")
                m.bloqueo = interprete.get(cd, "bloqueo")
                m.update_rect(ex*25,ey*25)
                ls_elementos.add(m)
                ls_todos.add(m)

            if((interprete.get(cd, "muro") == "si") and (interprete.get(cd, "bloqueo") == "si") and (interprete.get(cd, "puerta") == "no")):
                m = Elemento(ex*25,ey*25, images[1])
                m.tipo=interprete.get(cd, "nombre")
                m.bloqueo = interprete.get(cd, "bloqueo")
                m.update_rect(ex*25,ey*25)
                ls_muros.add(m)
                ls_elementos.add(m)
                ls_todos.add(m)

            if((interprete.get(cd, "muro") == "no") and (interprete.get(cd, "bloqueo") == "no") and (interprete.get(cd, "puerta") == "si")):
                m = Elemento(ex*25,ey*25, images[2])
                m.tipo=interprete.get(cd, "nombre")
                m.bloqueo = interprete.get(cd, "bloqueo")
                m.update_rect(ex*25,ey*25)
                ls_elementos.add(m)
                ls_todos.add(m)

            if((interprete.get(cd, "boss1") == "si")):
                m = Elemento(ex*25,ey*25, images[3])
                m.tipo=interprete.get(cd, "nombre")
                m.bloqueo = interprete.get(cd, "bloqueo")
                m.update_rect(ex*25,ey*25)
                #ls_muros.add(m)
                ls_elementos.add(m)
                ls_todos.add(m)
class Menu:
    lista = []
    pola = []
    rozmiar_fontu = 32
    font_path = 'data/coders_crux/coders_crux.ttf'
    font = pygame.font.Font
    dest_surface = pygame.Surface
    ilosc_pol = 0
    kolor_tla = (51,51,51)
    kolor_tekstu =  (255, 255, 153)
    kolor_zaznaczenia = (153,102,255)
    pozycja_zaznaczenia = 0
    pozycja_wklejenia = (0,0)
    menu_width = 0
    menu_height = 0

    class Pole:
        tekst = ''
        pole = pygame.Surface
        pole_rect = pygame.Rect
        zaznaczenie_rect = pygame.Rect

    def move_menu(self, top, left):
        self.pozycja_wklejenia = (top,left)

    def set_colors(self, text, selection, background):
        self.kolor_tla = background
        self.kolor_tekstu =  text
        self.kolor_zaznaczenia = selection

    def set_fontsize(self,font_size):
        self.rozmiar_fontu = font_size

    def set_font(self, path):
        self.font_path = path

    def get_position(self):
        return self.pozycja_zaznaczenia

    def init(self, lista, dest_surface):
        self.lista = lista
        self.dest_surface = dest_surface
        self.ilosc_pol = len(self.lista)
        self.stworz_strukture()

    def draw(self,przesun=0):
        if przesun:
            self.pozycja_zaznaczenia += przesun
            if self.pozycja_zaznaczenia == -1:
                self.pozycja_zaznaczenia = self.ilosc_pol - 1
            self.pozycja_zaznaczenia %= self.ilosc_pol
        menu = pygame.Surface((self.menu_width, self.menu_height))
        menu.fill(self.kolor_tla)
        zaznaczenie_rect = self.pola[self.pozycja_zaznaczenia].zaznaczenie_rect
        pygame.draw.rect(menu,self.kolor_zaznaczenia,zaznaczenie_rect)

        for i in xrange(self.ilosc_pol):
            menu.blit(self.pola[i].pole,self.pola[i].pole_rect)
        self.dest_surface.blit(menu,self.pozycja_wklejenia)
        return self.pozycja_zaznaczenia

    def stworz_strukture(self):
        przesuniecie = 0
        self.menu_height = 0
        self.font = pygame.font.Font(self.font_path, self.rozmiar_fontu)
        for i in xrange(self.ilosc_pol):
            self.pola.append(self.Pole())
            self.pola[i].tekst = self.lista[i]
            self.pola[i].pole = self.font.render(self.pola[i].tekst, 1, self.kolor_tekstu)

            self.pola[i].pole_rect = self.pola[i].pole.get_rect()
            przesuniecie = int(self.rozmiar_fontu * 0.2)

            height = self.pola[i].pole_rect.height
            self.pola[i].pole_rect.left = przesuniecie
            self.pola[i].pole_rect.top = przesuniecie+(przesuniecie*2+height)*i

            width = self.pola[i].pole_rect.width+przesuniecie*2
            height = self.pola[i].pole_rect.height+przesuniecie*2
            left = self.pola[i].pole_rect.left-przesuniecie
            top = self.pola[i].pole_rect.top-przesuniecie

            self.pola[i].zaznaczenie_rect = (left,top ,width, height)
            if width > self.menu_width:
                    self.menu_width = width
            self.menu_height += height
        x = self.dest_surface.get_rect().centerx - self.menu_width / 2
        y = self.dest_surface.get_rect().centery - self.menu_height / 2
        mx, my = self.pozycja_wklejenia
        self.pozycja_wklejenia = (x+mx, y+my)

class Jugador(pygame.sprite.Sprite):

    # Atributos
    paredes=None
    elementos=None
    image_arriba = []
    image_abajo =  []
    image_derecha = []
    image_izquierda=[]

    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)

        matrizimg = cargar_fondo("archivos/imagenes/heroe.png", 23,23)
        for i in xrange(3):
            self.image_abajo.append(matrizimg[i][0])
        for i in xrange(3):
            self.image_izquierda.append(matrizimg[i][1])
        for i in xrange(3):
            self.image_derecha.append(matrizimg[i][2])
        for i in xrange(3):
            self.image_arriba.append(matrizimg[i][3])

        self.increment_x, self.increment_y = 1,1
        self.image = self.image_arriba[2]
        self.direccion = "arriba"
    	self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.vida = 100
        self.cont = 0
        self.llaves = 0

    # Control del movimiento
    def ir_arr(self):
        self.direccion = "arriba"
        if(self.cont<2):
            self.cont+=1
        else:
            self.cont=0

        self.image=self.image_arriba[self.cont]
        self.rect.y -= self.increment_y

    def ir_abaj(self):
        """ Usuario pulsa flecha izquierda """
        self.direccion = "abajo"
        if(self.cont<2):
            self.cont+=1
        else:
            self.cont=0

        self.image=self.image_abajo[self.cont]
        self.rect.y += self.increment_y

    def ir_izq(self):
        """ Usuario pulsa flecha izquierda """
        self.direccion = "izquierda"
        if(self.cont<2):
            self.cont+=1
        else:
            self.cont=0
        self.image=self.image_izquierda[self.cont]
        self.rect.x -= self.increment_x

    def ir_der(self):
        """ Usuario pulsa flecha derecha """
        self.direccion = "derecha"
        if(self.cont<2):
            self.cont+=1
        else:
            self.cont=0
        self.image=self.image_derecha[self.cont]
        self.rect.x += self.increment_x

    def no_mover(self):
        """ Usuario no pulsa teclas """
        self.vel_x = 0

    def update(self):
        ls_choque=pygame.sprite.spritecollide(self, self.paredes, False)
        for muro in ls_choque:
            if(muro.bloqueo == "si"):
                if self.direccion == "derecha":
                   self.rect.right=muro.rect.left
                else:
                    if self.direccion == "izquierda":
                        self.rect.left=muro.rect.right
                    else:
                        if self.direccion == "arriba":
                            self.rect.top=muro.rect.bottom
                        else:
                            if self.direccion == "abajo":
                                self.rect.bottom=muro.rect.top

class Enemigo(pygame.sprite.Sprite):
    paredes=None
    elementos=None
    image_arriba = []
    image_abajo =  []
    image_derecha = []
    image_izquierda=[]

    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("archivos/imagenes/en.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.direccion="arriba"
        self.cont = 1 #Control de velocidad para los enemigos
        self.vida = 100
        self.flag = True
        self.cont_disparos = 0 #Control de los disparos

    def update_probabilidad(self):
        self.probabilidad = random.randrange(0,100)

    def get_direccion(self):
        flagd=False
        flagi=False
        save = (self.rect.x,self.rect.y)

        for muro in self.paredes:
            self.rect.x+=20
            if(checkCollision(self,muro)):
                flagd = True
                print "Con derecha"
            self.rect.x-=40
            if(checkCollision(self,muro)):
                flagi = True
                print "Con izquierda"
        self.rect.x, self.rect.y = save[0],save[1]
        if(not(flagd and flagi)):
            self.direccion = "arriba"

    def update(self):

        if(self.cont == 0):
            self.cont += 1
            """self.update_probabilidad()
            if(self.probabilidad > 0 and self.probabilidad < 50):
                self.direccion = "derecha"
            else:
                self.direccion = "arriba"""

            ls_choque=pygame.sprite.spritecollide(self, self.paredes, False)
            for muro in ls_choque:
                if(muro.bloqueo == "si"):
                    if self.direccion == "derecha":
                       self.rect.right=muro.rect.left
                       self.direccion = "izquierda"
                    else:
                        if self.direccion == "izquierda":
                            self.rect.left=muro.rect.right
                            self.direccion = "derecha"
                        else:
                            if self.direccion == "arriba":
                                self.rect.bottom=muro.rect.top
                                self.direccion = "abajo"
                            else:
                                if self.direccion == "abajo":
                                    self.rect.top=muro.rect.bottom
                                    self.direccion = "arriba"

            if(self.direccion=="derecha"):
                self.rect.x+=1
            if(self.direccion=="izquierda"):
                self.rect.x-=1
            if(self.direccion == "arriba"):
                self.rect.y+=1
            if(self.direccion == "abajo"):
                self.rect.y-=1
        else:
            if(self.cont >= 5):
                self.cont = 0
            else:
                self.cont += 1

        if(self.cont_disparos == 0):
            self.cont_disparos+=1
            b = Bullet("archivos/imagenes/bala_e.png", self.rect.x, self.rect.y, self.direccion)
            ls_balas_e.add(b)
            ls_todos.add(b)
        else:
            if(self.cont_disparos > 500):
                self.cont_disparos=0
            else:
                self.cont_disparos+=1

class Bullet(pygame.sprite.Sprite): #Hereda de la clase sprite

    def __init__(self, img_name, x,y, direccion): #img para cargar, y su padre(de donde debe salir la bala)
    	pygame.sprite.Sprite.__init__(self)
    	self.image = pygame.image.load(img_name).convert_alpha()
    	self.rect = self.image.get_rect()
    	self.rect.x = x
    	self.rect.y = y
        self.speed = 1
        self.direccion = direccion
    def update(self):

        if(self.direccion == "derecha"): #derecha
            self.rect.x += self.speed
        if(self.direccion == "izquierda"):#izquierda
            self.rect.x -= self.speed
        if(self.direccion == "arriba"):#arriba
            self.rect.y -= self.speed
        if(self.direccion == "abajo"):#abajo
            self.rect.y += self.speed

class Juego:
    nivel=0
    surface=None

    def __init__(self,nivel,surface):
        self.nivel = nivel
        self.surface = surface

    def historia(self):
        print "historia"

    def nivel1(self):
        global ANCHO,ALTO,pantalla,jugador,ls_todos,sub,tipo,ls_balas_boss,ls_muros,ls_elementos,ls_enemigos,ls_balas_e
        c_fondo = (255,0,0)
        ALTO = 600
        ANCHO = 800
        global vxi,vyi
        vxi=25
        vyi=25
        pygame.init()
        pantalla = pygame.display.set_mode((ANCHO, ALTO+30))
        pygame.display.set_caption(" El laberinto de la muerte lvl 2 - [v1] ", 'Spine Runtime')
        pantalla.fill(c_fondo)
        sub = pantalla.subsurface([0,ALTO, ANCHO, 30]) #Dibuja una surface sobre la pantalla
        tipo = pygame.font.SysFont("monospace", 15)
        tipo.set_bold(True)
        sub.fill((0,0,0))

        ls_enemigos=pygame.sprite.Group()
        ls_todos=pygame.sprite.Group()
        ls_muros=pygame.sprite.Group()
        ls_elementos=pygame.sprite.Group()
        ls_jugador=pygame.sprite.Group()
        ls_bajasj = pygame.sprite.Group()
        ls_balas_e = pygame.sprite.Group()
        terminar=False
        muerto = False

        m = dibujarmapa("mapeo.config")
        print ls_muros
        jugador = Jugador(80, 55)
        jugador.paredes = ls_muros
        ls_jugador.add(jugador)
        ls_todos.add(jugador)

        pos_en = [(190, 50),(730,554),(362,485),(534,309),(180,560),(414,425)]
        dir_en = ["izquierda","arriba","arriba","arriba","arriba","izquierda"]
        for i in range(len(pos_en)):
            en = Enemigo(pos_en[i][0],pos_en[i][1])
            en.paredes = ls_muros
            en.direccion = dir_en[i]
            ls_todos.add(en)
            ls_enemigos.add(en)

        while not terminar:
        
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    terminar=True
                    salir=True

                elif event.type==pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        terminar=True
                        salir=True
                    if event.key == pygame.K_n:
                        self.historia()

                    if event.key == pygame.K_SPACE:
                        b = Bullet("archivos/imagenes/bala_j.png", jugador.rect.x, jugador.rect.y, jugador.direccion)
                        ls_bajasj.add(b)
                        ls_todos.add(b)

            T=pygame.key.get_pressed()

            if T[pygame.K_LEFT]:
                jugador.update()
                jugador.ir_izq()

            if T[pygame.K_RIGHT]:
                jugador.update()
                jugador.ir_der()

            if T[pygame.K_UP]:
                jugador.update()
                jugador.ir_arr()

            if T[pygame.K_DOWN]:
                jugador.update()
                jugador.ir_abaj()


            """ZONA DE COLLIDES"""
            for b_j in ls_bajasj:
                for muro in ls_muros:
                    if(checkCollision(b_j,muro)):
                        ls_bajasj.remove(b_j)
                        ls_todos.remove(b_j)
                for enemigo in ls_enemigos:
                    if(checkCollision(b_j,enemigo)):
                        ls_bajasj.remove(b_j)
                        ls_todos.remove(b_j)
                        enemigo.vida -= random.randrange(10,20)
                    if(enemigo.vida <= 0 ):
                        ls_todos.remove(enemigo)
                        ls_enemigos.remove(enemigo)
                for b_e in ls_balas_e:
                    if(checkCollision(b_j,b_e)):
                        ls_bajasj.remove(b_j)
                        ls_todos.remove(b_j)
                        ls_balas_e.remove(b_e)
                        ls_todos.remove(b_e)

            for b_e in ls_balas_e:
                for muro in ls_muros:
                    if(checkCollision(b_e,muro)):
                        ls_balas_e.remove(b_e)
                        ls_todos.remove(b_e)
                if(checkCollision(jugador,b_e)):
                    jugador.vida -= random.randrange(10,20)



            """FIN ZONA DE COLLIDES"""
            ls_todos.update()
            ls_enemigos.update()
            ls_jugador.update()
            ls_todos.draw(pantalla)
            ls_elementos.draw(pantalla)
            ls_bajasj.draw(pantalla)
            ls_balas_e.draw(pantalla)
            ls_enemigos.draw(pantalla)
            ls_jugador.draw(pantalla)
            pygame.display.flip()
