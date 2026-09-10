from __future__ import annotations  
from typing import List, TYPE_CHECKING
import random
from constants import *
from animal import Animal

if TYPE_CHECKING: # Only for type checkers
    from cell import Cell 
    from herd import Herd

class Erbast(Animal):
    """
    Herbivorous species that feeds on Vegetob and forms Herds
    It inherites attributes and methods from class Animal
    It then defines a new attribute and new methods specific for Erbast class
    """
    
    def __init__(self, cell: 'Cell'):
        """
        Initialize an Erbast
        
        Args:
            cell (Cell): Starting cell where the Erbast will be located
        """
        
        # Randomly choose the initial energy within the defined range and the maximum lifetime within the defined range
        energy = random.uniform(INITIAL_ENERGY_MIN_E, INITIAL_ENERGY_MAX_E)
        max_lifetime = random.randint(MIN_LIFE_E, MAX_LIFE_E)

        super().__init__(cell, energy, MAX_ENERGY_E, max_lifetime, "erbast")
        
        # Erbast-specific attribute
        self.preferred_vegetob_density = random.uniform(60, 70) # Preferred Vegetob level
    
    # Now I implement getter and setter methods for Erbast's attributes (so not present in the Animal class)

    # preferred_vegetob_density (float)
    def get_preferred_vegetob_density(self) -> float:
        """
        Getter method of preferred_vegetob_density attribute

        Returns:
            float: preferred vegetob density level (0 to 100)
        """

        return self.preferred_vegetob_density

    def set_preferred_vegetob_density(self, preferred_vegetob_density: float):
        """
        Setter method of preferred_vegetob_density attribute

        Args:
            preferred_vegetob_density (float): preferred density value to set (0 to 100)
        """

        self.preferred_vegetob_density = max(0, min(100, preferred_vegetob_density))

    # current_group (Herd)
    def get_current_group(self) -> 'Herd':
        """
        Getter method of current_group attribute

        Returns:
            Herd: Herd object where the Erbast is currently in
        """

        return self.current_group

    def set_current_group(self, current_group: 'Herd'):
        """
        Setter method of current_group attribute

        Args:
            current_group (Herd): Set Erbast's current group
        """

        self.current_group = current_group

    # Now I define other Erbast-specific methods

    def graze(self):
        """
        Graze on Vegetob in the current cell where the Erbast is
        Call the method cell.consume_vegetob()
        """

        if not self.alive or not self.cell.is_ground():
            return
        
        # Erbast cannot move anymore
        self.can_move = False

        # Consume Vegetob from cell - Only if energy < max_energy
        if(self.energy < self.max_energy):
            consumed = self.cell.consume_vegetob(1.0)
            self.energy = min(self.max_energy, self.energy + consumed)
    
    def evaluate_cell_desirability_erbast(self, cell: 'Cell') -> float:
        """
        Compute a score to evaluate cell desirability for Erbast 

        Args:
            cell (Cell): Cell to evaluate, guaranteed to be a "ground" cell
            
        Returns:
            float: Desirability score (the higher the better)
        """

        # Compute the score
        
        # Component 1: Vegetob density matching
        density_distance = abs(cell.get_vegetob_density() - self.preferred_vegetob_density)
        density_score = 100 - density_distance  # Perfect match = 100

        # Component 2: Social attraction
        # More Erbast individuals => better, scaled by social attitude
        social_score = self.social_attitude * cell.get_erbast_count()
        
        # Component 3: Carviz avoidance
        # More Carviz => worse score
        carviz_penalty = cell.get_carviz_count() * 2

        # Component 4: Already visited cell
        # Introduce a small penalty if the cell has been recently visited
        already_visited_penalty = 1 if cell in self.visited_cells else 0

        # Return the total score
        return density_score + social_score - carviz_penalty - already_visited_penalty
    
    def evaluate_movement(self, ground_neighbors_cells: List['Cell']) -> 'Cell':
        """
        Evaluate if the single Erbast decides to stay in the current cell or to move in another one
        
        Args:
            ground_neighbors_cells (List['Cell']): List of the "ground" neighbors cells of the cell where the Erbast currently is 
        
        Returns:
            Cell: Resulting cell after the decision.
                  If the resulting cell has the same [row, column] as the starting cell, then the Erbast decides to stay
        """

        # No "ground" neighbors cells, stay in the current cell
        if not ground_neighbors_cells:
            return self.cell

        # At beginning, the best score is the one of the current cell
        best_score = self.evaluate_cell_desirability_erbast(self.cell)
        best_cell = self.cell
        
        # Iterate through the "ground" neighbors cells to find the best one
        # The best cell is the one with the highest evaluate_cell_desirability_erbast() score
        for neighbor_cell in ground_neighbors_cells:
            # Compute the desiderability score
            neighbor_score = self.evaluate_cell_desirability_erbast(neighbor_cell)
            if neighbor_score > best_score:
                best_score = neighbor_score
                best_cell = neighbor_cell

        return best_cell
    
    def apply_inheritance_rules(self, offsprings: List['Erbast']):
        """
        Override of the method from Animal class
        => Consider also Erbast-specific attributes

        Apply inheritance rules to offsprings according to specifications:
        - Age: set to 0 (already done in constructor)
        - Energy: sum of offsprings energy equals parent energy
        - Other properties: average of children equals parent value
        
        Args:
            offsprings (List[Erbast]): List of two offsprings animals
        """
        
        super().apply_inheritance_rules(offsprings)

        # Preferred vegetob density inheritance
        offsprings[0].preferred_vegetob_density = self.preferred_vegetob_density
        offsprings[1].preferred_vegetob_density = self.preferred_vegetob_density