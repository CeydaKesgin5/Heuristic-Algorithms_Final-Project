


import numpy as np
import random

print("************************************jobscheduling***************************************")

# Problem verileri
jobs = [1, 2, 3]  # İşler
machines = [1, 2]  # Makineler
processing_time = {
    (1, 1): 3, (1, 2): 2,  # İş 1'in işlem süreleri
    (2, 1): 2, (2, 2): 4,  # İş 2'nin işlem süreleri
    (3, 1): 4, (3, 2): 3   # İş 3'ün işlem süreleri
}

# ACO parametreleri
alpha = 1       # Feromon etkisi
beta = 2        # Sezgisel bilginin etkisi
rho = 0.5       # Buharlaşma oranı
num_ants = 20   # Karınca sayısı
num_iterations = 300  # Iterasyon sayısı
Q = 100         # Feromon güncelleme sabiti

# Feromon matrisini başlat
pheromones = {(j, m): 1 for j in jobs for m in machines}

# Sezgisel bilgi (eta) matrisini hesapla
eta = {(j, m): 1 / processing_time[(j, m)] for j in jobs for m in machines}

# İşleri çizelgeleme fonksiyonu
def schedule_jobs():
    solutions = []
    for _ in range(num_ants):
        solution = []
        assigned_jobs = set()
        for _ in range(len(jobs)):
            available_jobs = [j for j in jobs if j not in assigned_jobs]
            probabilities = []

            for j in available_jobs:
                prob = [pheromones[(j, m)]**alpha * eta[(j, m)]**beta for m in machines]
                probabilities.append(sum(prob))

            total_prob = sum(probabilities)
            probabilities = [p / total_prob for p in probabilities]

            selected_job = random.choices(available_jobs, probabilities)[0]
            assigned_jobs.add(selected_job)

            selected_machine = min(machines, key=lambda m: processing_time[(selected_job, m)])
            solution.append((selected_job, selected_machine))

        solutions.append(solution)
    return solutions

# Çözümün toplam tamamlama süresini hesapla
def calculate_makespan(solution):
    machine_times = {m: 0 for m in machines}
    for job, machine in solution:
        machine_times[machine] += processing_time[(job, machine)]
    return max(machine_times.values())

# Feromon güncelleme fonksiyonu
def update_pheromones(solutions):
    global pheromones
    # Feromon buharlaşması
    pheromones = {key: (1 - rho) * value for key, value in pheromones.items()}
    
    # Feromon ekleme
    for solution in solutions:
        makespan = calculate_makespan(solution)
        for job, machine in solution:
            pheromones[(job, machine)] += Q / makespan

# Ana ACO döngüsü
best_solution = None
best_makespan = float('inf')

for iteration in range(num_iterations):
    solutions = schedule_jobs()
    print(f"Iteration {iteration + 1}: Solutions: {solutions}")  # Iterasyon ve çözümleri yazdır
    update_pheromones(solutions)

    for solution in solutions:
        makespan = calculate_makespan(solution)
        if makespan < best_makespan:
            best_makespan = makespan
            best_solution = solution

# Başlangıç feromon matrisini yazdır
print("Initial Pheromone Matrix:", pheromones)

# Sonuçlar
total_time = calculate_makespan(best_solution)
print("En iyi çözüm:", best_solution)
print("Toplam tamamlama süresi (makespan):", total_time)



#binpacking

print("************************************binpacking***************************************")


class Ant:
    def __init__(self, capacity, items):
        self.capacity = capacity
        self.items = items
        self.solution = []
        self.total_bins_used = 0

    def construct_solution(self):
        # Başlangıç kutuları ve geçici nesne listesi
        bins = []
        remaining_items = self.items.copy()
        
        while remaining_items:
            current_bin = []
            current_bin_size = 0
            
            for item in remaining_items[:]:  # Geçici liste
                if current_bin_size + item <= self.capacity:
                    current_bin.append(item)
                    current_bin_size += item
                    remaining_items.remove(item)
                    
            bins.append(current_bin)
        
        self.solution = bins
        self.total_bins_used = len(bins)

def ant_colony_bin_packing(items, bin_capacity, num_ants, num_iterations):
    best_solution = None
    best_bins_used = float('inf')
    
    for iteration in range(num_iterations):
        ants = [Ant(bin_capacity, items) for _ in range(num_ants)]
        solutions = []
        
        for ant in ants:
            ant.construct_solution()
            solutions.append(ant)

        # En iyi çözümü bul
        for ant in solutions:
            if ant.total_bins_used < best_bins_used:
                best_solution = ant.solution
                best_bins_used = ant.total_bins_used
                
        # Sonuçları yazdır
        print(f"Iteration {iteration + 1}: Best bins used = {best_bins_used}, Solution = {best_solution}")

    return best_solution, best_bins_used

# Örnek veri
items = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
bin_capacity = 100
num_ants = 20
num_iterations = 300

best_solution, best_bins_used = ant_colony_bin_packing(items, bin_capacity, num_ants, num_iterations)

print(f"\nFinal Best Solution: {best_solution}")
print(f"Final Best Bins Used: {best_bins_used}")





#setcover
print("************************************setcover***************************************")

universe = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}
subsets = [
    {"set": {1, 2, 3}, "cost": 3},
    {"set": {2, 3, 4}, "cost": 2},
    {"set": {4, 5, 6}, "cost": 4},
    {"set": {6, 7, 8}, "cost": 3},
    {"set": {8, 9, 10}, "cost": 5},
    {"set": {10, 11, 12}, "cost": 4},
    {"set": {13, 14, 15}, "cost": 2},
]

# ACO Parametreleri
num_ants = 20
num_iterations = 300
alpha = 1  # Feromonun etkisi
beta = 2   # Sezgiselliğin etkisi
evaporation_rate = 0.5
initial_pheromone = 1.0

# Yardımcı Fonksiyonlar
def is_feasible(solution, universe):
    """Çözüm tüm evrensel kümeyi kapsıyor mu?"""
    covered = set()
    for subset in solution:
        covered.update(subset["set"])
    return covered == universe

def calculate_cost(solution):
    """Çözümün toplam maliyetini hesaplar."""
    return sum(subset["cost"] for subset in solution)

def select_subset(probabilities):
    """Verilen olasılıklara göre bir alt küme seç."""
    r = random.random()
    cumulative = 0
    for i, p in enumerate(probabilities):
        cumulative += p
        if r <= cumulative:
            return i
    return len(probabilities) - 1

def print_solution_matrix(solution, iteration):
    """Çözümü bir matris formatında yazdır."""
    matrix = np.zeros((len(subsets), len(universe)))
    for i, subset in enumerate(subsets):
        for element in subset["set"]:
            if subset in solution:
                matrix[i][element - 1] = 1
    print(f"\nÇözüm Matrisi - Iterasyon {iteration + 1}:")
    print(matrix)

# ACO Algoritması
def ant_colony_optimization(universe, subsets, num_ants, num_iterations, alpha, beta, evaporation_rate):
    # Feromon başlatma
    pheromone = [initial_pheromone] * len(subsets)

    best_solution = None
    best_cost = float("inf")

    for iteration in range(num_iterations):
        all_solutions = []

        for ant in range(num_ants):
            current_solution = []
            uncovered = universe.copy()

            while uncovered:
                # Sezgisellik: 1 / maliyet
                heuristic = [len(s["set"] & uncovered) / s["cost"] for s in subsets]

                # Olasılık hesaplama
                probabilities = [
                    (pheromone[i] ** alpha) * (heuristic[i] ** beta)
                    for i in range(len(subsets))
                ]
                total = sum(probabilities)
                probabilities = [p / total for p in probabilities]

                # Alt küme seçimi
                chosen_index = select_subset(probabilities)
                chosen_subset = subsets[chosen_index]

                if chosen_subset not in current_solution:
                    current_solution.append(chosen_subset)
                    uncovered -= chosen_subset["set"]

            all_solutions.append(current_solution)

            # En iyi çözümü güncelle
            current_cost = calculate_cost(current_solution)
            if current_cost < best_cost:
                best_solution = current_solution
                best_cost = current_cost

        # Feromon buharlaşması
        pheromone = [p * (1 - evaporation_rate) for p in pheromone]

        # Feromon güncellemesi
        for solution in all_solutions:
            solution_cost = calculate_cost(solution)
            for subset in solution:
                index = subsets.index(subset)
                pheromone[index] += 1 / solution_cost

        # Çözüm matrisini yazdır
        print_solution_matrix(best_solution, iteration)

        print(f"\nIterasyon {iteration + 1}:")
        print("En İyi Çözüm:", [(s["set"], s["cost"]) for s in best_solution])
        print("Toplam Maliyet:", best_cost)

    return best_solution, best_cost
 
# ACO'yu çalıştır
best_solution, best_cost = ant_colony_optimization(
    universe, subsets, num_ants, num_iterations, alpha, beta, evaporation_rate
)

# Sonuçları yazdır
print("\nEn iyi çözüm:")
for subset in best_solution:
    print(f"Alt Küme: {subset['set']}, Maliyet: {subset['cost']}")

print(f"Toplam Maliyet: {best_cost}")

#knapsack


print("************************************knapsack***************************************")

class Ant:
    def __init__(self, capacity, items):
        self.capacity = capacity
        self.items = items
        self.selected_items = []
        self.total_value = 0
        self.total_weight = 0

    def construct_solution(self):
        self.selected_items = []
        self.total_value = 0
        self.total_weight = 0

        # Karışık olarak nesneleri seç
        while True:
            item = random.choice(self.items)
            if self.total_weight + item[0] <= self.capacity:
                self.selected_items.append(item)
                self.total_weight += item[0]
                self.total_value += item[1]
            else:
                break

def ant_colony_knapsack(items, capacity, num_ants, num_iterations):
    best_solution = None
    best_value = 0

    for iteration in range(num_iterations):
        ants = [Ant(capacity, items) for _ in range(num_ants)]
        solutions = []
        
        for ant in ants:
            ant.construct_solution()
            solutions.append(ant)

        # En iyi çözümü bul
        for ant in solutions:
            if ant.total_value > best_value:
                best_solution = ant.selected_items
                best_value = ant.total_value
        
        # Sonuçları yazdır
        print(f"Iteration {iteration + 1}: Best Value = {best_value}, Selected Items = {best_solution}")

    return best_solution, best_value

# Örnek veri: (Ağırlık, Değer)
items = [
        (10, 60), (22, 100), (31, 120), (15, 150), (26, 200), (85, 250), (3, 300), (54, 350),
        (40, 120), (70, 180), (55, 140), (45, 200), (65, 210), (30, 170), (80, 280), (60, 220),
        (5, 90), (35, 150), (50, 180), (75, 260), (20, 110), (90, 310), (95, 320), (12, 130),
        (72, 230), (100, 350), (55, 190), (68, 270), (85, 300), (42, 150), (88, 260), (92, 310),
        (25, 140), (47, 170), (67, 240), (85, 290), (93, 330), (60, 200), (43, 160), (99, 370),
        (29, 130), (95, 310), (77, 280), (62, 250), (49, 180), (60, 170), (73, 290), (80, 320)
    ]
capacity = 510
num_ants = 20
num_iterations = 300

best_solution, best_value = ant_colony_knapsack(items, capacity, num_ants, num_iterations)

print(f"\nFinal Best Solution: {best_solution}")
print(f"Final Best Value: {best_value}")
