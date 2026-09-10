from __future__ import annotations 
from typing import List, TYPE_CHECKING
import random
from constants import *

if TYPE_CHECKING: # For static checkers only
    from cell import Cell

class Animal:
    """
    Base class for all animals in Planisuss
    Defines common attributes and behaviors for Erbast and Carviz
    """
    
    def __init__(self, cell: 'Cell', energy: float, max_energy: float, max_lifetime: int, species_name: str):
        """
        Initialize an animal with basic attributes
        
        Args:
            cell (Cell): [row, col] cell in the world
            energy (float): Initial energy level
            max_energy (float): Maximum energy capacity
            max_lifetime (int): Maximum lifetime in days
            species_name (str): Name of the species ("erbast" or "carviz")
        """

        self.cell = cell
        self.energy = energy
        self.max_energy = max_energy
        self.age = 0
        self.max_lifetime = max_lifetime
        self.alive = True
        self.species_name = species_name
        self.can_move = True # Movement is allowed by default
        
        # Social attributes
        self.social_attitude = random.uniform(0.0, 1.0) # 0 = Individualistic, 1 = Highly social
        self.current_group = None # Reference to current Herd / Pride social group 
        
        # Memory of recently visited cells -> Works as a queue (First In First Out)
        self.visited_cells: List['Cell'] = []
    
    # Now I implement getter and setter methods for Animal's attributes

    # cell (Cell)
    def get_cell(self) -> 'Cell':
        """
        Getter method of cell attribute

        Returns:
            Cell: Cell object associated with the animal
        """

        return self.cell

    def set_cell(self, cell: 'Cell'):
        """
        Setter method of cell attribute

        Args:
            cell (Cell): Cell object to set to the animal
        """

        self.cell = cell
    
    # energy (float)
    def get_energy(self) -> float:
        """
        Getter method of energy attribute

        Returns:
            float: current energy level of the animal
        """

        return self.energy

    def set_energy(self, energy: float):
        """
        Setter method of energy attribute, also checking if the animal dies due to low energy

        Args:
            energy (float): energy value to set to the animal
        """

        self.energy = max(min(energy, self.max_energy), 0.0)

        if(self.energy <= 0.0):
            self.die() # No offsprings generated

    # max_energy (float)
    def get_max_energy(self) -> float:
        """
        Getter method of max_energy attribute

        Returns:
            float: maximum energy the animal can reach
        """

        return self.max_energy

    def set_max_energy(self, max_energy: float):
        """
        Setter method of max_energy attribute

        Args:
            max_energy (float): maximum energy to set to the animal
        """

        self.max_energy = max_energy

    # age (int)
    def get_age(self) -> int:
        """
        Getter method of age attribute

        Returns:
            int: current age of the animal
        """

        return self.age

    def set_age(self, age: int):
        """
        Setter method of age attribute

        Args:
            age (int): age to set to the animal
        """

        self.age = age

    # max_lifetime (int)
    def get_max_lifetime(self) -> int:
        """
        Getter method of max_lifetime attribute

        Returns:
            int: maximum lifetime the animal can live
        """

        return self.max_lifetime

    def set_max_lifetime(self, max_lifetime: int):
        """
        Setter method of max_lifetime attribute

        Args:
            max_lifetime (int): maximum lifetime to set to the animal
        """

        self.max_lifetime = max_lifetime

    # alive (bool)
    def get_alive(self) -> bool:
        """
        Getter method of alive attribute

        Returns:
            bool: True if the animal is alive, False otherwise
        """

        return self.alive

    def set_alive(self, alive: bool):
        """
        Setter method of alive attribute

        Args:
            alive (bool): living status to set to the animal
        """

        self.alive = alive

    # species_name (str)
    def get_species_name(self) -> str:
        """
        Getter method of species_name attribute

        Returns:
            str: name of the species
        """

        return self.species_name

    def set_species_name(self, species_name: str):
        """
        Setter method of species_name attribute

        Args:
            species_name (str): name of the species to be set
        """

        self.species_name = species_name

    # can_move (bool)
    def get_can_move(self) -> bool:
        """
        Getter method of can_move attribute

        Returns:
            bool: True if the movement is allowed, False otherwise
        """

        return self.can_move

    def set_can_move(self, can_move: bool):
        """
        Setter method of can_move attribute

        Args:
            can_move (bool): True if the animal can move, False otherwise
        """

        self.can_move = can_move

    # social_attitude (float)
    def get_social_attitude(self) -> float:
        """
        Getter method of social_attitude attribute

        Returns:
            float: value representing the social tendency of the animal (0 to 1)
        """

        return self.social_attitude

    def set_social_attitude(self, social_attitude: float):
        """
        Setter method of social_attitude attribute

        Args:
            social_attitude (float): value representing the social tendency (0 to 1)
        """

        self.social_attitude = max(min(social_attitude, 1.0), 0.0)

    # visited_cells (List[Cell])
    def get_visited_cells(self) -> List['Cell']:
        """
        Getter method of visited_cells attribute

        Returns:
            List[Cell]: list of previously visited cells
        """

        return self.visited_cells

    def set_visited_cells(self, visited_cells: List['Cell']):
        """
        Setter method of visited_cells attribute

        Args:
            visited_cells (List[Cell]): list of cells to set
        """

        self.visited_cells = visited_cells

    # Now I define other methods common to both Erbast and Carviz
    
    def get_aging_cost(self) -> int:
        """
        Get daily aging energy cost
        
        Returns:
            int: Value of the constant AGING depending on species' name
        """
        
        if self.species_name == "erbast": # Erbast
            return AGING_E
        else: # Carviz
            return AGING_C
        
    def are_neighbors(self, cell_1: 'Cell', cell_2: 'Cell', radius: int) -> bool:
        """
        Check whether two cells are neighbors in purely vertical or horizontal directions (Manhattan distance), within the given radius

        Args:
            cell_1 (Cell): First cell
            cell_2 (Cell): Second cell
            radius (int): Maximum Manhattan distance to be considered neighbors

        Returns:
            bool: True  if 0 < row_diff + col_diff <= radius
                  False otherwise (same cell, too far, or diagonal-only offset)
        """
        
        # Calculate row and column difference
        row_diff = abs(cell_1.get_position()[0] - cell_2.get_position()[0])
        col_diff = abs(cell_1.get_position()[1] - cell_2.get_position()[1])

        # Calculate Manhattan distance
        manhattan_dist = row_diff + col_diff

        return 0 < manhattan_dist <= radius
    
    def move_to(self, new_cell: 'Cell') -> bool:
        """
        Move to a new cell and pay movement cost
        Movement can happen only if the animal is alive, its energy level is > MOVEMENT_COST and the cells are neighbors
        
        Args:
            new_cell (Cell): New cell

        Returns:
            bool: True if movement happened, False otherwise
        """

        if self.alive and self.energy > MOVEMENT_COST and self.are_neighbors(self.cell, new_cell, NEIGHBORHOOD):
            # All conditions for movement are respected
            
            # Add to visited cells memory (keep last 10 cells)
            self.visited_cells.append(self.cell)
            if len(self.visited_cells) > 10:
                self.visited_cells.pop(0)

            # Remove animal from old cell
            if self.species_name == "erbast":
                self.cell.remove_erbast(self)
            else:
                self.cell.remove_carviz(self)

            # Update position and decrease energy
            self.cell = new_cell # Set new cell
            self.energy -= MOVEMENT_COST # Movement cost

            # Add animal to new cell
            if self.species_name == "erbast":
                self.cell.add_erbast(self)
            else:
                self.cell.add_carviz(self)

            self.can_move = False # Movement can happen only once per day

            return True # Movement happened correctly
        
        return False # Movement cannot take place

    def age_one_day(self):
        """
        Age the animal by one day and apply aging costs
        Also call the method die() if the animal dies due to low energy or old age
        If that is the case, then possible offsprings can be generated
        If the animal is not alive, then it is removed from the cell
        """

        if self.alive:
            self.age += 1

            # Aging if a month has passed
            if self.age % 10 == 0:
                self.energy -= self.get_aging_cost()
            
            # Check if animal dies from old age or low energy
            if self.age >= self.max_lifetime or self.energy <= 0:
                self.die()
        else:
            # Remove dead animal from social group, if it belongs to any
            if self.current_group is not None:
                self.current_group.remove_member(self)

            # Remove dead animal from cell
            if self.species_name == "erbast":
                self.cell.remove_erbast(self)
            else:
                self.cell.remove_carviz(self)
    
    def die(self):
        """
        Kill the animal
        Offsprings spawn if the animal dies because of old age
        """

        self.alive = False

        # Remove dead animal from social group, if it belongs to any
        if self.current_group is not None:
            self.current_group.remove_member(self)

        # Remove dead animal from the cell where it was located, if it is in there
        if self.species_name == "erbast":
            self.cell.remove_erbast(self)
        else:
            self.cell.remove_carviz(self)

        # If animal died because of old age (reached max life) then offsprings are generated
        if self.age >= self.max_lifetime:
            self.reproduce()
    
    def can_reproduce(self) -> bool:
        """
        Check if reproduction is allowed based on social group capacity
        
        Returns:
            bool: True if reproduction is allowed, False otherwise
        """

        if self.current_group is None:
            return True # Individual animal can always reproduce
        
        # Check if group has capacity for 2 additional members
        if self.species_name == "erbast": # Erbast
            return self.current_group.get_size() + 2 <= MAX_HERD
        else: # Carviz
            return self.current_group.get_size() + 2 <= MAX_PRIDE
    
    def reproduce(self):
        """
        Create offsprings when animal reaches maximum age
        Following the specification rules for property conservation
        """

        # Check if reproduction is allowed based on group capacity
        if not self.can_reproduce():
            return # No reproduction if group would exceed capacity => Nothing happen
        
        # Reproduction can happen => Offsprings are generated

        offsprings: List['Animal'] = []

        # Create two offspring
        # Add them in the cell if the dead animal was not in any social group, otherwise add them in the social group of the dead animal
        for _ in range(2):
            if self.species_name == "erbast": # Erbast
                from erbast import Erbast
                child = Erbast(self.cell) # Erbast's child inheritance will be handled below
                
                # Add offspring to the cell individually or in the social group
                if self.current_group is None: # No social group => Add offspring individually in the cell
                    child.current_group = None
                    self.cell.add_erbast(child)
                else: # Social group => Add offsprings in the social group
                    child.current_group = self.current_group
                    self.current_group.add_member(child)

            else: # Carviz
                from carviz import Carviz
                child = Carviz(self.cell) # Carviz's child inheritance will be handled below

                # Add offspring to the cell individually or in the social group
                if self.current_group is None: # No social group => Add offspring individually in the cell
                    child.current_group = None
                    self.cell.add_carviz(child)
                else: # Social group => Add offsprings in the social group
                    child.current_group = self.current_group
                    self.current_group.add_member(child)

            offsprings.append(child)
        
        # Apply inheritance rules for offsprings
        self.apply_inheritance_rules(offsprings)
    
    def apply_inheritance_rules(self, offsprings: List['Animal']):
        """
        Apply inheritance rules to offsprings according to specifications:
        - Age: set to 0 (already done in Anaimal's constructor)
        - Energy: sum of offsprings energy equals parent energy
        - Other properties: sum of children equals parent value * 2
        
        Args:
            offsprings (List[Animal]): List of two offsprings animals
        """
        
        # Energy distribution: sum equals parent energy
        # Randomly distribute parent's energy between the two children
        energy_split = random.uniform(0.3, 0.7) # Avoid extreme distributions
        offsprings[0].set_energy(self.energy * energy_split)
        offsprings[1].set_energy(self.energy * (1 - energy_split))
        
        # Other properties: average of children = 2 * parent value

        # Max lifetime inheritance
        max_lifetime_split = random.uniform(0.3, 0.7) # Avoid extreme distributions
        offsprings[0].set_max_lifetime(round(self.max_lifetime * 2 * max_lifetime_split))
        offsprings[1].set_max_lifetime(round(self.max_lifetime * 2 * (1 - max_lifetime_split)))
        
        # Social attitude inheritance
        # Here I do not use the random assignment because of the possibility of exceeding the threshold of [0,1] for social_attitude
        offsprings[0].set_social_attitude(self.social_attitude)
        offsprings[1].set_social_attitude(self.social_attitude)
    
        # Species-specific property inheritance will be defined in Erbast and Carviz classes

    def can_follow_group(self) -> bool:
        """
        Determine if animal should follow its social group based on social attitude and energy
        
        Returns:
            bool: True if should follow group (or the animal is alone in the cell), False if should split
        """

        if self.current_group is None:
            return True
        
        if self.energy <= MOVEMENT_COST:
            return False # Animal cannot afford to move due to low energy

        # Low energy animals are more likely to make individual decisions
        energy_factor = self.energy / self.max_energy
        
        # Social attitude influences group following
        follow_probability = self.social_attitude * energy_factor
        
        return follow_probability >= 0.25 # Given threshold for following