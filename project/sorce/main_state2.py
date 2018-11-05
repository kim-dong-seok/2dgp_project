import random
import json
import os
import time
from pico2d import *

import game_framework
import title_state
import main_state
import cage_state

name = "MainState"
boy = None
swallow = None
grass = None
windcursor = None
font = None
money=None

global birdget
birdget=0


class Main_Background:
    def __init__(self):
        self.image = load_image('main_background2.png')
        self.y = 300
        self.x = 400
    def draw(self):
        self.image.clip_draw(0, 0, 800, 600, self.x,self.y,)

class Getbird:
    image = None
    image_fps =None
    def __init__(self):
        self.frame = 0
        if Getbird.image == None:
            self.image = load_image('chicken.png')

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, 800, 600,400 ,300)

class Windcursor:
    image = None
    image_fps =None
    def __init__(self):
        self.frame = 0
        if Windcursor.image == None:
            self.image = load_image('cursor.png')
        if Windcursor.image_fps == None:
            self.image_fps = load_image('fpscursor.png')
    def update(self):
        self.frame = (self.frame + 1) % 13


    def draw(self):
        if main_state.movemy>=500:
            self.image.clip_draw(self.frame * 30, 0, 30, 45, main_state.movemx, main_state.movemy)
        else:
            self.image_fps.clip_draw(0, 0, 100, 100, main_state.movemx, main_state.movemy,30,30)

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
class Swallow:
    image1 = None
    image2 = None
    imagehp = None
    def __init__(self):
        self.y = random.randint(0,500)
        self.x = random.randint(0,800)
        self.frame = 0
        self.xdir = 1
        self.ydir = 1
        self.hp=4

        if Swallow.image1 == None:
            Swallow.image1 = load_image('swallow.png')

        if Swallow.image2 == None:
            Swallow.image2 = load_image('swallow2.png')
        if Swallow.imagehp == None:
            Swallow.imagehp = load_image('hpbar.png')
    def update(self):
        global birdget
        global mx, my
        self.frame = (self.frame + 1) % 5
        self.x += self.xdir
        self.y += self.ydir
        if self.hp>0:
            if self.x+30>=main_state.mx and self.x-30<=main_state.mx:
                if self.y+30>=main_state.my and self.y-30<=main_state.my:
                    self.hp-=1
                    main_state.mx=-1
                    main_state.my=-1
        elif self.hp==0:
            birdget=1
            main_state.cagebird[1].name =1
            main_state.cagebird[1].hp = 50
            main_state.cagebird[1].sp = 30
            self.hp=-1
        if self.x >= 750:
            self.xdir = -1
        elif self.x <= 50:
            self.xdir = 1

        if self.y >= 500:
            self.ydir = -1
        elif self.y <= 50:
            self.ydir = 1

    def draw(self):

        if self.hp>0:
            if self.xdir==1:
                self.image1.clip_draw(self.frame * 378, 0, 378, 523, self.x, self.y,50,50)
            else:
                self.image2.clip_draw(self.frame * 378, 0, 378, 523, self.x, self.y,50,50)
        if self.hp < 3:
            if self.hp >= 1:
                self.imagehp.clip_draw(0, 0, 20, 10, self.x-20, self.y+20)
                if self.hp >= 2:
                    self.imagehp.clip_draw(0, 0, 20, 10, self.x, self.y + 20)
                    if self.hp >= 3:
                        self.imagehp.clip_draw(0, 0, 20, 10, self.x+20, self.y + 20)
class Main_UI:
    def __init__(self):
        self.image = load_image('main_ui2.png')
        self.y = 300
        self.x = 400
    def draw(self):
        self.image.clip_draw(0, 0, 800, 600, self.x,self.y,)


class Boy:
    def __init__(self):
        self.x, self.y = 0, 90
        self.frame = 0
        self.image = load_image('run_animation.png')
        self.dir = 1

    def update(self):
        self.frame = (self.frame + 1) % 8
        self.x += self.dir
        if self.x >= 800:
            self.dir = -1
        elif self.x <= 0:
            self.dir = 1

    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)


def enter():
    global main_ui,birds,money,windcursor,getbird,main_background
    getbird = Getbird()
    main_ui = Main_UI()
    money=Money()
    main_background=Main_Background()
    windcursor=Windcursor()
    birds = [Swallow() for i in range(11)]

def exit():
    global main_ui,birds,money,windcursor,getbird,main_background
    del(getbird)
    del (birds)
    del (main_ui)
    del (money)
    del (windcursor)
    del(main_background)

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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            game_framework.pop_state()
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            main_state.mx = event.x
            main_state.my = 600-event.y
        elif event.type == SDL_MOUSEMOTION:
            main_state.movemx, main_state.movemy = event.x, 600 - event.y


def update():
    global birdget
    windcursor.update()
    if birdget<1:
        for swallow in birds:
            swallow.update()
    if birdget > 0:
        if main_state.mx >= 246 and main_state.mx <= 354 and main_state.my >= 106 and main_state.my <= 175:
            birdget=0
        if main_state.mx >= 383 and main_state.mx <= 559 and main_state.my >= 106 and main_state.my <= 175:
            game_framework.change_state(cage_state)
            birdget = 0


def draw():

    clear_canvas()
    hide_cursor()
    main_background.draw()
    main_ui.draw()
    money.draw()
    for swallow in birds:
        swallow.draw()
    if birdget>0:
        getbird.draw()
    windcursor.draw()
    delay(0.03)
    update_canvas()



