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
    images = [pygame.image.load("/imagenes/cesped.jpeg").convert(),pygame.image.load("/imagenes/muro.jpeg").convert()]
    interprete = ConfigParser.ConfigParser()
    interprete.read(archivo)
    try:
        mapa = interprete.get("map", "mapa").split("\n")
    except:
        print("Error en la lectura de la seccion")
        sys.exit(0)
    try:
        for ey, punto in enumerate(mapa):
            for ex,cd in enumerate(punto):
                if((interprete.get(cd, "muro") == "no") and (interprete.get(cd, "bloqueo") == "no") and (interprete.get(cd, "puerta") == "no")):
                    m = Elemento(ex*25,ey*25, images[0])
                    m.image=images[0]
                    m.tipo=interprete.get(cd, "nombre")
                    m.bloqueo = interprete.get(cd, "bloqueo")
                    m.update_rect(ex*25,ey*25)
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


class Juego:
    
