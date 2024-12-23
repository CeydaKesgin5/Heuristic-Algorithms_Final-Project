import random

# 1. Job Scheduling Problem
def job_scheduling_tabu(job_times, num_machines, num_iterations, tabu_size):
    def evaluate(schedule):
        return max([sum(job_times[job] for job in machine) for machine in schedule])

    def generate_neighbors(schedule):
        neighbors = []
        for i in range(len(schedule)):
            if schedule[i]:
                for j in range(len(schedule)):
                    if i != j:
                        new_schedule = [machine[:] for machine in schedule]
                        new_schedule[j].append(new_schedule[i].pop(0))
                        neighbors.append(new_schedule)
        return neighbors

    schedule = [[] for _ in range(num_machines)]
    for i, job_time in enumerate(job_times):
        schedule[i % num_machines].append(i)

    tabu_list = []
    best_schedule = schedule
    best_score = evaluate(schedule)
    history = []
    population = [schedule]

    for iteration in range(num_iterations):
        neighbors = generate_neighbors(schedule)
        neighbors_scores = [(evaluate(n), n) for n in neighbors]
        neighbors_scores.sort(key=lambda x: x[0])

        for score, candidate in neighbors_scores:
            if candidate not in tabu_list or score < best_score:
                schedule = candidate
                if score < best_score:
                    best_schedule = candidate
                    best_score = score
                break

        tabu_list.append(schedule)
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

        population.append(schedule)
        history.append((iteration, [[job_times[job] for job in machine] for machine in schedule], best_score))

    return history, population

# 2. Knapsack Problem
def knapsack_tabu(values, weights, capacity, num_iterations, tabu_size):
    def evaluate(solution):
        total_value = sum(v for v, s in zip(values, solution) if s)
        total_weight = sum(w for w, s in zip(weights, solution) if s)
        return total_value if total_weight <= capacity else 0

    def generate_neighbors(solution):
        neighbors = []
        for i in range(len(solution)):
            neighbor = solution[:]
            neighbor[i] = 1 - neighbor[i]
            neighbors.append(neighbor)
        return neighbors

    solution = [random.randint(0, 1) for _ in range(len(values))]
    tabu_list = []
    best_solution = solution
    best_score = evaluate(solution)
    history = []
    population = [solution]

    for iteration in range(num_iterations):
        neighbors = generate_neighbors(solution)
        neighbors_scores = [(evaluate(n), n) for n in neighbors]
        neighbors_scores.sort(key=lambda x: x[0], reverse=True)

        for score, candidate in neighbors_scores:
            if candidate not in tabu_list or score > best_score:
                solution = candidate
                if score > best_score:
                    best_solution = candidate
                    best_score = score
                break

        tabu_list.append(solution)
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

        population.append(solution)
        history.append((iteration, solution, {
            "selected_items": [i for i, s in enumerate(solution) if s],
            "total_value": sum(v for v, s in zip(values, solution) if s),
            "total_weight": sum(w for w, s in zip(weights, solution) if s)
        }))

    return history, population

# 3. Bin Packing Problem
def bin_packing_tabu(items, bin_capacity, num_iterations, tabu_size):
    def evaluate(bins):
        return len(bins)

    def generate_neighbors(bins):
        neighbors = []
        for i in range(len(bins)):
            if bins[i]:
                for j in range(len(bins)):
                    if i != j and sum(bins[j]) + bins[i][0] <= bin_capacity:
                        new_bins = [b[:] for b in bins]
                        new_bins[j].append(new_bins[i].pop(0))
                        neighbors.append(new_bins)
        return neighbors

    bins = [[]]
    for item in items:
        placed = False
        for bin in bins:
            if sum(bin) + item <= bin_capacity:
                bin.append(item)
                placed = True
                break
        if not placed:
            bins.append([item])

    tabu_list = []
    best_bins = bins
    best_score = evaluate(bins)
    history = []
    population = [bins]

    for iteration in range(num_iterations):
        neighbors = generate_neighbors(bins)
        neighbors_scores = [(evaluate(n), n) for n in neighbors]
        neighbors_scores.sort(key=lambda x: x[0])

        for score, candidate in neighbors_scores:
            if candidate not in tabu_list or score < best_score:
                bins = candidate
                if score < best_score:
                    best_bins = candidate
                    best_score = score
                break

        tabu_list.append(bins)
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

        population.append(bins)
        history.append((iteration, bins, best_score))

    return history, population

# 4. Set Cover Problem
def set_cover_tabu(universe, subsets, num_iterations, tabu_size):
    def evaluate(solution):
        covered = set()
        for i, s in enumerate(solution):
            if s:
                covered.update(subsets[i])
        return len(universe - covered)

    def generate_neighbors(solution):
        neighbors = []
        for i in range(len(solution)):
            neighbor = solution[:]
            neighbor[i] = 1 - neighbor[i]
            neighbors.append(neighbor)
        return neighbors

    solution = [random.randint(0, 1) for _ in range(len(subsets))]
    tabu_list = []
    best_solution = solution
    best_score = evaluate(solution)
    history = []
    population = [solution]

    for iteration in range(num_iterations):
        neighbors = generate_neighbors(solution)
        neighbors_scores = [(evaluate(n), n) for n in neighbors]
        neighbors_scores.sort(key=lambda x: x[0])

        for score, candidate in neighbors_scores:
            if candidate not in tabu_list or score < best_score:
                solution = candidate
                if score < best_score:
                    best_solution = candidate
                    best_score = score
                break

        tabu_list.append(solution)
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

        population.append(solution)
        history.append((iteration, solution, {
            "selected_subsets": [i for i, s in enumerate(solution) if s],
            "uncovered_elements": universe - set.union(*[subsets[i] for i, s in enumerate(solution) if s])
        }))

    return history, population

# Test Examples
# Job Scheduling
job_times = [2, 5, 3, 7, 1, 4]
num_machines = 3
job_history, job_population = job_scheduling_tabu(job_times, num_machines, 10, 5)

# Knapsack
data = [
    (10, 60), (22, 100), (31, 120), (15, 150), (26, 200), (85, 250), (3, 300), (54, 350),
    (40, 120), (70, 180), (55, 140), (45, 200), (65, 210), (30, 170), (80, 280), (60, 220),
    (5, 90), (35, 150), (50, 180), (75, 260), (20, 110), (90, 310), (95, 320), (12, 130),
    (72, 230), (100, 350), (55, 190), (68, 270), (85, 300), (42, 150), (88, 260), (92, 310),
    (25, 140), (47, 170), (67, 240), (85, 290), (93, 330), (60, 200), (43, 160), (99, 370),
    (29, 130), (95, 310), (77, 280), (62, 250), (49, 180), (60, 170), (73, 290), (80, 320)
]

# values ve weights listelerini ayır
values = [item[0] for item in data]
weights = [item[1] for item in data]
capacity = 50
knapsack_history, knapsack_population = knapsack_tabu(values, weights, capacity, 10, 5)

# Bin Packing
items = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
bin_capacity = 10
bin_history, bin_population = bin_packing_tabu(items, bin_capacity, 10, 5)

# Set Cover
universe = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}
subsets = [{1, 2, 3}, {2, 3, 4}, {4, 5, 6}, {6, 7, 8}, {8, 9, 10}, {10, 11, 12}, {13, 14, 15}]
set_cover_history, set_cover_population = set_cover_tabu(universe, subsets, 10, 5)

# Extracting best solutions
best_job_schedule = job_history[-1][1]
best_job_max_time = job_history[-1][2]

best_knapsack_solution = knapsack_history[-1][1]
best_knapsack_details = knapsack_history[-1][2]

best_bin_packing = bin_history[-1][1]
best_bin_count = bin_history[-1][2]

best_set_cover_solution = set_cover_history[-1][1]
best_set_cover_details = set_cover_history[-1][2]


# Results
print("Job Scheduling:")
for step in job_history:
    print(f"Iteration {step[0]}: Schedule {step[1]}, Max Time: {step[2]}")
print(f"Best Schedule: {best_job_schedule}, Max Time: {best_job_max_time}")

print("\nKnapsack:")
for step in knapsack_history:
    print(f"Iteration {step[0]}: Solution {step[1]}, Details: {step[2]}")
print(f"Best Solution: {best_knapsack_solution}, Details: {best_knapsack_details}")

print("\nBin Packing:")
for step in bin_history:
    print(f"Iteration {step[0]}: Bins {step[1]}, Total Bins: {step[2]}")
print(f"Best Bins: {best_bin_packing}, Total Bins: {best_bin_count}")


print("\nSet Cover:")
for step in set_cover_history:
    print(f"Iteration {step[0]}: Solution {step[1]}, Details: {step[2]}")
print(f"Best Solution: {best_set_cover_solution}, Details: {best_set_cover_details}")


