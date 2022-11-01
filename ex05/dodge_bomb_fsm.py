import pygame as pg
import sys
import os
from random import randint

main_dir = os.path.split(os.path.abspath(__file__))[0]
time = 0
class Screen:
    def __init__(self, title, wh, bgimg):
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(wh)
        self.rct = self.sfc.get_rect()
        bgi_sfc = pg.image.load(bgimg)
        bgi_rct = bg_sfc.get_rect()
        

class Bird:
    def __init__(self, img, zoom, xy):
        tori_sfc = pg.image.load("fig/6.png")
        tori_sfc = pg.transform.rotozoom(tori_sfc, 0, 2.0)
        tori_rct = tori_sfc.get_rect()
        tori_rct.center = 900, 400


key_delta = {
    pg.K_UP:    [0, -1],
    pg.K_DOWN:  [0, +1],
    pg.K_LEFT:  [-1, 0],
    pg.K_RIGHT: [+1, 0],
}


def check_bound(obj_rct, scr_rct):
    """
    obj_rct：こうかとんrct，または，爆弾rct
    scr_rct：スクリーンrct
    領域内：+1／領域外：-1
    """
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right: 
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom: 
        tate = -1
    return yoko, tate

#音楽

def load_sound(file):
    """because pygame can be be compiled without mixer."""
    if not pg.mixer:
        return None
    file = os.path.join(main_dir, "data", file)
    try:
        sound = pg.mixer.Sound(file)
        return sound
    except pg.error:
        print("Warning, unable to load, %s" % file)
    return None

def load_image(file):
    """loads an image, prepares it for play"""
    try:
        surface = pg.image.load(file)
    except pg.error:
        raise SystemExit('Could not load image "%s" %s' % (file, pg.get_error()))
    return surface#.convert()

class Bomb(pg.sprite.Sprite):
    """A bomb the aliens drop."""

    speed = 5
    images = []

    def __init__(self):
        self.image = load_image("fig/rocket.png")
        self.rect = self.image.get_rect()

    def update(self):
        """called every time around the game loop.

        Every frame we move the sprite 'rect' down.
        When it reaches the bottom we:

        - make an explosion.
        - remove the Bomb.
        """
        self.rect.move_ip(1, self.speed)
        #if self.rect.bottom >= 470:
            #Explosion(self)
            #self.kill()
            
class Explosion(pg.sprite.Sprite):
    """An explosion. Hopefully the Alien and not the player!"""

    defaultlife = 12
    animcycle = 3
    images = []

    def __init__(self, actor):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=actor.rect.center)
        self.life = self.defaultlife

    def update(self):
        """called every time around the game loop.

        Show the explosion surface for 'defaultlife'.
        Every game tick(update), we decrease the 'life'.

        Also we animate the explosion.
        """
        self.life = self.life - 1
        self.image = self.images[self.life // self.animcycle % 2]
        if self.life <= 0:
            self.kill()

def main():
    
    yama = pg.time.get_ticks()
    tato = Bomb()
    
    # 練習1
    #scr = Screen("fig/pg_bg.jpg", (1600, 900), "逃げろ！こうかとん！")
    pg.display.set_caption("逃げろ！こうかとん")
    scrn_sfc = pg.display.set_mode((1600, 900))
    scrn_rct = scrn_sfc.get_rect()
    bg_sfc = pg.image.load("fig/P11.jpg")
    bg_rct = bg_sfc.get_rect()

    # 練習3
    tori_sfc = pg.image.load("fig/6.png")
    tori_sfc = pg.transform.rotozoom(tori_sfc, 0, 2.0)
    tori_rct = tori_sfc.get_rect()
    tori_rct.center = 900, 400

    # 練習5
    bomb_sfc = pg.Surface((20, 20)) # 空のSurface
    bomb_sfc.set_colorkey((0, 0, 0)) # 四隅の黒い部分を透過させる
    pg.draw.circle(bomb_sfc, (255, 0, 0), (10, 10), 10) # 爆弾用の円を描く
    bomb_rct = bomb_sfc.get_rect()
    bomb_rct.centerx = randint(0, scrn_rct.width)
    bomb_rct.centery = randint(0, scrn_rct.height)
    vx, vy = +1, +1 # 練習6
    
    # 音楽
    boom_sound = load_sound("boom.wav")
    shoot_sound = load_sound("car_door.wav")
    if pg.mixer:
        music = os.path.join(main_dir, "data", "boom.wav")
        pg.mixer.music.load(music)
        pg.mixer.music.play(-1)
    
    #爆弾
    img = load_image("data/explosion1.gif")
    Explosion.images = [img, pg.transform.flip(img, 1, 1)]
    
    

    clock = pg.time.Clock() # 練習1
    while True:
        scrn_sfc.blit(bg_sfc, bg_rct) # 練習2
        
        for event in pg.event.get(): # 練習2
            if event.type == pg.QUIT:
                return

        key_states = pg.key.get_pressed()
        for key, delta in key_delta.items():
            if key_states[key]:
                tori_rct.centerx += delta[0]
                tori_rct.centery += delta[1]
                # 練習7
                if check_bound(tori_rct, scrn_rct) != (+1, +1):
                    tori_rct.centerx -= delta[0]
                    tori_rct.centery -= delta[1]
        scrn_sfc.blit(tori_sfc, tori_rct) # 練習3
        
        #yama - pg.time.get_ticks()) <= 1000:
        #    Bomb()
        
        scrn_sfc.blit(tato.image, tato.rect)
        tato.update()

        # 練習7
        yoko, tate = check_bound(bomb_rct, scrn_rct)
        vx *= yoko
        vy *= tate
        bomb_rct.move_ip(vx, vy) # 練習6
        scrn_sfc.blit(bomb_sfc, bomb_rct) # 練習5

        # 練習8
        if tori_rct.colliderect(bomb_rct): # こうかとんrctが爆弾rctと重なったら
            return

        pg.display.update() #練習2
        clock.tick(1000)


if __name__ == "__main__":
    pg.init() # 初期化
    main()    # ゲームの本体
    pg.quit() # 初期化の解除
    sys.exit()
