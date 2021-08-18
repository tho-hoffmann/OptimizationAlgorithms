import time
import random
import math

people = [('Amanda', 'CWB'),
           ('Pedro', 'GIG'),
           ('Marcos', 'POA'),
           ('Priscila', 'FLN'),
           ('Jéssica', 'CNF'),
           ('Paulo', 'GYN')]

destination = 'GRU'

flights = {}

for line in open('../flights.txt'):
    _origin, _destination, _exit, _coming, _price = line.split(',') 
    flights.setdefault((_origin,_destination), [])
    flights[(_origin, _destination)].append((_exit, _coming, int(_price)))

print("_________PRINT_SCHEDULE________")
print("")
def print_schedule(schedule):
    id_flight = -1
    for i in range(len(schedule) // 2):
        name = people[i][0]
        origin = people[i][1]
        id_flight += 1
        go = flights[(origin, destination)][schedule[id_flight]]
        id_flight +=1
        goBack = flights[(destination, origin)][schedule[id_flight]]
        print('%10s%10s %5s-%5s R$%3s %5s-%5s R$%3s' % (name, origin, go[0], go[1], go[2], goBack[0], goBack[1], goBack[2]))

schedule = [1,4, 3,2, 7,3, 6,3, 2,4, 5,3]
print_schedule(schedule)

print("__________GET_MINUTES___________")
print("")
def get_minutes(hour):
    x = time.strptime(hour, '%H:%M')
    # x[3] - return the hour
    # x[4] - return the minutes
    minutes = x[3] * 60 + x[4]
    return minutes

print(get_minutes('6:13'))
print(get_minutes('23:00'))
print(get_minutes('00:00'))

print("___________FUNC_COST_____________")
print("")
def func_cost(solution):
    price_total = 0
    last_coming = 0
    first_exit = 1439

    id_flight = -1
    for i in range(len(solution) // 2):
        origin = people[i][1]
        id_flight += 1
        go = flights[(origin, destination)][solution[id_flight]]
        id_flight += 1
        goBack = flights[(destination, origin)][solution[id_flight]]

        price_total += go[2]
        price_total += goBack[2]

        if last_coming < get_minutes(go[1]):
            last_coming = get_minutes(go[1])

        if first_exit > get_minutes(goBack[0]):
            first_exit = get_minutes(goBack[0])
    
    wait_total = 0
    id_flight = -1
    for i in range(len(solution) // 2):
        origin = people[i][1]
        id_flight += 1
        go = flights[(origin, destination)][solution[id_flight]]
        id_flight += 1
        goBack = flights[(destination, origin)][solution[id_flight]]

        wait_total += last_coming - get_minutes(go[1])
        wait_total += get_minutes(goBack[0]) - first_exit

    if last_coming > first_exit: 
        price_total += 50
    
    return price_total + wait_total

print(func_cost(schedule))

print("__________RANDOM_SEARCH__________")
print("")
# Jump from one side to another

def random_search(domain, func_cost):
    best_cost = 999999999
    for i in range(0, 10000):
        solution = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
        cost = func_cost(solution)
        if cost < best_cost:
            best_cost = cost
            best_solution = solution
    return best_solution

domain = [(0,9)] * (len(people) * 2)

random_solution = random_search(domain, func_cost)
print(random_solution)
random_cost = func_cost(random_solution)
print(random_cost)
print_schedule(random_solution)

print("___________HILL_CLIMB___________")
print("")
# Starts with random solution and looks for the best neighbors

def hill_climb(domain, func_cost):
    solution = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
    while True:
        neighbors = []

        for i in range(len(domain)):
            if solution[i] > domain[i][0]:
                if solution[i] != domain[i][1]:
                    neighbors.append(solution[0:i] + [solution[i] + 1] + solution[i + 1:])
            if solution[i] < domain[i][1]:
                if solution[i] != domain[i][0]:
                    neighbors.append(solution[0:i] + [solution[i] - 1] + solution[i + 1:])
        current = func_cost(solution)
        best = current
        for i in range(len(neighbors)):
            cost = func_cost(neighbors[i])
            if cost < best:
                best = cost
                solution = neighbors[i]
        
        if best == current:
                break
    return solution

hill_climb_solution = hill_climb(domain, func_cost)
print(hill_climb_solution)
hill_climb_cost = func_cost(hill_climb_solution)
print(hill_climb_cost)
print_schedule(hill_climb_solution)

print("______SIMULATED_ANNEALING_______")
print("")
# Starts with the random solution using a variable that represents temperature (high and decreases)  
# If the solution is worse, it can be selected according to some probability
# Move to a worse solution so that the best one is selected

def simulated_annealing(domain, func_cost, temperature = 10000.0, cooling = 0.95, step = 1):
    solution = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
    while temperature > 0.1:
        i = random.randint(0, len(domain) - 1)
        direction = random.randint(-step, step)

        temp_solution = solution[:]
        temp_solution[i] += direction
        if(temp_solution[i] < domain[i][0]):
            temp_solution[i] = domain[i][0]
        elif(temp_solution[i] > domain[i][1]):
            temp_solution[i] = domain[i][1]

        cost_solution = func_cost(solution)
        cost_solution_temp = func_cost(temp_solution)
        probability = pow(math.e, (-cost_solution_temp - cost_solution) / temperature)

        if (cost_solution_temp < cost_solution or random.random() < probability):
            solution = temp_solution

        temperature = temperature * cooling

    return solution

simulated_annealing_solution = simulated_annealing(domain, func_cost)
print(simulated_annealing_solution)
simulated_annealing_cost = func_cost(simulated_annealing_solution)
print(simulated_annealing_cost)
print_schedule(simulated_annealing_solution)

print("____________MUTATION____________")
print("")
# Exchanges a value in the solution (individual) called the gene

def mutation(domain, step, solution):
    i = random.randint(0, len(domain) - 1)
    mutant = solution

    if random.random() < 0.5:
        if solution[i] != domain[i][0]:
            mutant = solution[0:i] + [solution[i] - step] + solution[i + 1:]
    else:
        if solution[i] != domain[i][1]:
            mutant = solution[0:i] + [solution[i] + step] + solution[i + 1:]

    return mutant

s = [1,4, 3,2, 7,3, 6,3, 2,4, 5,3]
mutant_gene = mutation(domain, 1, s)
print(mutant_gene)

print("____________CROSSING____________")
print("")
# Combination of two solutions (two individuals)

def crossing(domain, individual1, individual2):
    i = random.randint(1, len(domain) - 2)
    return individual1[0:i] + individual2[i:]
    
s1 = [1,4, 3,2, 7,3, 6,3, 2,4, 5,3]
s2 = [0,1, 2,5, 8,9, 2,3, 5,1, 0,6]
crossing_solution = crossing(domain, s1, s2)
print(crossing_solution)

print("_____________GENETIC_____________")
print("")

def genetic(domain, func_cost, tam_population = 100, step = 1, probability_mutation = 0.2, elitism = 0.2, num_generation = 500):
    population = []
    for i in range(tam_population):
        solution = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
        population.append(solution)
    
    num_elitism = int(elitism * tam_population)

    for i in range(num_generation):
        costs = [(func_cost(individual), individual) for individual in population]
        costs.sort()
        ordered_individuals = [individual for (cost, individual) in costs]

        population = ordered_individuals[0:num_elitism]

        while len(population) < tam_population:
            if random.random() < probability_mutation:
                m = random.randint(0, num_elitism)
                population.append(mutation(domain, step, ordered_individuals[m]))
            else:
                c1 = random.randint(0, num_elitism)
                c2 = random.randint(0, num_elitism)
                population.append(crossing(domain, ordered_individuals[c1], ordered_individuals[c2]))

    return costs[0][1]

genetic_solution = genetic(domain, func_cost)
print(genetic_solution)
genetic_cost = func_cost(genetic_solution)
print(genetic_cost)
print_schedule(genetic_solution)