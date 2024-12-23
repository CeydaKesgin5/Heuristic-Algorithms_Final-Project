import random
from typing import List, Tuple, Any, Set

class BinPackingAIS:
    def __init__(self, items: List[int], bin_capacity: int, population_size: int, max_generations: int,
                 clone_rate: float = 0.1, mutation_rate: float = 0.2):
        self.items = items
        self.bin_capacity = bin_capacity
        self.population_size = population_size
        self.max_generations = max_generations
        self.clone_rate = clone_rate
        self.mutation_rate = mutation_rate

    def _initialize_population(self):
        population = []
        for _ in range(self.population_size):
            solution = self._create_individual_solution()
            population.append(solution)
        return population

    def _create_individual_solution(self):
        bins = [[]]  # Start with one empty bin
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
                bins.append([item])
        return bins

    def _clone_and_hypermutate(self, population):
        clones = []
        for solution in population:
            if random.random() < self.clone_rate:
                clone = [bin.copy() for bin in solution]
                if random.random() < self.mutation_rate:
                    # Mutation: Move a random item to a different bin or create new bin
                    if len(clone) > 1:
                        source_bin = random.choice(clone)
                        if source_bin:
                            item = random.choice(source_bin)
                            source_bin.remove(item)
                            target_bin = random.choice(clone)
                            if sum(target_bin) + item <= self.bin_capacity:
                                target_bin.append(item)
                            else:
                                clone.append([item])
                clones.append(clone)
        return population + clones

    def _select_population(self, population):
        # Sort by fitness (number of bins) and keep the best solutions
        population.sort(key=lambda x: len([bin for bin in x if bin]))
        return population[:self.population_size]

    def _evaluate_solution(self, solution):
        return len([bin for bin in solution if bin])

    def run(self):
        print(f"Bin Packing AIS Configuration:")
        print(f"  Items: {self.items}")
        print(f"  Bin Capacity: {self.bin_capacity}")
        print(f"  Population Size: {self.population_size}")
        print(f"  Maximum Generations: {self.max_generations}")
        
        population = self._initialize_population()
        best_solution = min(population, key=self._evaluate_solution)
        best_fitness = self._evaluate_solution(best_solution)
        
        for generation in range(self.max_generations):
            population = self._clone_and_hypermutate(population)
            population = self._select_population(population)
            
            current_best = min(population, key=self._evaluate_solution)
            current_fitness = self._evaluate_solution(current_best)
            
            if current_fitness < best_fitness:
                best_solution = current_best
                best_fitness = current_fitness
        
        print(f"Best Bin Packing Solution:")
        print(f"  Bin assignments: {best_solution}")
        print(f"  Number of bins used: {best_fitness}")
        print("-" * 50)
        return best_solution, best_fitness

class SetCoverAIS:
    def __init__(self, universe: Set, subsets: List[Set], population_size: int, max_generations: int,
                 clone_rate: float = 0.1, mutation_rate: float = 0.2):
        self.universe = universe
        self.subsets = subsets
        self.population_size = population_size
        self.max_generations = max_generations
        self.clone_rate = clone_rate
        self.mutation_rate = mutation_rate

    def _initialize_population(self):
        population = []
        for _ in range(self.population_size):
            solution = self._create_individual_solution()
            population.append(solution)
        return population

    def _create_individual_solution(self):
        selected_subsets = []
        covered_elements = set()
        available_subsets = list(range(len(self.subsets)))
        
        while covered_elements != self.universe and available_subsets:
            subset_idx = random.choice(available_subsets)
            selected_subsets.append(subset_idx)
            covered_elements.update(self.subsets[subset_idx])
            available_subsets.remove(subset_idx)
            
        return selected_subsets

    def _clone_and_hypermutate(self, population):
        clones = []
        for solution in population:
            if random.random() < self.clone_rate:
                clone = solution.copy()
                if random.random() < self.mutation_rate:
                    # Mutation: Add or remove a random subset
                    if random.random() < 0.5 and len(clone) > 1:
                        clone.remove(random.choice(clone))
                    else:
                        available = set(range(len(self.subsets))) - set(clone)
                        if available:
                            clone.append(random.choice(list(available)))
                clones.append(clone)
        return population + clones

    def _is_valid_solution(self, solution):
        covered = set()
        for idx in solution:
            covered.update(self.subsets[idx])
        return covered == self.universe

    def _select_population(self, population):
        # Filter valid solutions and sort by size
        valid_solutions = [sol for sol in population if self._is_valid_solution(sol)]
        if not valid_solutions:
            return population[:self.population_size]
        valid_solutions.sort(key=len)
        return valid_solutions[:self.population_size]

    def run(self):
        print(f"Set Cover AIS Configuration:")
        print(f"  Universe: {self.universe}")
        print(f"  Subsets: {self.subsets}")
        print(f"  Population Size: {self.population_size}")
        print(f"  Maximum Generations: {self.max_generations}")
        
        population = self._initialize_population()
        best_solution = min((sol for sol in population if self._is_valid_solution(sol)),
                          key=len, default=population[0])
        
        for generation in range(self.max_generations):
            population = self._clone_and_hypermutate(population)
            population = self._select_population(population)
            
            current_best = min((sol for sol in population if self._is_valid_solution(sol)),
                             key=len, default=population[0])
            
            if len(current_best) < len(best_solution) and self._is_valid_solution(current_best):
                best_solution = current_best
        
        print(f"Best Set Cover Solution:")
        print(f"  Selected subsets: {best_solution}")
        print(f"  Number of subsets used: {len(best_solution)}")
        print("-" * 50)
        return best_solution

class KnapsackAIS:
    def __init__(self, items: List[Tuple[int, int]], capacity: int, population_size: int,
                 max_generations: int, clone_rate: float = 0.1, mutation_rate: float = 0.2):
        self.items = items
        self.capacity = capacity
        self.population_size = population_size
        self.max_generations = max_generations
        self.clone_rate = clone_rate
        self.mutation_rate = mutation_rate

    def _initialize_population(self):
        population = []
        for _ in range(self.population_size):
            solution = self._create_individual_solution()
            population.append(solution)
        return population

    def _create_individual_solution(self):
        solution = []
        current_weight = 0
        items_indices = list(range(len(self.items)))
        random.shuffle(items_indices)
        
        for idx in items_indices:
            weight, _ = self.items[idx]
            if current_weight + weight <= self.capacity:
                solution.append(idx)
                current_weight += weight
        
        return solution

    def _clone_and_hypermutate(self, population):
        clones = []
        for solution in population:
            if random.random() < self.clone_rate:
                clone = solution.copy()
                if random.random() < self.mutation_rate:
                    # Mutation: Add or remove an item
                    if random.random() < 0.5 and clone:
                        clone.remove(random.choice(clone))
                    else:
                        available = set(range(len(self.items))) - set(clone)
                        if available:
                            new_item = random.choice(list(available))
                            if self._get_weight(clone + [new_item]) <= self.capacity:
                                clone.append(new_item)
                clones.append(clone)
        return population + clones

    def _get_weight(self, solution):
        return sum(self.items[idx][0] for idx in solution)

    def _get_value(self, solution):
        return sum(self.items[idx][1] for idx in solution)

    def _select_population(self, population):
        # Filter valid solutions and sort by value
        valid_solutions = [sol for sol in population if self._get_weight(sol) <= self.capacity]
        valid_solutions.sort(key=self._get_value, reverse=True)
        return valid_solutions[:self.population_size]

    def run(self):
        print(f"Knapsack AIS Configuration:")
        print(f"  Items: {self.items}")
        print(f"  Capacity: {self.capacity}")
        print(f"  Population Size: {self.population_size}")
        print(f"  Maximum Generations: {self.max_generations}")
        
        population = self._initialize_population()
        best_solution = max(population, key=self._get_value)
        best_value = self._get_value(best_solution)
        
        for generation in range(self.max_generations):
            population = self._clone_and_hypermutate(population)
            population = self._select_population(population)
            
            current_best = max(population, key=self._get_value)
            current_value = self._get_value(current_best)
            
            if current_value > best_value:
                best_solution = current_best
                best_value = current_value
        
        best_weight = self._get_weight(best_solution)
        print(f"Best Knapsack Solution:")
        print(f"  Selected items: {best_solution}")
        print(f"  Total weight: {best_weight}")
        print(f"  Total value: {best_value}")
        print("-" * 50)
        return best_solution, best_value

class JobSchedulingAIS:
    def __init__(self, job_durations: List[int], population_size: int, max_generations: int,
                 clone_rate: float = 0.1, mutation_rate: float = 0.2):
        self.job_durations = job_durations
        self.population_size = population_size
        self.max_generations = max_generations
        self.clone_rate = clone_rate
        self.mutation_rate = mutation_rate

    def _initialize_population(self):
        population = []
        for _ in range(self.population_size):
            solution = self._create_individual_solution()
            population.append(solution)
        return population

    def _create_individual_solution(self):
        solution = list(range(len(self.job_durations)))
        random.shuffle(solution)
        return solution

    def _clone_and_hypermutate(self, population):
        clones = []
        for solution in population:
            if random.random() < self.clone_rate:
                clone = solution.copy()
                if random.random() < self.mutation_rate:
                    # Mutation: Swap two random jobs
                    idx1, idx2 = random.sample(range(len(clone)), 2)
                    clone[idx1], clone[idx2] = clone[idx2], clone[idx1]
                clones.append(clone)
        return population + clones

    def _get_completion_time(self, solution):
        completion_time = 0
        for job_idx in solution:
            completion_time += self.job_durations[job_idx]
        return completion_time

    def _select_population(self, population):
        # Sort by completion time (minimize)
        population.sort(key=self._get_completion_time)
        return population[:self.population_size]

    def run(self):
        print(f"Job Scheduling AIS Configuration:")
        print(f"  Job Durations: {self.job_durations}")
        print(f"  Population Size: {self.population_size}")
        print(f"  Maximum Generations: {self.max_generations}")
        
        population = self._initialize_population()
        best_solution = min(population, key=self._get_completion_time)
        best_completion_time = self._get_completion_time(best_solution)
        
        for generation in range(self.max_generations):
            population = self._clone_and_hypermutate(population)
            population = self._select_population(population)
            
            current_best = min(population, key=self._get_completion_time)
            current_completion_time = self._get_completion_time(current_best)
            
            if current_completion_time < best_completion_time:
                best_solution = current_best
                best_completion_time = current_completion_time
        
        print(f"Best Job Scheduling Solution:")
        print(f"  Job order: {best_solution}")
        print(f"  Completion time: {best_completion_time}")
        print("-" * 50)
        return best_solution, best_completion_time

if __name__ == "__main__":
    # Test Bin Packing
    items = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
    bin_capacity = 100
    population_size = 50
    max_generations = 500
    bin_packing = BinPackingAIS(items, bin_capacity, population_size, max_generations)
    bin_packing.run()

    # Test Set Cover
    universe = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}
    subsets = [{1, 2, 3}, {2, 3, 4}, {4, 5, 6}, {6, 7, 8}, {8, 9, 10}, {10, 11, 12}, {13, 14, 15}]
    set_cover = SetCoverAIS(universe, subsets, population_size, max_generations)
    set_cover.run()

    # Test Knapsack with more items and values
    items_knapsack = [
        (10, 60), (22, 100), (31, 120), (15, 150), (26, 200), (85, 250), (3, 300), (54, 350),
        (40, 120), (70, 180), (55, 140), (45, 200), (65, 210), (30, 170), (80, 280), (60, 220),
        (5, 90), (35, 150), (50, 180), (75, 260), (20, 110), (90, 310), (95, 320), (12, 130),
        (72, 230), (100, 350), (55, 190), (68, 270), (85, 300), (42, 150), (88, 260), (92, 310),
        (25, 140), (47, 170), (67, 240), (85, 290), (93, 330), (60, 200), (43, 160), (99, 370),
        (29, 130), (95, 310), (77, 280), (62, 250), (49, 180), (60, 170), (73, 290), (80, 320)
    ]
    knapsack_capacity = 560
    knapsack = KnapsackAIS(items_knapsack, knapsack_capacity, population_size, max_generations)
    knapsack.run()

    # Test Job Scheduling with more job durations
    job_durations = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
    job_scheduling = JobSchedulingAIS(job_durations, population_size, max_generations)
    job_scheduling.run()