from Environment import Environment
from Controller import Manual_controller

size = (7,7)
window_pos = (0,0)

controller = Manual_controller()

env = Environment(size,window_pos,controller)

while True:

    env.run()
    senses = env.get_sensors()
    # print(senses)
    print(env.snake.DEATH)
    env.render(block_size=100,framerate=1)