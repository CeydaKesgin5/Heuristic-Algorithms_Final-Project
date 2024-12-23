import random
from typing import List, Tuple, Any, Set

class BinPackingABC:
    def __init__(self, items: List[int], bin_capacity: int, num_bees: int, max_iterations: int):
        self.items = items
        self.bin_capacity = bin_capacity
        self.num_bees = num_bees
        self.max_iterations = max_iterations

    def _initialize_population(self):
        print("\nInitialization Phase:")
        population = []
        for i in range(self.num_bees):
            bins = [[] for _ in range(len(self.items))]
            items_copy = self.items.copy()
            random.shuffle(items_copy)
            
            for item in items_copy:
                placed = False
                for bin in bins:
                    if sum(bin) + item <= self.bin_capacity:
                        bin.append(item)
                        placed = True
                        break
                if not placed:
                    for bin in bins:
                        if not bin:
                            bin.append(item)
                            break
            
            bins = [bin for bin in bins if bin]
            population.append(bins)
            print(f"  Bee {i+1}: {len(bins)} bins, Items per bin: {[len(b) for b in bins]}")
        return population

    def _employed_bees_phase(self, population: List[Any]):
        print("\nEmployed Bees Phase:")
        new_population = []
        for i, solution in enumerate(population):
            new_solution = [bin.copy() for bin in solution]
            if len(new_solution) >= 2:
                bin1, bin2 = random.sample(range(len(new_solution)), 2)
                if new_solution[bin1] and new_solution[bin2]:
                    item1 = random.choice(new_solution[bin1])
                    item2 = random.choice(new_solution[bin2])
                    bin1_sum = sum(new_solution[bin1]) - item1 + item2
                    bin2_sum = sum(new_solution[bin2]) - item2 + item1
                    if bin1_sum <= self.bin_capacity and bin2_sum <= self.bin_capacity:
                        new_solution[bin1].remove(item1)
                        new_solution[bin2].remove(item2)
                        new_solution[bin1].append(item2)
                        new_solution[bin2].append(item1)
            print(f"  Bee {i+1}: {len(new_solution)} bins")
            new_population.append(new_solution)
        return new_population

    def _onlooker_bees_phase(self, population: List[Any]):
        print("\nOnlooker Bees Phase:")
        new_population = []
        for i, solution in enumerate(population):
            new_solution = [bin.copy() for bin in solution]
            if len(new_solution) >= 2:
                bin1, bin2 = random.sample(range(len(new_solution)), 2)
                if sum(new_solution[bin1]) + sum(new_solution[bin2]) <= self.bin_capacity:
                    new_solution[bin1].extend(new_solution[bin2])
                    new_solution.pop(bin2)
            print(f"  Onlooker {i+1}: {len(new_solution)} bins")
            new_population.append(new_solution)
        return new_population

    def _scout_bee_phase(self, population: List[Any]):
        print("\nScout Bees Phase:")
        new_population = []
        scouts = 0
        for solution in population:
            if random.random() < 0.1:
                new_solution = self._initialize_population()[0]
                new_population.append(new_solution)
                scouts += 1
            else:
                new_population.append(solution)
        print(f"  {scouts} scouts found new solutions")
        return new_population

    def _evaluate_solution(self, solution):
        return len(solution)

    def run(self):
        print("\n=== Bin Packing ABC Algorithm ===")
        print(f"Items: {self.items}")
        print(f"Bin Capacity: {self.bin_capacity}")
        print(f"Bees: {self.num_bees}, Iterations: {self.max_iterations}")
        
        population = self._initialize_population()
        best_solution = min(population, key=self._evaluate_solution)
        best_fitness = self._evaluate_solution(best_solution)
        
        for iteration in range(self.max_iterations):
            print(f"\nIteration {iteration + 1}:")
            population = self._employed_bees_phase(population)
            population = self._onlooker_bees_phase(population)
            population = self._scout_bee_phase(population)
            
            current_best = min(population, key=self._evaluate_solution)
            current_fitness = self._evaluate_solution(current_best)
            if current_fitness < best_fitness:
                best_solution = current_best
                best_fitness = current_fitness
                print(f"New best solution: {best_fitness} bins")
        
        print("\nFinal Best Solution:")
        print(f"Number of bins: {best_fitness}")
        for i, bin in enumerate(best_solution):
            print(f"Bin {i+1}: sum={sum(bin)}, items={bin}")
        return best_solution, best_fitness

class SetCoverABC:
    def __init__(self, universe: Set[int], subsets: List[Set[int]], num_bees: int, max_iterations: int):
        self.universe = universe
        self.subsets = subsets
        self.num_bees = num_bees
        self.max_iterations = max_iterations

    def _create_solution(self):
        solution = set()
        uncovered = self.universe.copy()
        available_subsets = list(range(len(self.subsets)))
        
        while uncovered and available_subsets:
            subset_idx = random.choice(available_subsets)
            subset = self.subsets[subset_idx]
            if not subset.isdisjoint(uncovered):
                solution.add(subset_idx)
                uncovered -= subset
            available_subsets.remove(subset_idx)
        return solution

    def _initialize_population(self):
        print("\nInitialization Phase:")
        population = []
        for i in range(self.num_bees):
            solution = self._create_solution()
            population.append(solution)
            print(f"  Bee {i+1}: {len(solution)} subsets")
        return population

    def _employed_bees_phase(self, population: List[Set[int]]):
        print("\nEmployed Bees Phase:")
        new_population = []
        for i, solution in enumerate(population):
            new_solution = solution.copy()
            if random.random() < 0.5 and new_solution:
                subset_to_remove = random.choice(list(new_solution))
                new_solution.remove(subset_to_remove)
                uncovered = self.universe - set.union(*[self.subsets[idx] for idx in new_solution])
                while uncovered:
                    available = set(range(len(self.subsets))) - new_solution
                    if not available:
                        break
                    new_subset = random.choice(list(available))
                    new_solution.add(new_subset)
                    uncovered = self.universe - set.union(*[self.subsets[idx] for idx in new_solution])
            print(f"  Bee {i+1}: {len(new_solution)} subsets")
            new_population.append(new_solution)
        return new_population

    def _onlooker_bees_phase(self, population: List[Set[int]]):
        print("\nOnlooker Bees Phase:")
        new_population = []
        for i, solution in enumerate(population):
            new_solution = solution.copy()
            if len(new_solution) >= 2:
                subset1, subset2 = random.sample(list(new_solution), 2)
                combined_coverage = self.subsets[subset1] | self.subsets[subset2]
                for idx in range(len(self.subsets)):
                    if idx not in new_solution and self.subsets[idx].issuperset(combined_coverage):
                        new_solution.remove(subset1)
                        new_solution.remove(subset2)
                        new_solution.add(idx)
                        break
            print(f"  Onlooker {i+1}: {len(new_solution)} subsets")
            new_population.append(new_solution)
        return new_population

    def _scout_bee_phase(self, population: List[Set[int]]):
        print("\nScout Bees Phase:")
        new_population = []
        scouts = 0
        for solution in population:
            if random.random() < 0.1:
                new_solution = self._create_solution()
                new_population.append(new_solution)
                scouts += 1
            else:
                new_population.append(solution)
        print(f"  {scouts} scouts found new solutions")
        return new_population

    def run(self):
        print("\n=== Set Cover ABC Algorithm ===")
        print(f"Universe: {self.universe}")
        print(f"Subsets: {self.subsets}")
        print(f"Bees: {self.num_bees}, Iterations: {self.max_iterations}")
        
        population = self._initialize_population()
        best_solution = min(population, key=len)
        best_fitness = len(best_solution)
        
        for iteration in range(self.max_iterations):
            print(f"\nIteration {iteration + 1}:")
            population = self._employed_bees_phase(population)
            population = self._onlooker_bees_phase(population)
            population = self._scout_bee_phase(population)
            
            current_best = min(population, key=len)
            current_fitness = len(current_best)
            if current_fitness < best_fitness:
                best_solution = current_best
                best_fitness = current_fitness
                print(f"New best solution: {best_fitness} subsets")
        
        print("\nFinal Best Solution:")
        print(f"Number of subsets: {best_fitness}")
        print(f"Selected subsets: {best_solution}")
        print(f"Coverage: {set.union(*[self.subsets[idx] for idx in best_solution])}")
        return best_solution, best_fitness

class KnapsackABC:
    def __init__(self, items: List[Tuple[int, int]], capacity: int, num_bees: int, max_iterations: int):
        self.items = items  # (weight, value) tuples
        self.capacity = capacity
        self.num_bees = num_bees
        self.max_iterations = max_iterations

    def _create_solution(self):
        solution = set()
        current_weight = 0
        items_indices = list(range(len(self.items)))
        random.shuffle(items_indices)
        
        for idx in items_indices:
            weight = self.items[idx][0]
            if current_weight + weight <= self.capacity:
                solution.add(idx)
                current_weight += weight
        return solution

    def _initialize_population(self):
        print("\nInitialization Phase:")
        population = []
        for i in range(self.num_bees):
            solution = self._create_solution()
            population.append(solution)
            value = sum(self.items[idx][1] for idx in solution)
            weight = sum(self.items[idx][0] for idx in solution)
            print(f"  Bee {i+1}: value={value}, weight={weight}")
        return population

    def _employed_bees_phase(self, population: List[Set[int]]):
        print("\nEmployed Bees Phase:")
        new_population = []
        for i, solution in enumerate(population):
            new_solution = solution.copy()
            if random.random() < 0.5:
                if new_solution:
                    item_to_remove = random.choice(list(new_solution))
                    new_solution.remove(item_to_remove)
                available_items = set(range(len(self.items))) - new_solution
                if available_items:
                    current_weight = sum(self.items[idx][0] for idx in new_solution)
                    for item in random.sample(list(available_items), min(3, len(available_items))):
                        if current_weight + self.items[item][0] <= self.capacity:
                            new_solution.add(item)
                            current_weight += self.items[item][0]
            value = sum(self.items[idx][1] for idx in new_solution)
            print(f"  Bee {i+1}: value={value}")
            new_population.append(new_solution)
        return new_population

    def _onlooker_bees_phase(self, population: List[Set[int]]):
        print("\nOnlooker Bees Phase:")
        new_population = []
        fitness_values = [sum(self.items[idx][1] for idx in solution) for solution in population]
        total_fitness = sum(fitness_values)
        probabilities = [f/total_fitness for f in fitness_values] if total_fitness > 0 else [1/len(population)]*len(population)
        
        for i in range(len(population)):
            selected_idx = random.choices(range(len(population)), probabilities)[0]
            new_solution = population[selected_idx].copy()
            value = sum(self.items[idx][1] for idx in new_solution)
            print(f"  Onlooker {i+1}: value={value}")
            new_population.append(new_solution)
        return new_population

    def _scout_bee_phase(self, population: List[Set[int]]):
        print("\nScout Bees Phase:")
        new_population = []
        scouts = 0
        for solution in population:
            if random.random() < 0.1:
                new_solution = self._create_solution()
                new_population.append(new_solution)
                scouts += 1
            else:
                new_population.append(solution)
        print(f"  {scouts} scouts found new solutions")
        return new_population

    def run(self):
        print("\n=== Knapsack ABC Algorithm ===")
        print(f"Items (weight, value): {self.items}")
        print(f"Capacity: {self.capacity}")
        print(f"Bees: {self.num_bees}, Iterations: {self.max_iterations}")
        
        population = self._initialize_population()
        best_solution = max(population, key=lambda s: sum(self.items[idx][1] for idx in s))
        best_fitness = sum(self.items[idx][1] for idx in best_solution)
        
        for iteration in range(self.max_iterations):
            print(f"\nIteration {iteration + 1}:")
            population = self._employed_bees_phase(population)
            population = self._onlooker_bees_phase(population)
            population = self._scout_bee_phase(population)
            
            current_best = max(population, key=lambda s: sum(self.items[idx][1] for idx in s))
            current_fitness = sum(self.items[idx][1] for idx in current_best)
            if current_fitness > best_fitness:
                best_solution = current_best
                best_fitness = current_fitness
                print(f"New best solution: value={best_fitness}")
        
        print("\nFinal Best Solution:")
        print(f"Total value: {best_fitness}")
        print(f"Total weight: {sum(self.items[idx][0] for idx in best_solution)}")
        print(f"Selected items: {[(idx, self.items[idx]) for idx in best_solution]}")
        return best_solution, best_fitness

class JobSchedulingABC:
    def __init__(self, job_durations: List[int], num_bees: int, max_iterations: int):
        self.job_durations = job_durations
        self.num_bees = num_bees
        self.max_iterations = max_iterations

    def _create_solution(self):
        solution = list(range(len(self.job_durations)))
        random.shuffle(solution)
        return solution

    def _initialize_population(self):
        print("\nInitialization Phase:")
        population = []
        for i in range(self.num_bees):
            solution = self._create_solution()
            population.append(solution)
            completion_time = self._evaluate_solution(solution)
            print(f"  Bee {i+1}: completion time={completion_time}")
        return population

    def _evaluate_solution(self, solution):
        completion_time = 0
        for job_idx in solution:
            completion_time += self.job_durations[job_idx]
        return completion_time

    def _employed_bees_phase(self, population: List[List[int]]):
        print("\nEmployed Bees Phase:")
        new_population = []
        for i, solution in enumerate(population):
            new_solution = solution.copy()
            # Swap two random jobs
            if len(new_solution) >= 2:
                idx1, idx2 = random.sample(range(len(new_solution)), 2)
                new_solution[idx1], new_solution[idx2] = new_solution[idx2], new_solution[idx1]
            completion_time = self._evaluate_solution(new_solution)
            print(f"  Bee {i+1}: completion time={completion_time}")
            new_population.append(new_solution)
        return new_population

    def _onlooker_bees_phase(self, population: List[List[int]]):
        print("\nOnlooker Bees Phase:")
        new_population = []
        fitness_values = [1/self._evaluate_solution(solution) for solution in population]
        total_fitness = sum(fitness_values)
        probabilities = [f/total_fitness for f in fitness_values]
        
        for i in range(len(population)):
            selected_idx = random.choices(range(len(population)), probabilities)[0]
            new_solution = population[selected_idx].copy()
            # Try to improve by reversing a subsequence
            if len(new_solution) >= 2:
                start = random.randint(0, len(new_solution)-2)
                end = random.randint(start+1, len(new_solution))
                new_solution[start:end] = reversed(new_solution[start:end])
            completion_time = self._evaluate_solution(new_solution)
            print(f"  Onlooker {i+1}: completion time={completion_time}")
            new_population.append(new_solution)
        return new_population

    def _scout_bee_phase(self, population: List[List[int]]):
        print("\nScout Bees Phase:")
        new_population = []
        scouts = 0
        for solution in population:
            if random.random() < 0.1:
                new_solution = self._create_solution()
                new_population.append(new_solution)
                scouts += 1
            else:
                new_population.append(solution)
        print(f"  {scouts} scouts found new solutions")
        return new_population

    def run(self):
        print("\n=== Job Scheduling ABC Algorithm ===")
        print(f"Job durations: {self.job_durations}")
        print(f"Bees: {self.num_bees}, Iterations: {self.max_iterations}")
        
        population = self._initialize_population()
        best_solution = min(population, key=self._evaluate_solution)
        best_fitness = self._evaluate_solution(best_solution)
        
        for iteration in range(self.max_iterations):
            print(f"\nIteration {iteration + 1}:")
            population = self._employed_bees_phase(population)
            population = self._onlooker_bees_phase(population)
            population = self._scout_bee_phase(population)
            
            current_best = min(population, key=self._evaluate_solution)
            current_fitness = self._evaluate_solution(current_best)
            if current_fitness < best_fitness:
                best_solution = current_best
                best_fitness = current_fitness
                print(f"New best solution: completion time={best_fitness}")
        
        print("\nFinal Best Solution:")
        print(f"Job sequence: {best_solution}")
        print(f"Job durations: {[self.job_durations[i] for i in best_solution]}")
        print(f"Total completion time: {best_fitness}")
        return best_solution, best_fitness

# Test runs for all algorithms
def run_all_tests():
    print("Running tests for all ABC algorithms...")
    print("=" * 50)

    num_bees = 30
    max_iterations = 500

    # # Test 1: Bin Packing
    # print("\nTest 1: Bin Packing Problem")
    # items = [5, 10, 15, 20, 25]
    # bin_capacity = 30
    # bin_packing = BinPackingABC(items, bin_capacity, num_bees, max_iterations)
    # bin_packing.run()

    # # Test 2: Set Cover
    # print("\nTest 2: Set Cover Problem")
    # universe = {1, 2, 3, 4, 5}
    # subsets = [{1, 2}, {2, 3}, {3, 4}, {4, 5}, {1, 5}]
    # set_cover = SetCoverABC(universe, subsets, num_bees, max_iterations)
    # set_cover.run()

    # Test 3: Knapsack
    # print("\nTest 3: Knapsack Problem")
    # items = [
    #         (10, 60), (22, 100), (31, 120), (15, 150), (26, 200), (85, 250), (3, 300), (54, 350),
    #         (40, 120), (70, 180), (55, 140), (45, 200), (65, 210), (30, 170), (80, 280), (60, 220),
    #         (5, 90), (35, 150), (50, 180), (75, 260), (20, 110), (90, 310), (95, 320), (12, 130),
    #         (72, 230), (100, 350), (55, 190), (68, 270), (85, 300), (42, 150), (88, 260), (92, 310),
    #         (25, 140), (47, 170), (67, 240), (85, 290), (93, 330), (60, 200), (43, 160), (99, 370),
    #         (29, 130), (95, 310), (77, 280), (62, 250), (49, 180), (60, 170), (73, 290), (80, 320)
    # ]    
    # capacity = 510
    # knapsack = KnapsackABC(items, capacity, num_bees, max_iterations)
    # knapsack.run()

    # Test 4: Job Scheduling
    print("\nTest 4: Job Scheduling Problem")
    job_durations = [2, 3, 4, 5, 6]
    job_scheduling = JobSchedulingABC(job_durations, num_bees, max_iterations)
    job_scheduling.run()

if __name__ == "__main__":
    run_all_tests()