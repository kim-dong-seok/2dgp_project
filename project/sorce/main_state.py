import random
import json
import os
import time

from pico2d import *

import game_framework
import title_state
import main_state2
import cage_state

name = "MainState"
boy = None
grass = None
windcursor = None
font = None
money=None
global click
cclick=0
global playermoney
playermoney=1000
global movemx, movemy
movemx=-1
movemy=-1
global mx, my
mx=-1
my=-1
global stone_count,field_stone
stone_count=0
field_stone=10
global expedition_complete,start_time,expedition_tim
expedition_complete=0
start_time=0
expedition_time=10



class Quest:
    def __init__(self):
        self.font1 = load_font('Gungsuh.TTF', 20)
        self.count=1
    def update(self):
        if stone_count>=5and self.count==1:
            self.count=2
        if cagebird[1].name >= 1 and self.count == 2:
            self.count=3
        if cagebird[1].start_time>0and self.count == 3:
            self.count=4
        if (field[0].plant_part2>=1 or field[1].plant_part2>=1 or field[2].plant_part2>=1) and self.count == 4:
            self.count=5
    def draw(self):
        if self.count==1:
            self.font1.draw(650, 350, '돌을 모으세요' , (255, 255, 255))
            self.font1.draw(650, 330, '모은 돌%d / 5' % stone_count, (255, 255, 255))
        if self.count==2:
            self.font1.draw(620, 350, '논에서 돌을 이용해', (255, 255, 255))
            self.font1.draw(620, 330, '제비를 잡으세요', (255, 255, 255))
            self.font1.draw(620, 310, ' 잡은 제비%d / 1' % main_state2.birdget, (255, 255, 255))
        if self.count==3:
            self.font1.draw(600, 350, '새장에서 잡은 제비를', (255, 255, 255))
            self.font1.draw(620, 330, '박씨 원정 보내세요', (255, 255, 255))
            self.font1.draw(620, 310, '원정%d / 1' % main_state2.birdget, (255, 255, 255))
        if self.count==4:
            self.font1.draw(660, 350, '얻은 박씨를', (255, 255, 255))
            self.font1.draw(630, 330, '심고 키우세요', (255, 255, 255))
            self.font1.draw(630, 310, '박 심기%d / 1' % main_state2.birdget, (255, 255, 255))
        if self.count==5:
            self.font1.draw(630, 350, '박을 수확하세요', (255, 255, 255))
            self.font1.draw(630, 310, '박 수확%d / 1' % main_state2.birdget, (255, 255, 255))
class Main_Background:
    def __init__(self):
        self.bgm = load_music('main_music.mp3')
        self.image = load_image('main_background.png')
        self.y = 300
        self.x = 400
        self.bgm.set_volume(32)
        self.bgm.repeat_play()
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
        self.image2 = load_image('exp.png')
        self.y = 300
        self.x = 400
        self.exp=0
    def draw(self):
        self.image.clip_draw(0, 0, 800, 600, self.x,self.y,)
        self.image2.clip_draw(0, 0, 32 * self.exp, 84, 58+6*self.exp, 570, 13*self.exp, 34)

class Bird:
    def __init__(self):
        self.name=0
        self.hp=0
        self.sp=0
        self.expedition=0
        self.start_time=0
        self.last_time=0
        self.expedition_time = 0
        self.expedition_complete=0
        self.expeditioning=0
    def update(self):
        if self.expedition>0:
            self.start_time=get_time()
            self.expedition=0
            self.expeditioning=1
        if self.start_time > 0:
            if self.expedition_time - (get_time() - self.start_time) < 0:
                self.expedition_complete = 1
                self.expeditioning = 0
                self.start_time = 0

        if self.expedition_complete > 0:
            if(mx >= 246 and mx <= 354 and my >= 106 and my <= 175) or (mx >= 383 and mx <= 559 and my >= 106 and my <= 175):
                self.expedition_complete = 0
                if self.name==1:
                    seeds[0].count += 1
                self.name=0
                self.hp = 0
                self.sp = 0
                if self.name==2:
                    seeds[1].count += 1
                self.name=0
                self.hp = 0
                self.sp = 0


    def draw(self):
        if self.expedition_complete > 0 and self.name==1:
            expedition_success.draw()
        elif self.expedition_complete > 0 and self.name == 2:
            expedition_success2.draw()
class Have_Seed:
    image1 = None
    image2 = None
    def __init__(self):
        self.name=0
        if self.image1 == None:
            self.image1 = load_image('seed_1.png')
        if self.image2 == None:
            self.image2 = load_image('gold_seed.png')
        self.count=0

    def update(self):
        pass

    def draw(self):
        pass

class Expedition:
    def __init__(self):
        self.name=0
    def update(self):
        pass


class Expedition_success:
    image = None
    def __init__(self):
        self.frame = 0
        if Expedition_success.image == None:
            self.image = load_image('success.png')

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, 800, 600,400 ,300)
class Expedition_success2:
    image = None
    def __init__(self):
        self.frame = 0
        if Expedition_success2.image == None:
            self.image = load_image('gold_seed_get.png')

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, 800, 600,400 ,300)

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

class Stone:
    image1=None
    def __init__(self):
        self.y = random.randint(0, 378)
        self.x = random.randint(0, 700)
        self.pick_up_sound = load_wav('pick_up.wav')
        self.pick_up_sound.set_volume(64)
        if Stone.image1 == None:
            Stone.image1 = load_image('stone1.png')
        self.hp=1
        self.stone_delay = 100
    def update(self):
        global stone_count
        global mx, my
        if self.hp>0:
            if self.x+30>=mx and self.x-30<=mx:
                if self.y+30>=my and self.y-30<=my:
                    self.hp=0
                    self.pick_up_sound.play()
                    mx=-1
                    my=-1
                    stone_count+=1
        if self.hp<=0:
            self.stone_delay-=1
        if self.stone_delay<=0:
            self.y = random.randint(0, 378)
            self.x = random.randint(0, 700)
            self.hp = 1
            self.stone_delay=500



    def draw(self):
        if self.hp>0:
            self.image1.clip_draw(0, 0, 800, 600, self.x, self.y,20,20)

class Field_State:
    image = None
    image2 = None
    image3 = None
    image4 = None
    image5 = None
    image6 = None
    image7 = None
    image8 = None
    image9 = None
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
            self.image7 = load_image('gourd_hitting.png')
        if Field_State.image8 == None:
            self.image8 = load_image('gourd_die.png')
        if Field_State.image9 == None:
            self.image9 = load_image('gold.png')
        self.attack_sound = load_wav('attack.wav')
        self.attack_sound.set_volume(64)
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
        self.scheck2 = 0
        self.sclick = 0 #박씨 클릭
        self.plant_part1=0 #발아기
        self.part1_clock=5
        self.plant_part2 = 0 #성장기
        self.part2_clock = 5
        self.plant_part3 = 0 #성숙기
        self.part3_clock = 600
        self.fcount=0
        self.cclick=0
        self.part1_fcheck=0
        self.part2_fcheck = 0
        self.part3_fcheck = 0
        self.hit=0
        self.hitting_count=0
        self.gourd_die=0
        self.hit_delay=0
        self.gold=0

    def update(self):
        global cclick, mx, my,playermoney
        plant.x=self.x+57
        plant.y = self.y + 57
        for field_state in field:
            if field_state.fcheck < 1:
                self.fcount += 1
        if self.gourd_die==1 and self.hit==0:
            self.mcheck = 0  # 마우스 체크
            self.fcheck = 0  # 필드 체크
            self.pcheck = 0  # 심을지 확인
            self.scheck = 0  # 박씨 정보 확인
            self.sclick = 0  # 박씨 클릭
            self.plant_part1 = 0  # 발아기
            self.plant_part2 = 0  # 성장기
            self.plant_part3 = 0  # 성숙기
            self.fcount = 0
            self.first_time1 = 0
            self.first_time2 = 0
            self.first_time3 = 0
            self.last_time = 0
            self.cclick = 0
            self.part1_fcheck = 0
            self.part2_fcheck = 0
            self.part3_fcheck = 0
            self.hitting_count = 0
            self.gourd_die = 0
        if self.gold==1:
            if self.x > 0 and self.x < mx and self.x + 114 > mx:  # 돈줍기
                if self.y > 0 and self.y < my and self.y + 114 > my:
                    self.gold=0
                    if self.seedkind==1:
                        playermoney+=1000
                    if self.seedkind==2:
                        playermoney+=2000
                    mx=-1
                    my=-1
        if self.fcount == 3 and self.gold==0:
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

                if self.x > 0 and self.x < mx and self.x + 114 > mx and self.hit==0: # 박 타기
                    if self.y > 0 and self.y < my and self.y + 114 > my:
                        self.attack_sound.play()
                        self.hit=3
                        self.hitting_count+=1
                        mx = -1
                        my = -1
                        if self.hitting_count==5:
                            self.gold = 1
                            self.gourd_die=1
                            main_ui.exp+=1
                            mx=-1
                            my=-1

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
            if self.x > 0 and self.screenx-55 < movemx and self.screenx -5 > movemx and self.fcheck==1: #씨앗 정보창
                if self.y > 0 and self.screeny+15 < movemy and self.screeny +65 > movemy:
                    self.scheck = 2
                    self.screenx2 = movemx
                    self.screeny2 = movemy
                else:
                    self.scheck= 0
            else:
                self.scheck = 0

            if self.x > 0 and self.screenx-107 < mx and self.screenx -57 > mx and self.fcheck==1: #씨앗클릭
                if self.y > 0 and self.screeny+15 < my and self.screeny +65 > my:
                    self.sclick = 1
            elif self.x > 0 and self.screenx - 55 < movemx and self.screenx - 5 > movemx and self.fcheck == 1:  # 씨앗 정보창
                if self.y > 0 and self.screeny + 15 < movemy and self.screeny + 65 > movemy:
                    self.sclick = 2

            if self.x > 0 and self.screenx+85 > mx and self.screenx +14 < mx and self.sclick==1: #심기 확인창
                if self.y > 0 and self.screeny-100 < my and self.screeny -51 > my:
                    self.pcheck=1
                    self.screenx2 = mx
                    self.screeny2 = my
                    self.seedkind=1
            if self.x > 0 and self.screenx+85 > mx and self.screenx +14 < mx and self.sclick>=2: #심기 확인창
                if self.y > 0 and self.screeny-100 < my and self.screeny -51 > my:
                    self.pcheck=2
                    self.screenx2 = mx
                    self.screeny2 = my
                    self.seedkind = 2
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
                    seeds[0].count-=1
                    cclick=0




    def draw(self):
        if self.plant_part1==1 and self.part1_clock/2 >(get_time() - self.first_time1):
            self.image5.clip_draw(0, 0, 51, 49, self.x+65, self.y+75, 40, 40)
        elif self.plant_part1==1:
            self.image6.clip_draw(0, 0, 70, 69, self.x+54, self.y+85, 70, 70)
        if self.plant_part2==1and self.seedkind==1:
            self.image7.clip_draw(0, 0, 200, 200, self.x + 57, self.y + 70, 50+(get_time() - self.first_time1)/2, 50+(get_time() - self.first_time1)/2)
        if self.plant_part2==1and self.seedkind==2:
            self.image7.clip_draw(0, 0, 200, 200, self.x + 57, self.y + 70, 80+(get_time() - self.first_time1)/2, 80+(get_time() - self.first_time1)/2)
        if self.plant_part3 == 1and self.seedkind==1:
            if self.gourd_die==0:
                self.image7.clip_draw(0+(200*self.hit), 0, 200, 200, self.x + 57, self.y + 70, 100,100)
            else:
                self.image8.clip_draw(0 + (200 * self.hit), 0, 200, 200, self.x + 57, self.y + 70, 100, 100)

            if self.hit_delay == 1:
                self.hit_delay = 0
                if self.hit > 0:
                    self.hit -= 1
            self.hit_delay += 1
        if self.plant_part3 == 1and self.seedkind==2:
            if self.gourd_die==0:
                self.image7.clip_draw(0+(200*self.hit), 0, 200, 200, self.x + 57, self.y + 70, 120,120)
            else:
                self.image8.clip_draw(0 + (200 * self.hit), 0, 200, 200, self.x + 57, self.y + 70, 120, 120)

            if self.hit_delay == 1:
                self.hit_delay = 0
                if self.hit > 0:
                    self.hit -= 1
            self.hit_delay += 1
        if self.gold==1and self.seedkind==1:
            self.image9.clip_draw(0, 0, 800, 600, self.x + 57, self.y + 70, 100, 100)
        if self.gold==1and self.seedkind==2:
            self.image9.clip_draw(0, 0, 800, 600, self.x + 57, self.y + 70, 120, 120)
        if self.mcheck==1:
            self.image.clip_draw(0, 0, 200 , 100, self.screenx+100,self.screeny+50,200,100)
            if self.fcheck==0 and self.plant_part1==0:
                self.font.draw(self.screenx+5,self.screeny+80 , '집앞 밭', (255, 255, 255))
                self.font2.draw(self.screenx + 5, self.screeny + 55, '상태: 재배가능', (0, 255, 0))
                self.font3.draw(self.screenx + 5, self.screeny + 35, '밭을 클릭하여 재배할', (255, 255, 0))
                self.font3.draw(self.screenx + 5, self.screeny + 16, '작물을 선택하세요', (255, 255, 0))
        if self.fcheck==1:
            self.image2.clip_draw(0, 0, 282, 274, self.screenx , self.screeny )

            if self.sclick == 1:
                self.image4.clip_draw(0, 0, 109, 120, self.screenx - 82, self.screeny + 40, 50, 50)
            if seeds[0].count>=1:
                seeds[0].image1.clip_draw(0, 0, 109, 120, self.screenx-82,self.screeny+40,50,50)
            if self.sclick == 2:
                self.image4.clip_draw(0, 0, 109, 120, self.screenx - 30, self.screeny + 40, 50, 50)
            if seeds[1].count>=1:
                seeds[1].image2.clip_draw(0, 0, 109, 120, self.screenx-30,self.screeny+40,50,50)

        if self.scheck == 1 and self.plant_part1 == 0 and seeds[0].count>0:
            seed_information.image1.clip_draw(0, 0, 256, 219, self.screenx2 + 150, self.screeny2 - 50, 256, 219)
            seeds[0].image1.clip_draw(0, 0, 109, 120, self.screenx2 + 57, self.screeny2 + 25, 50, 50)
            self.font.draw(self.screenx2 + 100, self.screeny2 + 25, '평범한 박 씨앗', (255, 255, 255))
            self.font2.draw(self.screenx2 + 30, self.screeny2 - 20, '생장주기:', (0, 255, 0))
            self.font2.draw(self.screenx2 + 30, self.screeny2 - 40, '[발아기] 10초' , (0, 255, 0))
            self.font2.draw(self.screenx2 + 30, self.screeny2 - 60, '[성장기] 1분', (0, 255, 0))
            self.font2.draw(self.screenx2 + 30, self.screeny2 - 80, '[성숙기] 10분', (0, 255, 0))
            self.font3.draw(self.screenx2 + 30, self.screeny2 - 100, '누가 봐도 평범해 보이는 박의 씨앗', (255, 255, 0))
            self.font4.draw(self.screenx2 + 30, self.screeny2 - 128, '주의: 발아기, 성장기에 정성껏 돌보면', (255, 255, 0))
            self.font4.draw(self.screenx2 + 30, self.screeny2 - 146, '성숙기에 더 좋은 보상을 받을 수 있다', (255, 255, 0))
        if self.scheck ==2and self.plant_part1 == 0 and seeds[1].count>0:
            seed_information.image1.clip_draw(0, 0, 256, 219, self.screenx2 + 150, self.screeny2 - 50, 256, 219)
            seeds[1].image2.clip_draw(0, 0, 109, 120, self.screenx2 + 57, self.screeny2 + 25, 50, 50)
            self.font.draw(self.screenx2 + 100, self.screeny2 + 25, '고오급 박 씨앗', (255, 255, 255))
            self.font2.draw(self.screenx2 + 30, self.screeny2 - 20, '생장주기:', (0, 255, 0))
            self.font2.draw(self.screenx2 + 30, self.screeny2 - 40, '[발아기] 20초' , (0, 255, 0))
            self.font2.draw(self.screenx2 + 30, self.screeny2 - 60, '[성장기] 2분', (0, 255, 0))
            self.font2.draw(self.screenx2 + 30, self.screeny2 - 80, '[성숙기] 20분', (0, 255, 0))
            self.font3.draw(self.screenx2 + 30, self.screeny2 - 100, '내용물을 알 수 없는 고오급 스러운 박', (255, 255, 0))
            self.font4.draw(self.screenx2 + 30, self.screeny2 - 128, '주의: 발아기, 성장기에 정성껏 돌보면', (255, 255, 0))
            self.font4.draw(self.screenx2 + 30, self.screeny2 - 146, '성숙기에 더 좋은 보상을 받을 수 있다', (255, 255, 0))
        if self.pcheck==1:
            self.image3.clip_draw(0, 0, 266, 166, self.screenx2 , self.screeny2+100 )
            self.font2.draw(self.screenx2 - 85, self.screeny2 + 135, '평범한 박 씨앗 작물을', (0, 0, 0))
            self.font2.draw(self.screenx2 - 85, self.screeny2 + 115, '재배하시겠습니까?', (0, 0, 0))
        if self.pcheck==2:
            self.image3.clip_draw(0, 0, 266, 166, self.screenx2 , self.screeny2+100 )
            self.font2.draw(self.screenx2 - 85, self.screeny2 + 135, '고오굽 박 씨앗 작물을', (0, 0, 0))
            self.font2.draw(self.screenx2 - 85, self.screeny2 + 115, '재배하시겠습니까?', (0, 0, 0))
        if self.part1_fcheck==1:
            self.image.clip_draw(0, 0, 200 , 100, self.screenx+100,self.screeny+50,200,100)
            if self.fcheck==0and self.seedkind==1:
                self.font.draw(self.screenx+5,self.screeny+80 , '평범한 박 씨앗', (255, 255, 255))
                self.font2.draw(self.screenx + 5, self.screeny + 55, '발아기:', (255, 255, 255))
                self.font2.draw(self.screenx + 75, self.screeny + 55, '%d초(남음)' %(self.part1_clock-(get_time()-self.first_time1)), (0, 255, 0))
                self.font2.draw(self.screenx + 5 ,self.screeny + 35, '생명력:', (255, 255, 255))
                self.font2.draw(self.screenx + 75, self.screeny + 35, '나쁨(하)', (255, 255, 0))
                self.font2.draw(self.screenx + 5, self.screeny + 16, '상태: 성장 중', (255, 255, 255))
            if self.fcheck== 0and self.seedkind==2:
                self.font.draw(self.screenx+5,self.screeny+80 , '고오급 박 씨앗', (255, 255, 255))
                self.font2.draw(self.screenx + 5, self.screeny + 55, '발아기:', (255, 255, 255))
                self.font2.draw(self.screenx + 75, self.screeny + 55, '%d초(남음)' %(self.part1_clock-(get_time()-self.first_time1)), (0, 255, 0))
                self.font2.draw(self.screenx + 5 ,self.screeny + 35, '생명력:', (255, 255, 255))
                self.font2.draw(self.screenx + 75, self.screeny + 35, '나쁨(하)', (255, 255, 0))
                self.font2.draw(self.screenx + 5, self.screeny + 16, '상태: 성장 중', (255, 255, 255))
        if self.part2_fcheck == 1:
            self.image.clip_draw(0, 0, 200, 100, self.screenx + 100, self.screeny + 50, 200, 100)
            if self.fcheck == 0 and self.seedkind==1:
                self.font.draw(self.screenx + 5, self.screeny + 80, '평범한 박 씨앗', (255, 255, 255))
                self.font2.draw(self.screenx + 5, self.screeny + 55, '성장기:', (255, 255, 255))
                self.font2.draw(self.screenx + 75, self.screeny + 55, '%d초(남음)' % (self.part2_clock - (get_time() - self.first_time1)),(0, 255, 0))
                self.font2.draw(self.screenx + 5, self.screeny + 35, '생명력:', (255, 255, 255))
                self.font2.draw(self.screenx + 75, self.screeny + 35, '나쁨(하)', (255, 255, 0))
                self.font2.draw(self.screenx + 5, self.screeny + 16, '상태: 성장 중', (255, 255, 255))
            if self.fcheck == 0and self.seedkind==2:
                self.font.draw(self.screenx + 5, self.screeny + 80, '고오급 박 씨앗', (255, 255, 255))
                self.font2.draw(self.screenx + 5, self.screeny + 55, '성장기:', (255, 255, 255))
                self.font2.draw(self.screenx + 75, self.screeny + 55, '%d초(남음)' % (self.part2_clock - (get_time() - self.first_time1)),(0, 255, 0))
                self.font2.draw(self.screenx + 5, self.screeny + 35, '생명력:', (255, 255, 255))
                self.font2.draw(self.screenx + 75, self.screeny + 35, '나쁨(하)', (255, 255, 0))
                self.font2.draw(self.screenx + 5, self.screeny + 16, '상태: 성장 중', (255, 255, 255))
        if self.part3_fcheck == 1:
            self.image.clip_draw(0, 0, 200, 100, self.screenx + 100, self.screeny + 50, 200, 100)
            if self.fcheck == 0and self.seedkind==1:
                self.font.draw(self.screenx + 5, self.screeny + 80, '평범한 박 씨앗', (255, 255, 255))
                self.font2.draw(self.screenx + 5, self.screeny + 55, '성숙기:', (255, 255, 255))
                self.font2.draw(self.screenx + 75, self.screeny + 55, '%d분(남음)' % ((self.part3_clock - (get_time() - self.first_time1))/60),(0, 255, 0))
                self.font2.draw(self.screenx + 5, self.screeny + 35, '생명력:', (255, 255, 255))
                self.font2.draw(self.screenx + 75, self.screeny + 35, '나쁨(하)', (255, 255, 0))
                self.font2.draw(self.screenx + 5, self.screeny + 16, '상태: 수확 대기', (255, 255, 255))
            if self.fcheck == 0and self.seedkind==2:
                self.font.draw(self.screenx + 5, self.screeny + 80,  '고오급 박 씨앗', (255, 255, 255))
                self.font2.draw(self.screenx + 5, self.screeny + 55, '성숙기:', (255, 255, 255))
                self.font2.draw(self.screenx + 75, self.screeny + 55, '%d분(남음)' % ((self.part3_clock - (get_time() - self.first_time1))/60),(0, 255, 0))
                self.font2.draw(self.screenx + 5, self.screeny + 35, '생명력:', (255, 255, 255))
                self.font2.draw(self.screenx + 75, self.screeny + 35, '나쁨(하)', (255, 255, 0))
                self.font2.draw(self.screenx + 5, self.screeny + 16, '상태: 수확 대기', (255, 255, 255))
def enter():
    global main_ui,money,windcursor,main_background,cagebird,field,seeds,seed_information,plant,stones,expedition_success,image1,font1,expeditions
    global quest,expedition_success2
    image1 = load_image('stone1.png')
    font1 = load_font('Gungsuh.TTF', 35)
    main_ui = Main_UI()
    money=Money()
    quest=Quest()
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
    expeditions=[Expedition() for i in range(2)]
    seeds[0].name=1
    seeds[0].count =10
    seeds[1].name=2
    seeds[1].count = 10
    stones = [Stone() for i in range(10)]
    expedition_success=Expedition_success()
    expedition_success2=Expedition_success2()
def exit():
    global main_ui,money,windcursor,main_background,cagebird,field,seeds,seed_information,plant,stones,expedition_success,expeditions,quest,expedition_success
    del (main_ui)
    del (money)
    del (windcursor)
    del(main_background)
    del(cagebird)
    del(field)
    del(seeds)
    del(seed_information)
    del(plant)
    del(stones)
    del(expedition_success)
    del(expeditions)
    del(quest)
    del(expedition_success2)
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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_DOWN:
            game_framework.push_state(cage_state)
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            mx = event.x
            my = 600-event.y
            cclick=1
        elif event.type == SDL_MOUSEBUTTONUP and event.button == SDL_BUTTON_LEFT:
            cclick=0
        elif event.type == SDL_MOUSEMOTION:
            movemx, movemy = event.x, 600 - event.y


def update():
    global expedition_complete,start_time
    windcursor.update()
    for stone in stones:
        stone.update()
    for field_state in field:
        field_state.update()
    for bird in cagebird:
        bird.update()
    quest.update()


def draw():

    clear_canvas()
    hide_cursor()
    main_background.draw()
    main_ui.draw()
    money.draw()
    for stone in stones:
        stone.draw()
    for field_state in field:
        field_state.draw()
    for bird in cagebird:
        bird.draw()


    image1.clip_draw(0, 0, 800, 600, 50, 50, 80, 80)
    font1.draw(80, 60, ' X %d' % stone_count, (255, 255, 255))
    quest.draw()
    windcursor.draw()
    delay(0.03)
    update_canvas()





