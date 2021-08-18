from flights import random_search, genetic, hill_climb, simulated_annealing

dorms = ['São Paulo', 'Flamengo', 'Coritiba', 'Cruzeiro', 'Fortaleza']
preferences = [('Amanda', ('Cruzeiro', 'Coritiba')),
               ('Pedro', ('São Paulo', 'Fortaleza')),
               ('Marcos', ('Flamengo', 'São Paulo')),
               ('Priscila', ('São Paulo', 'Fortaleza')),
               ('Jessica', ('Flamengo', 'Cruzeiro')), 
               ('Paulo', ('Coritiba', 'Fortaleza')), 
               ('Fred', ('Fortaleza', 'Flamengo')), 
               ('Suzana', ('Cruzeiro', 'Coritiba')), 
               ('Laura', ('Cruzeiro', 'Coritiba')), 
               ('Ricardo', ('Coritiba', 'Flamengo'))]

# [1, 0, 2, 0, 0, 0]
# (0,9), (0,8), (0,7)...(0,0)

domain = [(0, (len(dorms) * 2) -i -1) for i in range(0, len(dorms) * 2)] 

print("")
print("________PRINT_SOLUTION________")

def print_solution(solution):
    options = []
    for i in range(len(dorms)):
        options += [i, i]
    for i in range(len(solution)):
        current = solution[i]
        dorm = dorms[options[current]]
        print(preferences[i][0], dorm)
        del options[current]

print_solution([6,1,2,1,2,0,2,2,0,0])

print("")
print("____________FUNC_COST____________")

def func_cost(solution):
    cost = 0
    options = [0,0,1,1,2,2,3,3,4,4]
    for i in range(len(solution)):
        current = solution[i]
        dorm = dorms[options[current]]
        preference = preferences[i][1]
        if preference[0] == dorm:
            cost += 0
        elif preference[1] == dorm:
            cost +=1
        else:
            cost += 3

        del options[current]

    return cost

cost_solution = func_cost([6,1,2,1,2,0,2,2,0,0])
print(cost_solution)

print("")
print("________RANDOM_SEARCH_________")

random_soluction = random_search(domain, func_cost)
random_cost = func_cost(random_soluction)
print_solution(random_soluction)
print("")
print(random_cost)

print("")
print("__________HILL_CLIMB___________")
hill_climb_soluction = hill_climb(domain, func_cost)
hill_climb_cost = func_cost(hill_climb_soluction)
print_solution(hill_climb_soluction)
print("")
print(hill_climb_cost)

print("")
print("______SIMULATED_ANNEALING______")
annealing_soluction = simulated_annealing(domain, func_cost)
annealing_cost = func_cost(annealing_soluction)
print_solution(annealing_soluction)
print("")
print(annealing_cost)

print("")
print("____________GENETIC____________")
genetic_soluction = genetic(domain, func_cost)
genetic_cost = func_cost(genetic_soluction)
print_solution(genetic_soluction)
print("")
print(genetic_cost)