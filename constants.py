# Planisuss Default Simulation Constants
# Some of these values can be modified in the configuration window directly by the user

# World dimensions
NUMCELLS_R = 20   # Number of rows
NUMCELLS_C = 25   # Number of columns

# Simulation parameters
NUMDAYS = 1000                 # Total simulation days
NEIGHBORHOOD = 1               # Vision radius for animals
MOVEMENT_COST = NEIGHBORHOOD   # Movement cost, equals to the neighborhood constant
HUNT_ENERGY_COST = 10          # Energy cost per hunting attempt

# Initial populations (for world initialization)
INITIAL_ERBAST_RATIO = 2     # Initial Erbast ratio
INITIAL_CARVIZ_RATIO = 0.4   # Initial Carviz ratio
WATER_RATIO = 0.15           # Percentage of inner cells that are water

# Vegetob parameters
MIN_VEGETOB_DENSITY = 0     # Minimum Vegetob density
MAX_VEGETOB_DENSITY = 100   # Maximum Vegetob density
INITIAL_VEGETOB_MIN = 50    # Initial Vegetob density for initialisation
INITIAL_VEGETOB_MAX = 70    # Initial Vegetob density for initialisation
DYNAMIC_GROWING_RATE = 2    # Dynamic Vegetob growing rate per day -> Further explanation in vegetob.py

# Energy and life limits for Erbast and Carviz
MAX_ENERGY_E = 100   # Maximum energy for Erbast
MAX_ENERGY_C = 100   # Maximum energy for Carviz
MIN_LIFE_E = 90      # Minimum bound lifetime for Erbast in days
MAX_LIFE_E = 110     # Maximum bound lifetime for Erbast in days
MIN_LIFE_C = 70      # Minimum bound lifetime for Carviz in days
MAX_LIFE_C = 85      # Maximum bound lifetime for Carviz in days

# Energy initial ranges
INITIAL_ENERGY_MIN_E = 50   # Minimum starting energy for Erbast
INITIAL_ENERGY_MAX_E = 70   # Maximum starting energy for Erbast
INITIAL_ENERGY_MIN_C = 30   # Minimum starting energy for Carviz
INITIAL_ENERGY_MAX_C = 60   # Maximum starting energy for Carviz

# Animal aging
AGING_E = 5    # Energy lost per month for Erbast
AGING_C = 10   # Energy lost per month for Carviz

# Social group parameters
MAX_HERD = 30                    # Maximum number of Erbasts in a Herd
MAX_PRIDE = 20                   # Maximum number of Carvizs in a Pride
JOIN_THRESHOLD = 0.35            # Average social attitude required to join when Prides reach the same cell
SOCIAL_BOOST_FROM_FIGHT = 0.02   # Social attitude boost for members in winner Pride when combat

# Migration parameters
MIGRATION_TRIGGER_FACTOR = 0.35    # Trigger a migration when population < 35% of expected
MIGRATION_COOLDOWN_DAYS = 20       # Minimum days between migrations
MIGRATION_REPLENISH_RATIO = 0.60   # Migrate 60% of the population deficit to avoid extintion

# Epidemic parameters
EPIDEMIC_TRIGGER_FACTOR = 2   # Population must exceed 2× initial ratio to trigger an epidemic
EPIDEMIC_COOLDOWN_DAYS = 10   # Minimum days between epidemics
EPIDEMIC_DEATH_RATE = 0.9     # Percentage of population that dies during an epidemic to re-equilibrate

# UI constants
SPEEDS = [1, 1.5, 2]                                        # Speed multipliers for the simulation
COLORS = { 'Erbast': '#00FF00', 'Carviz': "#FF0000" }   # Distinct colors for species visualization