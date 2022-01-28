from Environment import Environment
from Controller import Manual_controller, Random_controller, Neural_controller
import time
from keras.models import load_model

size = (15,15)
window_pos = (0,0)

# controller = Manual_controller()
# controller = Random_controller()
controller = Neural_controller()

env = Environment(size,window_pos,controller)

m = load_model('20.h5')
w = m.get_weights()
controller.set_weights(w)

while True:
    env.run()
    senses = env.get_sensors()
    controller.predict(senses)

    env.render(block_size=50,framerate=2)


