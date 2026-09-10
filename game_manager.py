from constants import *
from cell import Cell
from erbast import Erbast
from carviz import Carviz
from herd import Herd

import random, pickle
from typing import List, Tuple
import numpy as np

class GameManager:
    """
    Manages the Planisuss ecosystem simulation
    Handles world initialization, daily cycles and game progression
    """

    def __init__(self):
        # World data
        self.grid: List[List['Cell']] = []
        self.size = 0
        self.ground_cells: List['Cell'] = []

        # Day and event counters
        self.current_day = 0
        self.last_migration_day = 0
        self.last_epidemic_day = 0

        # UI-related state
        self.time = 0.0 # Simulated days
        self.speed = 1.0 # X multiplier (1, 1.5, 2), default is x1.0
        
        # time-series for live plots and information
        self.history = {
            "time": [],
            "Erbast": [],
            "Carviz": [],
            "avg_Vegetob": [],
            "total_Herds": [],
            "total_Prides": []
        }

        # Store the configuration values when the game is created
        self.config_values = {
            'NUMDAYS': NUMDAYS,
            'NUMCELLS_R': NUMCELLS_R,
            'NUMCELLS_C': NUMCELLS_C,
            'WATER_RATIO': WATER_RATIO,
            'INITIAL_ERBAST_RATIO': INITIAL_ERBAST_RATIO,
            'INITIAL_CARVIZ_RATIO': INITIAL_CARVIZ_RATIO,
            'MAX_HERD': MAX_HERD,
            'MAX_PRIDE': MAX_PRIDE
        }

    # Now I implement getter and setter methods for GameManager's attributes

    # grid (List[List[Cell]])
    def get_grid(self) -> List[List['Cell']]:
        """
        Getter method of grid attribute
        
        Returns:
            List[List[Cell]]: The grid representing the world
        """

        return self.grid

    def set_grid(self, grid: List[List['Cell']]):
        """
        Setter method of grid attribute
        
        Args:
            grid (List[List[Cell]]): The new grid to set for the world
        """

        self.grid = grid

    # size (int)
    def get_size(self) -> int:
        """
        Getter method of size attribute
        
        Returns:
            int: The size of the world grid (number of cells along one dimension)
        """
        
        return self.size

    def set_size(self, size: int):
        """
        Setter method of size attribute
        
        Args:
            size (int): The new size of the world grid to set
        """
        
        self.size = max(0, size)

    # ground_cells (List[Cell])
    def get_ground_cells(self) -> List['Cell']:
        """
        Getter method of ground_cells attribute
        
        Returns:
            List[Cell]: The list of "ground" cells in the world
        """

        return self.ground_cells

    def set_ground_cells(self, ground_cells: List['Cell']):
        """
        Setter method of ground_cells attribute
        
        Args:
            ground_cells (List[Cell]): The new list of "ground" cells to set for the world
        """
        
        self.ground_cells = ground_cells

    # current_day (int)
    def get_current_day(self) -> int:
        """
        Getter method of current_day attribute
        
        Returns:
            int: The current day in the simulation
        """
        
        return self.current_day

    def set_current_day(self, current_day: int):
        """
        Setter method of current_day attribute
        
        Args:
            current_day (int): The new current day to set for the simulation
        """
        
        self.current_day = max(0, current_day)

    # last_migration_day (int)
    def get_last_migration_day(self) -> int:
        """
        Getter method of last_migration_day attribute
        
        Returns:
            int: The last day when a migration occurred
        """
        
        return self.last_migration_day

    def set_last_migration_day(self, day: int):
        """
        Setter method of last_migration_day attribute
        
        Args:
            day (int): The new last migration day to set for the simulation
        """
        
        self.last_migration_day = max(0, day)

    # last_epidemic_day (int)
    def get_last_epidemic_day(self) -> int:
        """
        Getter method of last_epidemic_day attribute
        
        Returns:
            int: The last day when an epidemic occurred
        """
        
        return self.last_epidemic_day

    def set_last_epidemic_day(self, day: int):
        """
        Setter method of last_epidemic_day attribute
        
        Args:
            day (int): The new last epidemic day to set for the simulation
        """
        
        self.last_epidemic_day = max(0, day)

    # time (float)
    def get_time(self) -> float:
        """
        Getter method of time attribute (simulated days)
        
        Returns:
            float: The current simulated time in days
        """
        
        return self.time

    def set_time(self, time: float):
        """
        Setter method of time attribute
        
        Args:
            time (float): The new time to set for the simulation, in days
        """
        
        self.time = max(0.0, time)

    # speed (float)
    def get_speed(self) -> float:
        """
        Getter method of speed attribute
        
        Returns:
            float: The current speed multiplier for the simulation
        """
        
        return self.speed

    def set_speed(self, speed: float):
        """
        Setter method of speed attribute
        
        Args:
            speed (float): The new speed multiplier to set for the simulation
        """
        
        self.speed = max(1, speed)  # Lower bound to avoid less than x1 speeds

    # history (dict)
    def get_history(self) -> dict:
        """
        Getter method of history dictionary
        
        Returns:
            dict: The history of simulation statistics, including time, Erbast count, Carviz count, average Vegetob density and other stats
        """
        
        return self.history

    def set_history(self, history: dict):
        """
        Setter method of history dictionary
        
        Args:
            history (dict): The new history dictionary to set for the simulation
        """
        
        if isinstance(history, dict):
            self.history = history

    # config_values (dict)
    def get_config_values(self) -> dict:
        """
        Getter method of config_values dictionary
        
        Returns:
            dict: config_values to use in the simulation
        """
        
        return self.config_values

    def set_config_values(self, config_values: dict):
        """
        Setter method of config_values dictionary
        
        Args:
            config_values (dict): The new config_values to set for the simulation
        """
        
        if isinstance(config_values, dict):
            self.config_values = config_values

    # Now I define other methods

    def initialize_world(self):
        """
        Create grid, Vegetob and starter animals
        """
        
        self.grid, self.ground_cells = self.create_world_grid()
        self.size = len(self.grid)
        self.populate_initial_animals()

    def create_world_grid(self) -> Tuple[List[List['Cell']],List['Cell']]:
        """
        Create and initialize the Planisuss world grid
        
        - Creates a rectangular grid of NUMCELLS_R x NUMCELLS_C cells
        - Border cells are always "water" cells (inhabitable)
        - Inner cells are randomly assigned as "water" or "ground" based on WATER_RATIO constant
        - Each cell is initialized with appropriate terrain type and Vegetob density
        
        Returns:
            Tuple: - List[List[Cell]]: 2D grid of Cell objects representing the world
                   - List[Cell]: List of "ground" cells in the world
        """
        
        grid: List[List['Cell']] = []
        ground_cell: List['Cell'] = []
        
        for row in range(NUMCELLS_R):
            cell_row = []
            
            for col in range(NUMCELLS_C):
                # Determine terrain type
                terrain_type = self.determine_terrain_type(row, col)
                
                # Create cell
                cell = Cell(row, col, terrain_type)
                cell_row.append(cell)

                # Check if the cell is a "ground" cell
                if terrain_type == "ground":
                    ground_cell.append(cell)
            
            grid.append(cell_row)
        
        return (grid, ground_cell)

    def determine_terrain_type(self, row: int, col: int) -> str:
        """
        Determine whether a cell should be "water" or "ground" based on its position
        
        Rules:
        - Border cells (edges) are always "water" cells
        - Inner cells are randomly "water" or "ground" based on WATER_RATIO constant
        
        Args:
            row (int): Row position in grid
            col (int): Column position in grid
            
        Returns:
            str: "water" or "ground"
        """

        # Check if cell is on the border and return "water" if that is the case
        if (row == 0 or row == NUMCELLS_R - 1 or col == 0 or col == NUMCELLS_C - 1):
            return "water"
        
        # For inner cells, randomly assign based on WATER_RATIO constant
        if random.random() < WATER_RATIO:
            return "water"
        else:
            return "ground"

    def get_neighbors_ground_cells(self, grid: List[List['Cell']], cell: 'Cell', radius: int) -> List['Cell']:
        """
        Get neighboring "ground" cells within a specified radius from a given position
        Consider the horizontal and vertical dimensions with radius given as parameter
        Control the limit of the map based on the cell position

        Args:
            grid (List[List[Cell]]): The world grid
            cell (Cell): Given cell, need to find its neighbors 

        Returns:
            List[Cell]: List of neighbors "ground" cells
        """
        
        row, col = cell.get_position()
        ground_neighbors = []

        for delta_row in range(-radius, radius + 1):
            for delta_col in range(-radius, radius + 1):
                # Skip the center cell itself
                if delta_row == 0 and delta_col == 0:
                    continue

                # Only allow vertical or horizontal neighbors, not diagonal
                if abs(delta_row) + abs(delta_col) > radius or (delta_row != 0 and delta_col != 0):
                    continue

                neighbor_row = row + delta_row
                neighbor_col = col + delta_col

                # Check if the cell is actually a neighbor and if it is a "ground" cell
                if 0 <= neighbor_row < NUMCELLS_R and 0 <= neighbor_col < NUMCELLS_C and grid[neighbor_row][neighbor_col].is_ground():
                    ground_neighbors.append(grid[neighbor_row][neighbor_col])

        return ground_neighbors

    def populate_initial_animals(self):
        """
        Populate world with the initial Erbasts and Carvizs
        Assign animals to random ground cells
        """
        
        total_ground = len(self.ground_cells)
        number_erbasts = max(1, int(total_ground * INITIAL_ERBAST_RATIO))
        number_carvizs = max(1, int(total_ground * INITIAL_CARVIZ_RATIO))

        # Create random Erbasts and Carvizs and put them in random cells
        for _ in range(number_erbasts):
            self.create_random_erbast()
        for _ in range(number_carvizs):
            self.create_random_carviz()
    
    def create_random_erbast(self):
        """
        Create a random Erbast in a random "ground" cell and add it to that cell
        """

        cell = random.choice(self.ground_cells)
        erbast = Erbast(cell)
        cell.add_erbast(erbast)

    def create_random_carviz(self):
        """
        Create a random Carviz in a random "ground" cell and add it to that cell
        """

        cell = random.choice(self.ground_cells)
        carviz = Carviz(cell)
        cell.add_carviz(carviz)

    def step(self, dt: float = 1.0):
        """
        Simulation step
        Advance the simulation by dt simulated days, scaled by the UI's speed multiplier

        Args:
            dt (float): Number of days to advance in the simulation
        """

        target_time = self.time + dt * self.speed

        # Increase time in 1-day increments
        while self.time + 1.0 <= target_time:
            self.time += 1.0
            self.current_day = int(self.time)
            
            if not self.simulate_one_day():
                raise StopIteration  # Extinction – UI catches and stops simulation
        
        self.time = target_time # Keep fractional remainder of time
        self.current_day = len(self.history["time"]) # Update current_day to match the actual number of days simulated

    def simulate_one_day(self) -> bool:
        """
        Perform the five daily phases
        
        Returns:
            bool: True if simulation can continue, False if extinction detected (to end the simulation early)
        """
        
        # daily phases
        self.phase_growing()
        self.phases_movement_grazing_hunting()
        self.phase_procreation()
        self.maybe_trigger_migrations()
        self.maybe_trigger_epidemic()

        # Count overall Erbasts and Carvizs
        erbasts_end = sum(cell.get_erbast_count() for cell in self.ground_cells)
        carvizs_end = sum(cell.get_carviz_count() for cell in self.ground_cells)
        
        # Calculate average Vegetob density
        total_density = 0.0
        for cell in self.ground_cells:
            total_density += cell.get_vegetob_density()
        avg_vegetob = round(total_density / len(self.ground_cells), 3)

        # Count Herds and Prides
        herds_end = sum(len(cell.get_herds()) for cell in self.ground_cells)
        prides_end = sum(len(cell.get_prides()) for cell in self.ground_cells)

        # keep history for UI
        self.log_stats(erbasts_end, carvizs_end, avg_vegetob, herds_end, prides_end)

        return not self.check_extinction() # Check extinction of the species

    def log_stats(self, total_erbasts: int, total_carvizs: int, avg_vegetob: float, herds_end: int, prides_end: int):
        """
        Append end of day statistics to the history for UI visualization
        
        Args:
            total_erbasts (int): Total number of Erbasts at the end of the day
            total_carvizs (int): Total number of Carvizs at the end of the day
            avg_vegetob (float): Average Vegetob density across all ground cells
            herds_end (int): Total number of Herds at the end of the day
            prides_end (int): Total number of Prides at the end of the day
        """
        
        self.history["time"].append(self.time)
        self.history["Erbast"].append(total_erbasts)
        self.history["Carviz"].append(total_carvizs)
        self.history["avg_Vegetob"].append(avg_vegetob)
        self.history["total_Herds"].append(herds_end)
        self.history["total_Prides"].append(prides_end)

    def phase_growing(self):
        """
        Vegetob growth in all cells and check for overwhelmed cells
        """
        
        # Grow Vegetob in all "ground" cells
        for cell in self.ground_cells:
            cell.grow_vegetob()
            ground_neighbors = self.get_neighbors_ground_cells(self.grid, cell, NEIGHBORHOOD)
            cell.is_overwhelmed_by_vegetob(ground_neighbors)

    def phases_movement_grazing_hunting(self):
        """
        Collective and individual movements
        Grazing happen for Erbasts and Herds who decide to stay in their current cell, otherwise movement happen
        Hunting happen for Carvizs and Prides who decide to stay in their current cell, otherwise movement happen
        """

        # At the beginning of the day social groups are formed / merged
        for cell in self.ground_cells:
            cell.initiate_daily_social_groups()

            # After social groups formation, set forced_to_move attribute of there are multiple Herds in the cell 
            self.manage_herds_competition(cell.get_herds())

        # Process each "ground" cell
        for cell in self.ground_cells:
            # Determine "ground" neighbors
            ground_neighbors = self.get_neighbors_ground_cells(self.grid, cell, NEIGHBORHOOD)

            # Movement or grazing for Herds
            for herd in cell.get_herds()[:]:
                if herd.get_can_move():
                    target_cell = herd.decide_collective_movement(ground_neighbors)
                    if target_cell == cell:
                        # Herd stays in the same cell, it grazes
                        herd.collective_graze()
                    else:
                        # Herd moves to a new cell
                        herd.collective_move_to(target_cell)

            # Movement or grazing for individual Erbasts
            for erbast in cell.get_erbast_individuals()[:]:
                if erbast.get_can_move():
                    target_cell = erbast.evaluate_movement(ground_neighbors)
                    if target_cell == cell:
                        # Erbast stays in the same cell, it grazes
                        erbast.graze()
                    else:
                        # Erbast moves to a new cell
                        erbast.move_to(target_cell)

            # Movement or hunting for Prides
            for pride in cell.get_prides()[:]:
                if pride.get_can_move():
                    target_cell = pride.decide_collective_movement(ground_neighbors)
                    if target_cell == cell:
                        # Pride stays in the same cell, it hunts
                        pride.collective_hunt()
                    else:
                        # Pride moves to a new cell
                        pride.collective_move_to(target_cell)

            # Movement or hunting for individual Carvizs
            for carviz in cell.get_carviz_individuals()[:]:
                if carviz.get_can_move():
                    target_cell = carviz.evaluate_movement(ground_neighbors)
                    if target_cell == cell:
                        # Carviz stays in the same cell, it hunts
                        prey = carviz.search_erbast_to_hunt()
                        if prey:
                            carviz.hunt(prey, 0.0)
                    else:
                        # Carviz moves to a new cell
                        carviz.move_to(target_cell)

        # After movement or actions, reset can_move flags for all animals and forced_to_move for Herds
        for cell in self.ground_cells:
            for erbast in cell.get_erbast_individuals():
                erbast.set_can_move(True)
            
            for carviz in cell.get_carviz_individuals():
                carviz.set_can_move(True)
            
            for herd in cell.get_herds():
                herd.set_can_move(True)
                herd.set_forced_to_move(False)
                for member in herd.get_members():
                    member.set_can_move(True)
            
            for pride in cell.get_prides():
                pride.set_can_move(True)
                for member in pride.get_members():
                    member.set_can_move(True)

    def manage_herds_competition(self, herds: List['Herd']):
        """
        Manage competition between Herds in the same cell
        If there are multiple Herds in a cell, the first one can stay (forced_to_move = False), while the others must move (forced_to_move = True)
        
        Args:
            herds (List[Herd]): List of Herds that need to be checked
        """
            
        if len(herds) >= 2: # Multiple Herds in the cell
            # First Herd can stay (keep forced_to_move = False)
            herds[0].set_forced_to_move(False)
                
            # All other Herds must move (set forced_to_move = True)
            for i in range(1, len(herds)):
                herds[i].set_forced_to_move(True)
        else:
            # Only one or no Herds in the cell, no competition
            for herd in herds:
                herd.set_forced_to_move(False)

    def phase_procreation(self):
        """
        Age all animals, evaluate reproduction and generation of offsprings, remove dead animals
        """
        
        for cell in self.ground_cells:
            # Age individual Erbast
            for erbast in cell.get_erbast_individuals()[:]: # Iterate over a copy
                erbast.age_one_day()
            
            # Age individual Carviz
            for carviz in cell.get_carviz_individuals()[:]: # Iterate over a copy
                carviz.age_one_day()
            
            # Age Herds's members
            for herd in cell.get_herds()[:]: # Iterate over a copy
                herd.age_all_members()
            
            # Age Prides's members
            for pride in cell.get_prides()[:]: # Iterate over a copy
                pride.age_all_members()

    def maybe_trigger_migrations(self):
        """
        Trigger migrations based on current animal counts and replenish populations if below expected levels
        Migrations occur if at least MIGRATION_COOLDOWN_DAYS have passed since the last migration
        """

        # Check if enough time has passed since the last migration
        if self.current_day - self.last_migration_day < MIGRATION_COOLDOWN_DAYS:
            return # Not enoigh time, so exit the method

        # Calculate current and expected counts of Erbasts and Carvizs
        current_erbasts = sum(cell.get_erbast_count() for cell in self.ground_cells)
        current_carvizs = sum(cell.get_carviz_count() for cell in self.ground_cells)
        expected_erbasts = len(self.ground_cells) * INITIAL_ERBAST_RATIO
        expected_carvizs = len(self.ground_cells) * INITIAL_CARVIZ_RATIO

        if current_erbasts < expected_erbasts * MIGRATION_TRIGGER_FACTOR:
            # Calculate how many Erbasts to create
            arrivals = max(1, int((expected_erbasts - current_erbasts) * MIGRATION_REPLENISH_RATIO))
            for _ in range(arrivals):
                self.create_random_erbast() # Create random Erbast

            self.last_migration_day = self.current_day

        if current_carvizs < expected_carvizs * MIGRATION_TRIGGER_FACTOR:
            # Calculate how many Carvizs to create
            arrivals = max(1, int((expected_carvizs - current_carvizs) * MIGRATION_REPLENISH_RATIO))
            for _ in range(arrivals):
                self.create_random_carviz() # Create random Carviz
            
            self.last_migration_day = self.current_day

    def maybe_trigger_epidemic(self):
        """
        Trigger an epidemic if the number of Erbasts or Carvizs exceeds a threshold
        Epidemics can only occur if at least EPIDEMIC_COOLDOWN_DAYS have passed since the last epidemic
        """
        
        # Check if enough time has passed since the last epidemic
        if self.current_day - self.last_epidemic_day < EPIDEMIC_COOLDOWN_DAYS:
            return # Not enoigh time, so exit the method

        # Calculate expected and current counts of Erbasts and Carvizs
        current_erbasts = sum(cell.get_erbast_count() for cell in self.ground_cells)
        current_carvizs = sum(cell.get_carviz_count() for cell in self.ground_cells)
        expected_erbasts = len(self.ground_cells) * INITIAL_ERBAST_RATIO
        expected_carvizs = len(self.ground_cells) * INITIAL_CARVIZ_RATIO

        # Check if current counts exceed expected counts by the trigger factor
        affects_erbasts = current_erbasts > expected_erbasts * EPIDEMIC_TRIGGER_FACTOR
        affects_carvizs = current_carvizs > expected_carvizs * EPIDEMIC_TRIGGER_FACTOR
        
        if not (affects_erbasts or affects_carvizs):
            return # No epidemic triggered

        # Calculate the number of deaths based on the current counts
        all_erbasts = []
        all_carvizs = []

        for cell in self.ground_cells:
            # Get all Erbasts from the current cell if needed
            if affects_erbasts:
                all_erbasts.extend(cell.get_erbast_individuals())
                for herd in cell.get_herds():
                    all_erbasts.extend(herd.get_members())
            
            # Get all Carvizs from the current cell if needed
            if affects_carvizs:
                all_carvizs.extend(cell.get_carviz_individuals())
                for pride in cell.get_prides():
                    all_carvizs.extend(pride.get_members())

        deaths_erb = int(current_erbasts * EPIDEMIC_DEATH_RATE) if affects_erbasts else 0
        deaths_car = int(current_carvizs * EPIDEMIC_DEATH_RATE) if affects_carvizs else 0

        # Randomly select animals to die based on the calculated death counts
        if affects_erbasts and all_erbasts:
            # Randomly select Erbasts to die
            for erbast in random.sample(all_erbasts, min(deaths_erb, len(all_erbasts))):
                erbast.die()
        
        if affects_carvizs and all_carvizs:
            # Randomly select Carvizs to die
            for carviz in random.sample(all_carvizs, min(deaths_car, len(all_carvizs))):
                carviz.die()

        self.last_epidemic_day = self.current_day
    
    def check_extinction(self) -> bool:
        """
        Check if the simulation has reached extinction conditions
        
        Returns:
            bool: True if extinction is detected (no Erbasts or Carvizs left), False otherwise
        """
        
        total_erbasts = sum(cell.get_erbast_count() for cell in self.ground_cells)
        total_carvizs = sum(cell.get_carviz_count() for cell in self.ground_cells)
        return total_erbasts == 0 or total_carvizs == 0

    def get_time_series(self) -> Tuple[List[float], dict]:
        """
        Getter method of relevant info contained in history attribute
        Used in the UI to show charts, so it returns a tuple with useful data (social groups not included)
        
        Returns:
            Tuple[List[float], dict]: (time, {"Erbast": List, "Carviz": List, "avg_Vegetob": List})
        """
        
        return (
            self.history["time"],
            {"Erbast": self.history["Erbast"],
             "Carviz": self.history["Carviz"],
             "avg_Vegetob": self.history["avg_Vegetob"]}
        )

    def get_map_rgb(self) -> np.ndarray:
        """
        Get the RGB representation of the world grid
        NUMCELLS_R x NUMCELLS_C x 3 float array in [0,1]:
        - Red: Carviz
        - Green: Erbast
        - Yellow (R+G): Vegetob
        - Blue: Water

        Returns:
            np.ndarray: RGB representation of the world grid
        """

        rgb = np.zeros((self.size, len(self.grid[0]), 3), dtype=float)
        
        # Iterate through each cell in the grid and convert to RGB
        for i in range(self.size):
            for j in range(len(self.grid[0])):
                rgb[i, j] = self.cell_to_rgb(self.grid[i][j])
        
        return rgb

    def cell_to_rgb(self, cell: 'Cell') -> Tuple[float, float, float]:
        """
        Convert a Cell to its RGB representation
        
        Args:
            cell (Cell): The cell to convert

        Returns:
            Tuple[float, float, float]: float values of the RGB representation of the cell
        """

        if not cell.is_ground():
            return (0.0, 0.0, 1.0)  # Water = Blue

        # Species presence
        r = min(cell.get_carviz_count() / MAX_PRIDE, 1.0)
        g = min(cell.get_erbast_count() / MAX_HERD, 1.0)

        # Vegetob density adds yellow tint ( red + green)
        veg = cell.get_vegetob_density() / 100.0  # 0–1 scale
        r += 0.5 * veg
        g += 0.5 * veg

        # Clip to valid RGB range [0,1]
        return (min(r, 1.0), min(g, 1.0), 0.0)

    def save_state(self, file_path: str):
        """
        Save the current state of the game manager to a file
        - Ensure the directory exists
        - File open using 'wb' mode for writing in binary format
        - File saved using .pkl extension
        Save also the configuation values defined by the user

        Args:
            file_path (str): The file path where the state should be saved
        """

        save_data = {
            'game_state': self.__dict__, # All game data
            'config_values': self.config_values # Configuration used
        }

        with open(file_path, 'wb') as f:
            pickle.dump(save_data, f)

    @classmethod
    def load_state(cls, file_path: str) -> 'GameManager':
        """
        Class method used to load and return a GameManager instance from a file
        Allows calling without creating an object first (GameManager.load_state(path))
        
        - Ensure the file exists and is readable
        - File open using 'rb' mode for reading in binary format
        - File loaded using .pkl extension
        
        Args:
            file_path (str): The file path from which to load the state

        Return:
            GameManager: Instance of the loaded GameManager
        """

        # Imports
        import pickle
        import constants

        with open(file_path, 'rb') as f:
            save_data = pickle.load(f)
        
        # Restore configuration values to constants module
        if 'config_values' in save_data:
            for key, value in save_data['config_values'].items():
                setattr(constants, key, value)
        
        # Create new instance and restore game state
        instance = cls()
        if 'config_values' in save_data:
            instance.__dict__.update(save_data['game_state'])
        else:
            # Handle old save files without config_values
            instance.__dict__.update(save_data)
        
        return instance