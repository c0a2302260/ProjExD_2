import os
import random
import sys
import pygame as pg
import time


WIDTH, HEIGHT = 1600, 900
mv_dict = { #移動量辞書 (押下キー : 移動量タプル)
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, 5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(5, 0)
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct:pg.Rect) -> tuple[bool, bool]:
    """
    こうかとんRect、または、爆弾Rectの画面内外判定用の関数
    引数：こうかとんRect、または、爆弾Rect
    戻り値：横方向判定結果、縦方向判定結果(True：画面内/False：画面外)
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)

    kk_sad_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.0)
    gameover_img = pg.Surface((WIDTH, HEIGHT))
    gameover_img.set_alpha(200)

    fonto = pg.font.Font(None, 80)
    gameover_txt = fonto.render("Game Over", True, (255, 255, 255))
    gameover_txt_rct = gameover_txt.get_rect()
    gameover_txt_rct.center = WIDTH/2, HEIGHT/2

    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    clock = pg.time.Clock()
    tmr = 0
    vx, vy = 5, 5

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        screen.blit(bg_img, [0, 0])

        if kk_rct.colliderect(bb_rct):
            # こうかとんと爆弾の衝突判定
            screen.blit(gameover_img, [0, 0])
            screen.blit(gameover_txt, gameover_txt_rct)
            screen.blit(kk_sad_img, [WIDTH/2+200, HEIGHT/2-70])
            screen.blit(kk_sad_img, [WIDTH/2-280, HEIGHT/2-70])
            pg.display.update()
            time.sleep(5)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for k, v in mv_dict.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            # こうかとんと壁の衝突判定
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        yoko, tate = check_bound(bb_rct)
        # 爆弾と壁の衝突判定
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        bb_rct.move_ip(vx, vy)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()