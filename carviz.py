from __future__ import annotations  
from typing import List, Optional, TYPE_CHECKING
import random
from constants import *
from animal import Animal

if TYPE_CHECKING: # Only for type checkers
    from cell import Cell
    from erbast import Erbast
    from pride import Pride

class Carviz(Animal):
    """
    Carnivorous species that hunts Erbast and forms Prides
    It inherites attributes and methods from class Animal
    It then defines a new attribute and new methods specific for Carviz class
    """
    
    def __init__(self, cell: 'Cell'):
        """
        Initialize a Carviz
        
        Args:
            cell (Cell): Starting cell
        """

        # Randomly choose the initial energy within the defined range and the maximum lifetime within the defined range
        energy = random.uniform(INITIAL_ENERGY_MIN_C, INITIAL_ENERGY_MAX_C)
        max_lifetime = random.randint(MIN_LIFE_C, MAX_LIFE_C)
        
        super().__init__(cell, energy, MAX_ENERGY_C, max_lifetime, "carviz")
        
        # Carviz-specific attributes
        self.hunting_efficiency = random.uniform(0.65, 0.85) # How efficiently they hunt
        self.hunting_success_rate = random.uniform(0.65, 0.85) # Base hunting success rate
        self.days_since_last_hunt = 0

    # Now I implement getter and setter methods for Carviz's attributes (so not present in the Animal class)

    # hunting_efficiency (float)
    def get_hunting_efficiency(self) -> float:
        """
        Getter method of hunting_efficiency attribute

        Returns:
            float: efficiency of the Carviz while hunting
        """

        return self.hunting_efficiency

    def set_hunting_efficiency(self, hunting_efficiency: float):
        """
        Setter method of hunting_efficiency attribute

        Args:
            hunting_efficiency (float): efficiency value to set
        """

        self.hunting_efficiency = hunting_efficiency

    # hunting_success_rate (float)
    def get_hunting_success_rate(self) -> float:
        """
        Getter method of hunting_success_rate attribute

        Returns:
            float: success rate of the Carviz in hunting attempts
        """

        return self.hunting_success_rate

    def set_hunting_success_rate(self, hunting_success_rate: float):
        """
        Setter method of hunting_success_rate attribute

        Args:
            hunting_success_rate (float): success rate value to set
        """

        self.hunting_success_rate = hunting_success_rate

    # days_since_last_hunt (int)
    def get_days_since_last_hunt(self) -> int:
        """
        Getter method of days_since_last_hunt attribute

        Returns:
            int: number of days since the Carviz's last hunt
        """

        return self.days_since_last_hunt

    def set_days_since_last_hunt(self, days_since_last_hunt: int):
        """
        Setter method of days_since_last_hunt attribute

        Args:
            days_since_last_hunt (int): number of days to set
        """
        self.days_since_last_hunt = days_since_last_hunt

    # current_group (Pride)
    def get_current_group(self) -> 'Pride':
        """
        Getter method of current_group attribute

        Returns:
            Pride: Pride object where the Carviz is currently in
        """

        return self.current_group

    def set_current_group(self, current_group: 'Pride'):
        """
        Setter method of current_group attribute

        Args:
            current_group (Pride): Set Carviz's current group
        """

        self.current_group = current_group

    # Now I define other Carviz-specific methods
    
    def modify_hunting_attributes(self, hunting_efficiency_delta: float, hunting_success_rate_delta: float):
        """
        Method to modify the hunting attributes of the Carviz of a delta given as parameter 

        Args:
            hunting_efficiency_delta (float): Delta variation of attribute hunting_efficiency
            hunting_success_rate_delta (float): Delta variation of attribute hunting_success_rate
        """

        self.hunting_efficiency += hunting_efficiency_delta
        self.hunting_success_rate += hunting_success_rate_delta
    
    def age_one_day(self):
        """
        Override to track hunting days 
        Age the Carviz by one day and apply aging costs
        Also call the method die() if the Carviz dies due to low energy or old age
        If that is the case, then possible offsprings can be generated
        """
        
        super().age_one_day()
        if self.alive:
            self.days_since_last_hunt += 1 # Increase counter
    
    def search_erbast_to_hunt(self) -> Optional['Erbast']:
        """
        Carviz search in the cell where it is located if there is an Erbast to hunt, otherwise no erbast will be returned

        1. First the Pride looks for the weakest individual Erbast
        2. If none, look for the weakest Erbast inside the Herds in the cell

        Returns:
            Optional[Erbast]: Erbast to hunt if it is found, None otherwise
        """
        
        if not self.alive:
            return None
        
        # choose a target
        erbast_to_hunt = None

        # 1. Look among individual Erbasts
        if self.cell.get_erbast_individuals():
            erbast_to_hunt = self.cell.get_erbast_with_lowest_energy_single(self.cell.get_erbast_individuals()) # Find weakest individual Erbast
        
        # 2. Otherwise look inside herds
        if not erbast_to_hunt and self.cell.get_herds():
            erbast_to_hunt = self.cell.get_erbast_with_lowest_energy_herds(self.cell.get_herds()) # Find weakest Erbast in Herds

        # Return Erbast to hunt, if there is any
        return erbast_to_hunt

    def hunt(self, erbast_to_hunt: Erbast, pride_hunting_coordination_bonus: float) -> bool:
        """
        Carviz hunts the Erbast given as parameter
        The hunt phase is implemented as follow:
        - Considering the hunting efficiency and success rate as a multiplier, the hunt is successful if
          the energy of the Carviz * mutiplier is greater than the energy of the hunted Erbast 
        - If the Carviz wins: Erbast dies and Carviz gains energy and increases its hunting attributes
        - If the Erbast wins: Carviz loses some energy and its hunting attributes decrease 
        
        Args:
            erbast_to_hunt (Erbast): Erbast to hunt
            pride_hunting_coordination_bonus (float): Bonus given by the Carviz's Pride

        Returns:
            bool: True if Carviz wins, False otherwise
        """

        if not self.alive:
            return False # No hunting because the animal is dead, but still present in the game in the current execution
        
        # Carviz cannot move anymore
        self.can_move = False

        # Calculate hunting success rate
        success_rate = self.hunting_success_rate * self.hunting_efficiency + pride_hunting_coordination_bonus
        
        # Desperation increases success rate of the Carviz
        if self.days_since_last_hunt > 10:
            success_rate *= 1.25
        
        # Now proceed with the hunting
        if erbast_to_hunt:
            if success_rate * self.energy >= erbast_to_hunt.get_energy():
                # Successful hunt => Gain energy and Erbast dies
                            
                # Gain energy from hunt and increase hunting attributes
                self.energy = min(self.max_energy, self.energy + erbast_to_hunt.get_energy())
                self.modify_hunting_attributes(0.05, 0.05)

                # Reset Carviz last hunt counter to 0
                self.days_since_last_hunt = 0   
                
                # Mark Erbast as dead
                # No need to consider offsprings
                erbast_to_hunt.die()

                return True

            else:
                # Unsuccessful hunt => Loss of energy (also for the Erbast), decrease of hunting attributes
                erbast_to_hunt.set_energy(erbast_to_hunt.get_energy() * 0.7) # Reduce 30% of Erbast's energy

                # Reduce energy, also checking if the Carviz dies while hunting
                if (self.energy - HUNT_ENERGY_COST) <= 0:
                    self.die() # No offsprings generated in this case
                else:
                    self.energy -= HUNT_ENERGY_COST # No need to check bounds
                    self.modify_hunting_attributes(-0.05, -0.05)

                return False
        else:
            # No Erbast to hunt, so no hunting and no decrease of energy
            self.days_since_last_hunt += 1

            return False
    
    def evaluate_cell_desirability_carviz(self, cell: 'Cell') -> float:
        """
        Evaluate cell desirability for Carviz (prefers cells with Erbasts)
        
        Args:
            cell (Cell): Cell to evaluate, guaranteed to be a "ground" cell
            
        Returns:
            float: Desirability score (the higher the better)
        """

        # Compute the score
        
        # Component 1: Social attraction
        # More Carviz individuals => better, scaled by social attitude
        social_score = self.social_attitude * cell.get_carviz_count()
        
        # Component 2: Erbasts presence
        # More Erbast individuals => better situation for hunting
        erbast_score = cell.get_erbast_count()

        # Desperate hunters value prey more highly
        if self.days_since_last_hunt > 10:
            erbast_score *= 1.5

        # Return the total score
        return social_score + erbast_score
    
    def evaluate_movement(self, ground_neighbors_cells: List['Cell']) -> 'Cell':
        """
        Evaluate if the single Carviz decides to stay in the current cell or to move in another one
        
        Args:
            ground_neighbors_cells (List['Cell']): List of the "ground" neighbors cells of the cell where the Carviz currently is 
        
        Return:
            Cell: Resulting cell after the decision.
                  If the resulting cell is the starting cell, then the Carviz decides to stay
        """

        # No "ground" neighbors cells, stay in the current cell
        if not ground_neighbors_cells:
            return self.cell

        # At beginning, the best score is the one of the current cell
        best_score = self.evaluate_cell_desirability_carviz(self.cell)
        best_cell = self.cell
        
        # Iterate through the "ground" neighbors cells to find the best one
        # The best cell is the one with the highest evaluate_cell_desirability_carviz() score
        for neighbor_cell in ground_neighbors_cells:
            # Compute the desiderability score
            neighbor_score = self.evaluate_cell_desirability_carviz(neighbor_cell)
            if neighbor_score > best_score: # Higher score
                best_score = neighbor_score
                best_cell = neighbor_cell

        return best_cell
    
    def apply_inheritance_rules(self, offsprings: List['Carviz']):
        """
        Override of the method from Animal class
        => Consider also Carviz-specific attributes

        Apply inheritance rules to offsprings according to specifications:
        - Age: set to 0 (already done in constructor)
        - Energy: sum of offsprings energy equals parent energy
        - Other properties: average of children equals parent value
        
        Args:
            offsprings (List['Carviz']): List of two offsprings animals
        """
        
        super().apply_inheritance_rules(offsprings)
        
        # Hunting efficiency inheritance using random splitting, hunting_efficiency can exceed 1
        efficiency_split = random.uniform(0.4, 0.6)
        offsprings[0].set_hunting_efficiency(self.hunting_efficiency * 2 * efficiency_split)
        offsprings[1].set_hunting_efficiency(self.hunting_efficiency * 2 * (1 - efficiency_split))
        
        # Hunting success rate inheritance using random splitting, hunting_success_rate can exceed 1
        success_split = random.uniform(0.4, 0.6)
        offsprings[0].set_hunting_success_rate(self.hunting_success_rate * 2 * success_split)
        offsprings[1].set_hunting_success_rate(self.hunting_success_rate * 2 * (1 - success_split))