from gym import Env
from gym.spaces import Discrete, Box

from Environment import Environment
from Controller import Neural_controller


class GymEnv(Env):
    def __init__(self):
        size = (15,15)
        window_pos = (0,0)
        controller = Neural_controller()
        self.env = Environment(size,window_pos,controller)

    def step(self):
        senses = env.get_sensors()
        controller.predict(senses)
        self.env.run()
        state = self.env.snake.pos
        done = False
        reward = 0
        if self.env.snake.food_eaten():
            reward = 1
        if self.env.snake.DEATH:
            reward = -1
            done = True
        info = {}
        return state,reward,done,info

    def render(self):
        self.env.render(30,15)
    def reset(self):
        self.env.reset()

env = GymEnv()
check_env(env)


actions = Discrete(3)
