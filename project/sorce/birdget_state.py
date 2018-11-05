import game_framework
import main_state2
from pico2d import *


name = "PauseState"
image = None
logo_time = 0.0

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




def enter():
    global getbird
    getbird=Getbird()



def exit():
    global getbird
    del(getbird)


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_p):
                game_framework.pop_state()
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            main_state.mx = event.x
            main_state.my =600- event.y
        elif event.type == SDL_MOUSEMOTION:
            main_state.movemx, main_state.movemy = event.x, 600 - event.y


def draw():
    clear_canvas()
    main_state.hide_cursor()
    main_state.main_ui.draw()
    main_state.money.draw()
    for main_state2.swallow in main_state2.birds:
        main_state2.swallow.draw()
    getbird.draw()
    main_state.windcursor.image.clip_draw(main_state.windcursor.frame * 30, 0, 30, 45, main_state.movemx, main_state.movemy)
    delay(0.03)
    update_canvas()


def update():
    main_state.windcursor.update()
    if main_state.mx>=246 and main_state.mx<=354 and main_state.my>=106 and main_state.my<=175:
        game_framework.pop_state()

def pause():
    pass


def resume():
    pass
