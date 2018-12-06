import random
import json
import os
import time

from pico2d import *

import game_framework
import main_state
import main_state2

name = "MainState"
boy = None
grass = None
windcursor = None
font = None
money=None
global confirm,expedition,start_time,expedition_time
expedition=0
confirm=0
start_time=0
expedition_time=10
class Expedition_Confirm:
    image = None
    def __init__(self):
        self.frame = 0
        self.image2 = load_image('Chicken2.png')
        self.image3 = load_image('swallow_ch.png')
        self.font = load_font('Gungsuh.TTF', 30)
        if Expedition_Confirm.image == None:
            self.image = load_image('expedition.png')

    def update(self):
        global confirm
        if confirm == 1:
            if main_state.mx >= 246 and main_state.mx <= 354 and main_state.my >= 106 and main_state.my <= 175:
                confirm = 0
            if main_state.mx >= 383 and main_state.mx <= 559 and main_state.my >= 106 and main_state.my <= 175:

                main_state.start_time = get_time()
                main_state.my = -1
                main_state.mx = -1
                main_state.cagebird[1].expedition = 1
                confirm = 0
        if confirm == 2:
            if main_state.mx >= 246 and main_state.mx <= 354 and main_state.my >= 106 and main_state.my <= 175:
                confirm = 0
            if main_state.mx >= 383 and main_state.mx <= 559 and main_state.my >= 106 and main_state.my <= 175:

                main_state.start_time = get_time()
                main_state.my = -1
                main_state.mx = -1
                main_state.cagebird[2].expedition = 1
                confirm = 0

    def draw(self):
        if confirm==1 and main_state.cagebird[1].name==1:
            self.image.clip_draw(0, 0, 800, 600,400 ,300)
            self.image2.clip_draw(0, 0, 210, 164, 400, 370, 200, 200)
            self.font.draw(290, 260, '상처입은 닭둘기', (255, 255, 255))
        elif confirm==1 and main_state.cagebird[1].name==2:
            self.image.clip_draw(0, 0, 800, 600,400 ,300)
            self.image3.clip_draw(0, 0, 522, 273, 400, 370, 200, 200)
            self.font.draw(290, 260, '상처입은 제비', (255, 255, 255))

        if confirm==2 and main_state.cagebird[2].name==1:
            self.image.clip_draw(0, 0, 800, 600,400 ,300)
            self.image2.clip_draw(0, 0, 210, 164, 400, 370, 200, 200)
            self.font.draw(290, 260, '상처입은 닭둘기', (255, 255, 255))
        elif confirm==2 and main_state.cagebird[2].name==2:
            self.image.clip_draw(0, 0, 800, 600,400 ,300)
            self.image3.clip_draw(0, 0, 522, 273, 400, 370, 200, 200)
            self.font.draw(290, 260, '상처입은 제비', (255, 255, 255))
class Main_Background:
    image = None
    def __init__(self):
        if Main_Background.image==None:
            self.image = load_image('cage.png')
        self.y = 300
        self.x = 400
    def draw(self):
        self.image.clip_draw(0, 0, 800, 600, self.x,self.y,)
        main_state.main_ui.image2.clip_draw(0, 0, 32 * main_state.main_ui.exp, 84, 58 + 6 * main_state.main_ui.exp, 572, 13 * main_state.main_ui.exp, 34)
class Expeditioning:
    image = None
    def __init__(self):
        if Expeditioning.image==None:
            self.image = load_image('expeditioning.png')
    def draw(self):
        if main_state.cagebird[1].expeditioning== 1 or main_state.cagebird[1].expedition==1:
            self.image.clip_draw(0, 0, 300, 300,170 ,458)
        if main_state.cagebird[2].expeditioning== 1 or main_state.cagebird[2].expedition==1:
            self.image.clip_draw(0, 0, 300, 300,470 ,458)
class Draw_bird:

    def __init__(self):
        self.image = load_image('Chicken2.png')
        self.image2 = load_image('swallow_ch.png')
        self.font = load_font('Gungsuh.TTF', 20)
    def update(self):
        global confirm
        if main_state.mx >= 252 and main_state.mx <= 390 and main_state.my <= 420 and main_state.my >= 380:
            confirm = 1
        if main_state.mx >= 552 and main_state.mx <= 690 and main_state.my <= 420 and main_state.my >= 380:
            confirm=2

    def draw(self):
        if main_state.cagebird[1].name==1:
            self.image.clip_draw(0, 0, 210, 164, 162,440,60,60)
            self.font.draw(220,463, '상처입은 닭둘기', (255, 255, 255))
            self.font.draw(220, 440, '체력: %d'%main_state.cagebird[1].hp, (255, 255, 255))
            self.font.draw(300, 440, '기력: %d' % main_state.cagebird[1].sp, (255, 255, 255))
        if main_state.cagebird[1].name==2:
            self.image2.clip_draw(0, 0, 522, 273, 162,440,60,60)
            self.font.draw(220,463, '상처입은 제비', (255, 255, 255))
            self.font.draw(220, 440, '체력: %d'%main_state.cagebird[1].hp, (255, 255, 255))
            self.font.draw(300, 440, '기력: %d' % main_state.cagebird[1].sp, (255, 255, 255))
        if main_state.cagebird[2].name==1:
            self.image.clip_draw(0, 0, 210, 164, 462,440,60,60)
            self.font.draw(520,463, '상처입은 닭둘기', (255, 255, 255))
            self.font.draw(520, 440, '체력: %d'%main_state.cagebird[2].hp, (255, 255, 255))
            self.font.draw(600, 440, '기력: %d' % main_state.cagebird[2].sp, (255, 255, 255))
        if main_state.cagebird[2].name==2:
            self.image2.clip_draw(0, 0, 522, 273, 462,440,60,60)
            self.font.draw(520,463, '상처입은 제비', (255, 255, 255))
            self.font.draw(520, 440, '체력: %d'%main_state.cagebird[2].hp, (255, 255, 255))
            self.font.draw(600, 440, '기력: %d' % main_state.cagebird[2].sp, (255, 255, 255))
class expedition_success:
    image = None
    def __init__(self):
        self.frame = 0
        if expedition_success.image == None:
            self.image = load_image('success.png')

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, 800, 600,400 ,300)
class Windcursor:
    image = None
    def __init__(self):
        self.frame = 0
        if Windcursor.image == None:
            self.image = load_image('cursor.png')

    def update(self):
        self.frame = (self.frame + 1) % 13


    def draw(self):
            self.image.clip_draw(self.frame * 30, 0, 30, 45, main_state.movemx, main_state.movemy)

class Money:
    image1=None
    def __init__(self):
        self.x, self.y = 0, 90
        self.frame = 0
        if Money.image1==None:
            self.image1 = load_image('0_9.png')

    def update(self):
        pass

    def draw(self):
        self.image1.clip_draw(((main_state.playermoney % 10) + 1) * 97, 0, 97, 145, 744, 572, 17, 28)
        self.image1.clip_draw((((main_state.playermoney % 100) // 10) + 1) * 97, 0, 97, 145, 700, 572, 17, 28)
        self.image1.clip_draw((((main_state.playermoney % 1000) // 100) + 1) * 97, 0, 97, 145, 654, 572, 17, 28)
        self.image1.clip_draw((((main_state.playermoney % 10000) // 1000) + 1) * 97, 0, 97, 145, 638, 572, 17, 28)
        self.image1.clip_draw((((main_state.playermoney % 100000) // 10000) + 1) * 97, 0, 97, 145, 622, 572, 17, 28)
        self.image1.clip_draw((((main_state.playermoney % 1000000) // 100000) + 1) * 97, 0, 97, 145, 606, 572, 17, 28)
        self.image1.clip_draw((((main_state.playermoney % 10000000) // 1000000) + 1) * 97, 0, 97, 145, 590, 572, 17, 28)

class Main_UI:
    def __init__(self):
        self.image = load_image('main_ui.png')
        self.y = 300
        self.x = 400
    def draw(self):
        self.image.clip_draw(0, 0, 800, 600, self.x,self.y,)



def enter():
    global main_ui,money,windcursor,main_background,birddraw,expedition_confirm,expeditioning
    main_ui = Main_UI()
    money=Money()
    windcursor=Windcursor()
    main_background = Main_Background()
    birddraw=Draw_bird()
    expedition_confirm=Expedition_Confirm()
    expeditioning=Expeditioning()
def exit():
    global main_ui,money,windcursor,main_background,birddraw,expedition_confirm,expeditioning
    del (main_ui)
    del (money)
    del (windcursor)
    del (main_background)
    del (birddraw)
    del (expedition_confirm)
    del (expeditioning)
def pause():
    pass

def resume():
    pass


def handle_events():
    global mx, my
    global movemx,movemy
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            game_framework.pop_state()
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            main_state.mx = event.x
            main_state.my = 600-event.y
        elif event.type == SDL_MOUSEMOTION:
            main_state.movemx, main_state.movemy = event.x, 600 - event.y
        elif event.type == SDL_KEYDOWN and event.key == SDLK_UP:
            game_framework.pop_state

def update():
    global confirm,expedition,start_time
    windcursor.update()
    birddraw.update()
    expedition_confirm.update()
    if main_state.mx >= 335 and main_state.mx <= 465 and main_state.my >=22  and main_state.my <= 104:
        game_framework.pop_state()






def draw():

    clear_canvas()
    hide_cursor()
    main_background.draw()
    money.draw()
    birddraw.draw()
    expeditioning.draw()
    if confirm>0:
        expedition_confirm.draw()

    windcursor.draw()
    delay(0.03)
    update_canvas()





