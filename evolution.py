from Environment import Environment
from Controller import Neural_controller
from KerasGA import GeneticAlgorithm

size = (15,15)
window_pos = (0,0)
controller = Neural_controller()
env = Environment(size,window_pos,controller)

model = controller.my_model()

population_size = 200
GA = GeneticAlgorithm(model, population_size = population_size, selection_rate = 0.13, mutation_rate = 0.03)
population = GA.initial_population()

epoch = 0
while True:
    scores = []

    for chromosome in population:
        controller.set_weights(chromosome)
        env.reset()
        step = 0
        score = 0
        while True:
            env.run()
            senses = env.get_sensors()
            controller.predict(senses)
            step += 1
            if env.eaten:
                step = 0
                score += 1
            if env.snake.DEATH == True or step == 90:
                if score > 15:
                    model_to_save = controller.my_model()
                    model_to_save.set_weights(chromosome)
                    model_to_save.save(str(score)+'.h5')
                scores.append(score)
                break

            env.render(block_size=30, framerate=9999)

    print(max(scores))

    top_performers = GA.strongest_parents(population, scores)

    pairs = []
    while len(pairs) != GA.population_size:
        pairs.append(GA.pair(top_performers))

    base_offsprings = []
    for pair in pairs:
        offsprings = GA.crossover(pair[0][0], pair[1][0])
        base_offsprings.append(offsprings[-1])

    population = GA.mutation(base_offsprings)

    epoch += 1














