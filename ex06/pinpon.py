# -*- coding:utf-8 -*-
import pygame
from pygame.locals import *
import sys
import pygame as pg
import os

main_dir = os.path.split(os.path.abspath(__file__))[0]

# ボールの動きを計算
def calc_ball(ball_x, ball_y, ball_vx, ball_vy, bar1_x, bar1_y, bar2_x, bar2_y, ):
    #ball_vx2, ball_vy2, bar1_x, bar1_y, bar2_x, bar2_y, ball_x2, ball_y2):
    
        if ball_x <= bar1_x + 10.:
            if ball_y >= bar1_y - 7.5 and ball_y <= bar1_y + 90.:
                ball_x = 20.
                ball_vx = -ball_vx
        if ball_x >= bar2_x - 15.:
            if ball_y >= bar2_y - 7.5 and ball_y <= bar2_y + 90.:
                ball_x = 1275.
                ball_vx = -ball_vx
        if ball_x < 5.:
            ball_x, ball_y = 600.5, 460.5
        elif ball_x > 1317.5:
            ball_x, ball_y = 600.5, 470.5
        if ball_y <= 10.:
            ball_vy = -ball_vy
            ball_y = 10.
        elif ball_y >= 957.5:
            ball_vy = -ball_vy
            ball_y = 957.5
            
        return ball_x, ball_y, ball_vx, ball_vy #ball_x2, ball_y2, ball_vx2, ball_vy2
    
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

# AIの動きを計算
def calc_ai(ball_x, ball_y, bar2_x, bar2_y):
    dy = ball_y - bar2_y
    if dy > 80: bar2_y += 50
    elif dy > 50: bar2_y += 15
    elif dy > 30: bar2_y += 12
    elif dy > 10: bar2_y += 20
    elif dy < -80: bar2_y -= 50
    elif dy < -50: bar2_y -= 15
    elif dy < -30: bar2_y -= 12
    elif dy < -10: bar2_y -= 20

    if bar2_y >= 950.: bar2_y = 950.
    elif bar2_y <= 10.: bar2_y = 10.
    return bar2_y

# プレイヤーの動き
def calc_player(bar1_y, bar1_dy):
    bar1_y += bar1_dy
    if bar1_y >= 950.: bar1_y = 950.
    elif bar1_y <= 10. : bar1_y = 10.
    return bar1_y

# 得点の計算
def calc_score(ball_x, score1, score2):
    if ball_x < 5.:
        score2 += 1
    if ball_x > 1315.:
        score1 += 1
    return score1, score2

# イベント処理
def event(bar1_dy):
    for event in pygame.event.get():
        if event.type == QUIT:          # 閉じるボタンが押されたら終了
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:       # キーを押したら
            if event.key == K_UP:
                bar1_dy = -10
            elif event.key == K_DOWN:
                bar1_dy = 10
        elif event.type == KEYUP:       # キーを押し終わったら
            if event.key == K_UP:
                bar1_dy = 0.
            elif event.key == K_DOWN:
                bar1_dy = 0.
    return bar1_dy

def main():
    # 各パラメータ
    bar1_x, bar1_y = 10. , 480.
    bar2_x, bar2_y = 1300., 480.
    ball_x, ball_y = 607.5, 432.5
    ball_x2, ball_y2 = 600.0, 400.0
    ball_x3, ball_y3 = 688.0, 388.0
    bar1_dy, bar2_dy = 0. , 0.
    ball_vx, ball_vy = 250., 250.
    ball_vx2, ball_vy2 = 250., 250.
    ball_vx3, ball_vy3 = 250., 250.
    
    score1, score2 = 0,0
    ball_r = 10
    
    if pg.get_sdl_version()[0] == 2:
        pg.mixer.pre_init(44100, 32, 2, 1024)
    pg.init()
    if pg.mixer and not pg.mixer.get_init():
        print("Warning, no sound")
        pg.mixer = None
        
    if pg.mixer:
        music = os.path.join(main_dir, "data", "house_lo.wav")
        pg.mixer.music.load(music)
        pg.mixer.music.play(-1)

    # pygameの設定
    pygame.init()                                       # Pygameの初期化
    screen = pygame.display.set_mode((1320,960),0,32)    # 画面の大きさ
    pygame.display.set_caption("ピンポンゲーム")                  # 画面タイトル
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None,40)                 # 画面文字の設定

    # 背景の設定
    back = pygame.Surface((1320,960))
    background = back.convert()
    screen.fill((176,224,0))

    # ボールを打つバーの設定
    bar = pygame.Surface((10,90))
    bar1 = bar.convert()
    bar1.fill((255,255,255))
    
    bar2 = bar.convert()
    bar2.fill((255,255,255))

    # ボールの設定
    circ_sur = pygame.Surface((20,20))
    pygame.draw.circle(circ_sur,(255,255,255),(ball_r, ball_r), ball_r)
    ball = circ_sur
    ball.set_colorkey((0,0,0))
    
    ball_2 = circ_sur
    ball_2.set_colorkey((0,0,0)) 
    
    ball_3 = circ_sur
    ball_3.set_colorkey((0,100,0))
    
    

    while (1):
        # 各オブジェクトの描画
        screen.blit(background,(0,0))
        pygame.draw.aaline(screen,(255,255,255),(660,5),(660,955))  # 中央線の描画
        screen.blit(bar1,(bar1_x,bar1_y))                           # プレイヤー側バーの描画
        screen.blit(bar2,(bar2_x,bar2_y))                          # CPU側バーの描画
        screen.blit(ball,(ball_x, ball_y)) # ボールの描画
        screen.blit(ball_2,(ball_x2, ball_y2))
        screen.blit(ball_3,(ball_x3, ball_y3))
        screen.blit(font.render(str(score1), True,(255,255,255)),(250.,10.))
        screen.blit(font.render(str(score2), True,(255,255,255)),(400.,10.))

        # プレイヤー側バーの位置
        bar1_dy = event(bar1_dy)
        bar1_y = calc_player(bar1_y,bar1_dy)

        # ボールの移動
        time_passed = clock.tick(70)
        time_sec = time_passed / 900.0
        time_sec2 = time_passed / 700.0
        time_sec3 = time_passed / 600.0
        ball_x += ball_vx * time_sec
        ball_y += ball_vy * time_sec
        
        ball_x2 += ball_vx2 * time_sec2
        ball_y2 += ball_vy2 * time_sec3
        
        ball_x3 += ball_vx3 * time_sec3
        ball_y3 += ball_vy3 * time_sec2
        

        # 得点の計算
        score1, score2 = calc_score(ball_x, score1, score2)
        score1, score2 = calc_score(ball_x2, score1, score2)
        score1, score2 = calc_score(ball_x3, score1, score2)
        

        # CPUのバー速度を計算
        bar2_y = calc_ai(ball_x, ball_y, bar2_x, bar2_y)

        # ボールの速度・位置を計算
        ball_x, ball_y, ball_vx, ball_vy = calc_ball(ball_x, ball_y, ball_vx, ball_vy, bar1_x, bar1_y, bar2_x, bar2_y )
        ball_x2, ball_y2, ball_vx2, ball_vy2 = calc_ball(ball_x2, ball_y2, ball_vx2, ball_vy2, bar1_x, bar1_y, bar2_x, bar2_y )
        ball_x3, ball_y3, ball_vx3, ball_vy3 = calc_ball(ball_x3, ball_y3, ball_vx3, ball_vy3, bar1_x, bar1_y, bar2_x, bar2_y )
        pygame.display.update()                                     # 画面を更新


if __name__ == "__main__":
    main()