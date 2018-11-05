import game_framework
import main_state
import main_state2
from pico2d import *


name = "PauseState"
image = None
logo_time = 0.0

def enter():
    global image
    image = load_image('pause.png')


def exit():
    global image
    del(image)


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_p):
                game_framework.pop_state()


def draw():
    clear_canvas()

    if logo_time == 1:
        image.draw(400, 300)

    main_state.grass.draw()
    main_state.boy.draw()
    update_canvas()


def update():
    global logo_time

    if (logo_time > 1):
        logo_time = 0
        # game_framework.quit()

    delay(0.5)
    logo_time += 1


def pause():
    pass


def resume():
    pass
