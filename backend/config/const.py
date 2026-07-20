import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_MIN_TEMP_C = int(os.getenv("DEFAULT_MIN_TEMP_C", -25))

# Max number of modues in terms of random initalization of chromosome - GA algorithm
MAX_DEFAULT_NUMBER_OF_MODULES = int(os.getenv("MAX_DEFAULT_NUMBER_OF_MODULES", 12))

# GA algorithm
POPULATION_SIZE = int(os.getenv("POPULATION_SIZE", 100))
MUTATION_RATE = float(os.getenv("MUTATION_RATE", 0.01))
CROSSOVER_RATE = float(os.getenv("CROSSOVER_RATE", 0.7))
ELITISM_RATE = float(os.getenv("ELITISM_RATE", 0.1))
GENERATIONS = int(os.getenv("GENERATIONS", 100))
TOURNAMENT_SIZE = int(os.getenv("TOURNAMENT_SIZE", 3))
TOP_RESULTS_COUNT = int(os.getenv("TOP_RESULTS_COUNT", 3))
MAX_BUDGET_OVERSHOOT_RATIO = float(os.getenv("MAX_BUDGET_OVERSHOOT_RATIO", 0.05))


BASIC_SERVICE_COST_PLN = 1_000
CABLE_COST_PLN_PER_M = 25
ROOF_LABOR_COST_PLN_PER_PANEL = 120
GROUND_LABOR_COST_PLN_PER_PANEL = 150
ROOF_MOUNTING_COST_PLN_PER_PANEL = 50
GROUND_MOUNTING_COST_PLN_PER_PANEL = 200

# PV production model (Poland)
Y_REF_KWH_PER_KWP = 1050
OPTIMAL_TILT_DEG = 35
TILT_FACTOR_SIGMA = 15
LIKERT_SHADING_FACTORS = {
    1: 1.00,
    2: 0.95,
    3: 0.85,
    4: 0.70,
    5: 0.50,
}

# Chat
MAX_MESSAGES = 6