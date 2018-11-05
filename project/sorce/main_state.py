import random
import json
import os
import time

from pico2d import *

import game_framework
import title_state
import main_state2

name = "MainState"
boy = None
grass = None
windcursor = None
font = None
money=None
global click
cclick=0
global playermoney
playermoney=99999999
global movemx, movemy
movemx=-1
movemy=-1
global mx, my
mx=-1
my=-1
class Main_Background:
    def __init__(self):
        self.image = load_image('main_background.png')
        self.y = 300
        self.x = 400
    def draw(self):
        self.image.clip_draw(0, 0, 800, 600, self.x,self.y,)


class Windcursor:
    image = None
    def __init__(self):
        self.frame = 0
        if Windcursor.image == None:
            self.image = load_image('cursor.png')

    def update(self):
        self.frame = (self.frame + 1) % 13


    def draw(self):
            self.image.clip_draw(self.frame * 30, 0, 30, 45, movemx, movemy-20)

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
        self.image1.clip_draw(((playermoney%10)+1)*97, 0, 97, 145,744,572, 17, 28)
        self.image1.clip_draw((((playermoney%100)//10)+1)*97, 0, 97, 145, 700, 572, 17, 28)
        self.image1.clip_draw((((playermoney%1000)//100)+1)*97, 0, 97, 145, 654, 572, 17, 28)
        self.image1.clip_draw((((playermoney%10000)//1000)+1)*97, 0, 97, 145, 638, 572, 17, 28)
        self.image1.clip_draw((((playermoney%100000)//10000)+1)*97, 0, 97, 145, 622, 572, 17, 28)
        self.image1.clip_draw((((playermoney%1000000)//100000)+1)*97, 0, 97, 145, 606, 572, 17, 28)
        self.image1.clip_draw((((playermoney%10000000)//1000000)+1)*97, 0, 97, 145, 590, 572, 17, 28)

class Main_UI:
    def __init__(self):
        self.image = load_image('main_ui.png')
        self.y = 300
        self.x = 400
    def draw(self):
        self.image.clip_draw(0, 0, 800, 600, self.x,self.y,)


class Bird:
    def __init__(self):
        self.name=0
        self.hp=0
        self.sp=0
        self.expedition=0

    def update(self):
        pass

    def draw(self):
        pass
class Have_Seed:
    image1 = None
    def __init__(self):
        self.name=0
        if Have_Seed.image1 == None:
            self.image1 = load_image('seed_1.png')
        self.count=0

    def update(self):
        pass

    def draw(self):
        pass
class Seed_Information:
    image1 = None
    def __init__(self):
        if Seed_Information.image1 == None:
            self.image1 = load_image('seed_information.png')


    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, 200, 100, self.screenx + 100, self.screeny + 50, 200, 100)
class Draw_Plant:
    image1 = None
    image2 = None
    def __init__(self):
        if Field_State.image == None:
            self.image1 = load_image('plant_part1_1.png')
        if Field_State.image2 == None:
            self.image2 = load_image('plant_part1_2.png')
        self.x=0
        self.y=0
    def update(self):
        pass
    def draw(self):
        self.image1.clip_draw(0, 0, 51,49, self.x, self.y, 50, 50)
        #self.image2.clip_draw(0, 0, 70, 69, self.x, self.y, 70, 70)
class Field_State:
    image = None
    image2 = None
    image3 = None
    image4 = None
    image5 = None
    image6 = None
    image7 = None
    def __init__(self):
        self.frame = 0
        self.seedkind=0
        self.font = load_font('Gungsuh.TTF', 20)
        self.font2 = load_font('Gungsuh.TTF', 18)
        self.font3 = load_font('Gungsuh.TTF', 15)
        self.font4 = load_font('Gungsuh.TTF', 13)
        if Field_State.image == None:
            self.image = load_image('field_state.png')
        if Field_State.image2 == None:
            self.image2 = load_image('seed_select.png')
        if Field_State.image3 == None:
            self.image3 = load_image('plant_check.png')
        if Field_State.image4 == None:
            self.image4 = load_image('seed_click.png')
        if Field_State.image5 == None:
            self.image5 = load_image('plant_part1_1.png')
        if Field_State.image6 == None:
            self.image6 = load_image('plant_part1_2.png')
        if Field_State.image7 == None:
            self.image7 = load_image('gourd_stand.png')
        self.x=0
        self.y=0
        self.screenx=0
        self.screeny = 0
        self.screenx2 = 0
        self.screeny2 = 0
        self.mcheck=0 #마우스 체크
        self.fcheck=0 #필드 체크
        self.pcheck=0 #심을지 확인
        self.scheck=0 #박씨 정보 확인
        self.sclick = 0 #박씨 클릭
        self.plant_part1=0 #발아기
        self.part1_clock=10
        self.plant_part2 = 0 #성장기
        self.part2_clock = 60
        self.plant_part3 = 0 #성숙기
        self.part3_clock = 600
        self.fcount=0
        self.first_time1=0
        self.first_time2= 0
        self.first_time3= 0
        self.last_time = 0
        self.cclick=0
        self.part1_fcheck=0
        self.part2_fcheck = 0
        self.part3_fcheck = 0
    def update(self):
        global cclick
        plant.x=self.x+57
        plant.y = self.y + 57
        for field_state in field:
            if field_state.fcheck < 1:
                self.fcount += 1
        if self.fcount == 3:
            if self.plant_part1 == 1 and self.plant_part2 == 0:

                if self.x > 0 and self.x < movemx and self.x + 114 > movemx:
                    if self.y > 0 and self.y < movemy and self.y + 114 > movemy:
                        self.part1_fcheck = 1
                        self.screenx = movemx
                        self.screeny = movemy

                    else:
                        self.part1_fcheck = 0
                else:
                    self.part1_fcheck = 0
                if self.part1_clock - (get_time() - self.first_time1) < 0:
                    self.part1_fcheck = 0
                    self.plant_part2 = 1
                    self.plant_part1 = 2
                    self.first_time1 = get_time()

            if self.plant_part1 == 2 and self.plant_part2 == 1:
                if self.x > 0 and self.x < movemx and self.x + 114 > movemx:
                    if self.y > 0 and self.y < movemy and self.y + 114 > movemy:
                        self.part2_fcheck = 1
                        self.screenx = movemx
                        self.screeny = movemy

                    else:
                        self.part2_fcheck = 0
                else:
                    self.part2_fcheck = 0
                if self.part2_clock - (get_time() - self.first_time1) < 0:
                    self.part2_fcheck = 0
                    self.plant_part3 = 1
                    self.plant_part2 = 2
                    self.first_time1 = get_time()

            if self.plant_part1 == 2 and self.plant_part2 == 2 and self.plant_part3 == 1:
                if self.x > 0 and self.x < movemx and self.x + 114 > movemx:
                    if self.y > 0 and self.y < movemy and self.y + 114 > movemy:
                        self.part3_fcheck = 1
                        self.screenx = movemx
                        self.screeny = movemy

                    else:
                        self.part3_fcheck = 0
                else:
                    self.part3_fcheck = 0
                if self.part3_clock - (get_time() - self.first_time1) < 0:
                    self.part2_fcheck = 0
                    self.plant_part3 = 1
                    self.plant_part2 = 2
                    self.first_time1 = get_time()

            if self.plant_part1 == 0:
                if self.fcheck < 1:
                    if self.x > 0 and self.x < movemx and self.x + 114 > movemx:
                        if self.y > 0 and self.y < movemy and self.y + 114 > movemy:
                            self.mcheck = 1
                            self.screenx = movemx
                            self.screeny = movemy
                        else:
                            self.mcheck = 0
                    else:
                        self.mcheck = 0

                    if self.x > 0 and self.x < mx and self.x + 114 > mx and cclick == 1:  # 씨앗선택창
                        if self.y > 0 and self.y < my and self.y + 114 > my:
                            self.fcheck = 1
                            self.mcheck = 0
                            self.screenx = mx
                            self.screeny = my
                            self.cclick = 0
        self.fcount = 0;
        if self.plant_part1 == 0:
            if self.x > 0 and self.screenx-85 < mx and self.screenx -14 > mx:     #씨앗선택창 취소
                if self.y > 0 and self.screeny-100 < my and self.screeny -51 > my:
                    self.fcheck = 0
                    self.mcheck = 0
                    self.screenx = 0
                    self.screeny = 0
                    self.cclick =mx
                    cclick = 0
            if self.x > 0 and self.screenx-107 < movemx and self.screenx -57 > movemx and self.fcheck==1: #씨앗 정보창
                if self.y > 0 and self.screeny+15 < movemy and self.screeny +65 > movemy:
                    self.scheck = 1
                    self.screenx2 = movemx
                    self.screeny2 = movemy
                else:
                    self.scheck = 0
            else:
                self.scheck = 0

            if self.x > 0 and self.screenx-107 < mx and self.screenx -57 > mx and self.fcheck==1: #씨앗클릭
                if self.y > 0 and self.screeny+15 < my and self.screeny +65 > my:
                    self.sclick = 1

            if self.x > 0 and self.screenx+85 > mx and self.screenx +14 < mx and self.sclick==1: #심기 확인창
                if self.y > 0 and self.screeny-100 < my and self.screeny -51 > my:
                    self.pcheck=1
                    self.screenx2 = mx
                    self.screeny2 = my

            if self.x > 0 and self.screenx2-85 < mx and self.screenx2 -14 > mx: #심기 취소
                if self.y > 0 and self.screeny2+100-57 < my and self.screeny2+100 -14 > my:
                    self.pcheck = 0
                    self.screenx2 = 0
                    self.screeny2 = 0
                    cclick = 0
            if self.x > 0 and self.screenx2 + 85 > mx and self.screenx2 + 14 < mx:  #심기 확인
                if self.y > 0 and self.screeny2 + 100 - 57 < my and self.screeny2 + 100 - 14 > my:
                    self.pcheck = 0
                    self.screenx2 = 0
                    self.screeny2 = 0
                    self.fcheck = 0
                    self.plant_part1 = 1
                    self.sclick=0
                    self.first_time1=get_time()
                    cclick=0




    def draw(self):
        if self.plant_part1==1 and self.part1_clock/2 >(get_time() - self.first_time1):
            self.image5.clip_draw(0, 0, 51, 49, self.x+65, self.y+75, 40, 40)
        elif self.plant_part1==1:
            self.image6.clip_draw(0, 0, 70, 69, self.x+54, self.y+85, 70, 70)
        if self.plant_part2==1:
            self.image7.clip_draw(0, 0, 296, 296, self.x + 57, self.y + 70, 50+(get_time() - self.first_time1)/2, 50+(get_time() - self.first_time1)/2)
        if self.plant_part3 == 1:
            self.image7.clip_draw(0, 0, 296, 296, self.x + 57, self.y + 70, 50 + 30,50 +30)
        if self.mcheck==1:
            self.image.clip_draw(0, 0, 200 , 100, self.screenx+100,self.screeny+50,200,100)
            if self.fcheck==0 and self.plant_part1==0:
                self.font.draw(self.screenx+5,self.screeny+80 , '집앞 밭', (255, 255, 255))
                self.font2.draw(self.screenx + 5, self.screeny + 55, '상태: 재배가능', (0, 255, 0))
                self.font3.draw(self.screenx + 5, self.screeny + 35, '밭을 클릭하여 재배할', (255, 255, 0))
                self.font3.draw(self.screenx + 5, self.screeny + 16, '작물을 선택하세요', (255, 255, 0))
        if self.fcheck==1:
            self.image2.clip_draw(0, 0, 282, 274, self.screenx , self.screeny )
            for have_seed in seeds:
                if have_seed.name>0 and have_seed.count>0:
                    if self.sclick == 1:
                        self.image4.clip_draw(0, 0, 109, 120, self.screenx - 82, self.screeny + 40, 50, 50)
                    have_seed.image1.clip_draw(0, 0, 109, 120, self.screenx-82,self.screeny+40,50,50)
                    self.seedkind+=1

        if self.scheck == 1 and self.plant_part1 == 0:
            seed_information.image1.clip_draw(0, 0, 256, 219, self.screenx2 + 150, self.screeny2 - 50, 256, 219)
            seeds[1].image1.clip_draw(0, 0, 109, 120, self.screenx2 + 57, self.screeny2 + 25, 50, 50)
            self.font.draw(self.screenx2 + 100, self.screeny2 + 25, '평범한 박 씨앗', (255, 255, 255))
            self.font2.draw(self.screenx2 + 30, self.screeny2 - 20, '생장주기:', (0, 255, 0))
            self.font2.draw(self.screenx2 + 30, self.screeny2 - 40, '[발아기] 10초' , (0, 255, 0))
            self.font2.draw(self.screenx2 + 30, self.screeny2 - 60, '[성장기] 1분', (0, 255, 0))
            self.font2.draw(self.screenx2 + 30, self.screeny2 - 80, '[성숙기] 10분', (0, 255, 0))
            self.font3.draw(self.screenx2 + 30, self.screeny2 - 100, '누가 봐도 평범해 보이는 박의 씨앗', (255, 255, 0))
            self.font4.draw(self.screenx2 + 30, self.screeny2 - 128, '주의: 발아기, 성장기에 정성껏 돌보면', (255, 255, 0))
            self.font4.draw(self.screenx2 + 30, self.screeny2 - 146, '성숙기에 더 좋은 보상을 받을 수 있다', (255, 255, 0))

        if self.pcheck==1:
            self.image3.clip_draw(0, 0, 266, 166, self.screenx2 , self.screeny2+100 )
            self.font2.draw(self.screenx2 - 85, self.screeny2 + 135, '평범한 박 씨앗 작물을', (0, 0, 0))
            self.font2.draw(self.screenx2 - 85, self.screeny2 + 115, '재배하시겠습니까?', (0, 0, 0))

        if self.part1_fcheck==1:
            self.image.clip_draw(0, 0, 200 , 100, self.screenx+100,self.screeny+50,200,100)
            if self.fcheck==0:
                self.font.draw(self.screenx+5,self.screeny+80 , '평범한 박 씨앗', (255, 255, 255))
                self.font2.draw(self.screenx + 5, self.screeny + 55, '발아기:', (255, 255, 255))
                self.font2.draw(self.screenx + 75, self.screeny + 55, '%d초(남음)' %(self.part1_clock-(get_time()-self.first_time1)), (0, 255, 0))
                self.font2.draw(self.screenx + 5 ,self.screeny + 35, '생명력:', (255, 255, 255))
                self.font2.draw(self.screenx + 75, self.screeny + 35, '나쁨(하)', (255, 255, 0))
                self.font2.draw(self.screenx + 5, self.screeny + 16, '상태: 성장 중', (255, 255, 255))

        if self.part2_fcheck == 1:
            self.image.clip_draw(0, 0, 200, 100, self.screenx + 100, self.screeny + 50, 200, 100)
            if self.fcheck == 0:
                self.font.draw(self.screenx + 5, self.screeny + 80, '평범한 박 씨앗', (255, 255, 255))
                self.font2.draw(self.screenx + 5, self.screeny + 55, '성장기:', (255, 255, 255))
                self.font2.draw(self.screenx + 75, self.screeny + 55, '%d초(남음)' % (self.part2_clock - (get_time() - self.first_time1)),(0, 255, 0))
                self.font2.draw(self.screenx + 5, self.screeny + 35, '생명력:', (255, 255, 255))
                self.font2.draw(self.screenx + 75, self.screeny + 35, '나쁨(하)', (255, 255, 0))
                self.font2.draw(self.screenx + 5, self.screeny + 16, '상태: 성장 중', (255, 255, 255))
        if self.part3_fcheck == 1:
            self.image.clip_draw(0, 0, 200, 100, self.screenx + 100, self.screeny + 50, 200, 100)
            if self.fcheck == 0:
                self.font.draw(self.screenx + 5, self.screeny + 80, '평범한 박 씨앗', (255, 255, 255))
                self.font2.draw(self.screenx + 5, self.screeny + 55, '성숙기:', (255, 255, 255))
                self.font2.draw(self.screenx + 75, self.screeny + 55, '%d분(남음)' % ((self.part3_clock - (get_time() - self.first_time1))/60),(0, 255, 0))
                self.font2.draw(self.screenx + 5, self.screeny + 35, '생명력:', (255, 255, 255))
                self.font2.draw(self.screenx + 75, self.screeny + 35, '나쁨(하)', (255, 255, 0))
                self.font2.draw(self.screenx + 5, self.screeny + 16, '상태: 수확 대기', (255, 255, 255))
def enter():
    global main_ui,money,windcursor,main_background,cagebird,field,seeds,seed_information,plant
    main_ui = Main_UI()
    money=Money()
    main_background=Main_Background()
    windcursor=Windcursor()
    seed_information=Seed_Information()
    field=[Field_State() for i in range(3)]
    field[0].x = 312
    field[0].y = 378
    field[1].x = 312
    field[1].y = 186
    field[2].x = 490
    field[2].y = 186
    plant=Draw_Plant()
    cagebird=[Bird() for i in range(6)]
    seeds=[Have_Seed() for i in range(10)]
    seeds[0].name=1
    seeds[0].count = 3

def exit():
    global main_ui,money,windcursor,main_background,cagebird,field,seeds,seed_information,plant
    del (main_ui)
    del (money)
    del (windcursor)
    del(main_background)
    del(cagebird)
    del(field)
    del(seeds)
    del(seed_information)
    del(plant)
def pause():
    pass

def resume():
    pass


def handle_events():
    global mx, my
    global movemx,movemy,cclick
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            game_framework.push_state(main_state2)
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            mx = event.x
            my = 600-event.y
            cclick=1
        elif event.type == SDL_MOUSEBUTTONUP and event.button == SDL_BUTTON_LEFT:
            cclick=0
        elif event.type == SDL_MOUSEMOTION:
            movemx, movemy = event.x, 600 - event.y


def update():
    windcursor.update()
    for field_state in field:
        field_state.update()
def draw():

    clear_canvas()
    hide_cursor()
    main_background.draw()
    main_ui.draw()
    money.draw()
    for field_state in field:
        field_state.draw()
    windcursor.draw()
    delay(0.03)
    update_canvas()





