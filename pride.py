from __future__ import annotations 
from typing import List, TYPE_CHECKING
from constants import *

if TYPE_CHECKING: # For static checkers only
    from cell import Cell
    from carviz import Carviz

class Pride:
    """
    Social group for Carviz animals
    Prides are formed when multiple Carviz are in the same cell and coordinate their hunting
    """
    
    def __init__(self, cell: 'Cell', members: List['Carviz']):
        """
        Initialize a Pride with a list of Carviz members
        
        Args:
            cell (Cell): Cell where the Pride is located
            members (List['Carviz']): List of Carviz objects to form the Pride
        """
        
        self.cell = cell
        self.members = members[:] # Copy the list of members to avoid reference issues
        self.visited_cells: List['Cell'] = []
        self.can_move = True # Prides can move by default
        self.hunting_coordination = self.calculate_hunting_coordination() # Influence movement decisions and hunting
        
        for member in self.members:
            # Set all members' current_group reference to this Pride
            member.set_current_group(self)

            # Remove members from the cell's list of individual Carviz
            self.cell.remove_carviz(member)
    
    # Now I implement getter and setter methods for Pride's attributes

    # cell (Cell)
    def get_cell(self) -> 'Cell':
        """
        Getter method of cell attribute

        Returns:
            Cell: Cell where the Pride is located
        """

        return self.cell

    def set_cell(self, cell: 'Cell'):
        """
        Setter method of cell attribute

        Args:
            cell (Cell): Cell to set to the Pride
        """

        self.cell = cell

    # members (List[Carviz])
    def get_members(self) -> List['Carviz']:
        """
        Getter method of members attribute

        Returns:
            List[Carviz]: list of Carvizs in the Pride
        """

        return self.members

    def set_members(self, members: List['Carviz']):
        """
        Setter method of members attribute

        Args:
            members (List[Carviz]): list of Carviz to set
        """

        self.members = members

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

    # hunting_coordination (float)
    def get_hunting_coordination(self) -> float:
        """
        Getter method of hunting_coordination attribute

        Returns:
            float: Value of hunting_coordination of this Pride
        """

        return self.hunting_coordination

    def set_hunting_coordination(self, hunting_coordination: float):
        """
        Setter method of hunting_coordination attribute

        Args:
            hunting_coordination (float): Value to set
        """

        self.hunting_coordination = hunting_coordination

    # Now I define other methods
    
    def get_size(self) -> int:
        """
        Get number of members in the Pride
        
        Returns:
            int: Number of members in the Pride
        """
        
        return len(self.members)
    
    def get_member_with_highest_energy(self) -> 'Carviz':
        """
        Get the Carviz in the Pride with the highest value of energy
        
        Returns:
            Carviz: Carviz with highest value of energy
        """

        # At beginning, the Carviz with highest value of energy is the first one
        carviz_highest_energy = self.members[0]
        highest_energy = carviz_highest_energy.get_energy()
        
        # Iterate throigh other memebers and check if there is one whose energy is higher than the current highest value
        for member in self.members[1:]:
            if(member.get_energy() > highest_energy):
                carviz_highest_energy = member
                highest_energy = member.get_energy()

        return carviz_highest_energy

    def calculate_hunting_coordination(self) -> float:
        """
        Calculate the hunting coordination of the Pride based on members' attributes
        
        Returns:
            float: Hunting coordination strength
        """
        
        if not self.members:
            return 0.0
        
        # Average social attitude, hunting efficiency and hunting_success_rate
        total_social = sum(member.get_social_attitude() for member in self.members)
        total_hunting_efficiency = sum(member.get_hunting_efficiency() for member in self.members)
        total_hunting_success_rate = sum(member.get_hunting_success_rate() for member in self.members)
        
        avg_social = total_social / len(self.members)
        avg_hunting_efficiency = total_hunting_efficiency / len(self.members)
        avg_hunting_success_rate = total_hunting_success_rate / len(self.members)
        
        # Size factor - optimal Pride size for hunting
        optimal_size = MAX_PRIDE * 0.75 # About 75% of max size is optimal
        size_factor = 1.0 - abs(len(self.members) - optimal_size) / optimal_size
        size_factor = max(0.1, size_factor) # Minimum 0.1
        
        return (avg_social + avg_hunting_efficiency + avg_hunting_success_rate) * size_factor
    
    def modify_social_attitude_from_fight(self, amount: float):
        """
        Modify the social attribute of the Pride's member of a value given as paramter
        
        Args:
            amount (float): Amount to sum (can be negative)
        """

        for member in self.members:
            member.set_social_attitude(member.get_social_attitude() + amount)

    def eliminate(self):
        """
        Eliminate the Pride is there are no members or there is only one
        It also deals with the cell's lists attributes
        """

        if len(self.members) == 0:
            # Pride is empty => Remove it from the cell
            self.cell.remove_pride(self)
        
        if len(self.members) == 1:
            # Only 1 member => Remove from the Pride and consider it as an individual, re-set its attributes
            self.remove_member(self.members[0])

            # Modify cell's lists
            self.cell.remove_pride(self)

        # Do nothing if there are at least 2 members
    
    def add_member(self, carviz: 'Carviz') -> bool:
        """
        Add a Carviz to the Pride
        
        Args:
            carviz (Carviz): Carviz object to add
            
        Returns:
            bool: True if successfully added, False if Pride is full
        """
        
        if len(self.members) >= MAX_PRIDE:
            return False
        
        if carviz not in self.members:
            self.cell.remove_carviz(carviz) # Remove Carviz from the cell's list of individual Carviz
            carviz.set_current_group(self) # Set Carviz's current group attribute
            carviz.set_social_attitude(carviz.get_social_attitude() + 0.1) # Increase Carviz's social attitude
            self.members.append(carviz) # Add given Carviz to the Pride
            self.hunting_coordination = self.calculate_hunting_coordination() # Re-calculate Pride's hunting coordination
            return True
    
        return False # Carviz already in the Pride

    def remove_member(self, carviz: 'Carviz'):
        """
        Remove a Carviz from the pride
        
        Args:
            carviz (Carviz): Carviz object to remove
        """
        
        try:
            self.members.remove(carviz) # Remove given Carviz
            
            # Re-set Carviz's attributes
            carviz.set_current_group(None)
            carviz.set_cell(self.cell)
            carviz.set_social_attitude(carviz.get_social_attitude() - 0.1)
            carviz.set_visited_cells(self.visited_cells)

            # Add Carviz in the cell's list of individual carviz
            carviz.get_cell().add_carviz(carviz)

            # Re-calculate Pride's hunting coordination
            self.hunting_coordination = self.calculate_hunting_coordination()

        except ValueError:
            pass # Carviz not present in the Pride, do nothing
        
    def age_all_members(self):
        """
        Age all members
        Removal of dead ones and addition of new generated offsprings in the Pride is done in Carviz.age_one_day() follow-up calls
        Pride capacity limit already checked in the method Carviz.age_one_day() follow-up calls
        """

        for member in self.members:
            # Age member
            member.age_one_day()

    def pride_wants_to_join(self) -> bool:
        """
        Define if the Pride wants to join the other Prides in the same cell or not
        
        Returns:
            bool: True if average social attitude >= JOIN_THRESHOLD
        """
        
        if not self.members:
            return False
        
        # Compute average social attitude of the Pride's members
        avg_social = sum(member.get_social_attitude() for member in self.members) / len(self.members)
        
        return avg_social >= JOIN_THRESHOLD
    
    def decide_collective_movement(self, available_cells: List['Cell']) -> 'Cell':
        """
        Decide where the Pride should move based on collective hunting strategy
        
        Args:
            available_cells (List[Cell]): List of cells the Pride can move to
                                          The current cell is not present in the cell
                                          No "water" cells are present
            
        Returns:
            Cell: Chosen destination Cell, can also be the current cell if its have the highest score
        """

        # No available cells, stay in the current cell
        if not available_cells:
            return self.cell
        
        # Add current cell to the list of available cells
        available_cells.append(self.cell)

        # Evaluate each available cell with Pride hunting bonuses
        cell_scores = {} # Dict containing cells - scores values
        index = 0 # Set index of the dict

        for cell in available_cells:
            # Collective evaluation - average of all members' preferences, with hunting coordination bonus
            total_score = 0.0
            for member in self.members:
                score = member.evaluate_cell_desirability_carviz(cell)
                total_score += score
            
            avg_score = total_score / len(self.members)
            
            # Apply hunting coordination bonus for cells with prey
            if cell.get_erbast_count() > 0:
                avg_score += self.hunting_coordination * 50
            
            cell_scores[index] = avg_score
            index += 1
        
        # Return the best cell, so the one with the maximum score
        index_best_cell = max(cell_scores.keys(), key=lambda index: cell_scores[index])
        return available_cells[index_best_cell]
      
    def collective_move_to(self, new_cell: 'Cell') -> bool:
        """
        Move to a new cell and pay movement cost
        Recall single Carviz can_follow_group() method

        Args:
            new_cell (Cell): New cell

        Returns:
            bool: True if movement happened, False otherwise
        """

        for member in self.members:
            if not member.can_follow_group():
                # Carviz decides not to move, so remove it from the Pride
                self.remove_member(member)

                # Single Craviz hunts
                erbast_to_hunt = member.search_erbast_to_hunt()
                if erbast_to_hunt: # Hunt happen only if there is an Erbast to hunt
                    member.hunt(erbast_to_hunt, 0.0)

        # Now the Pride moves to the new cell
        # Add to visited cells memory (keep last 10 cells)
        self.visited_cells.append(self.cell)
        if len(self.visited_cells) > 10:
            self.visited_cells.pop(0)

        # Remove Pride from old cell
        self.cell.remove_pride(self)

        # Update position and decrease energy
        self.cell = new_cell # Set new cell
        for member in self.members:
            member.set_cell(new_cell)
            member.set_energy(member.get_energy() - MOVEMENT_COST) # Movement cost
            member.set_can_move(False)

        # Add Pride to new cell's list of Prides
        self.cell.add_pride(self)

        self.can_move = False # Pride cannot move again until next day
    
    def collective_hunt(self):
        """
        Have all Pride members hunt together in the current cell
        1. First the Pride looks for the weakest individual Erbast
        2. If none, look for the weakest Erbast inside the Herds in the cell
        3. If still none, no hunt takes place (social attitude and hunting attributes drop)
        """

        # Pride cannot move anymore
        self.can_move = False
        for member in self.members:
            member.set_can_move(False)

        # Choose a target
        erbast_to_hunt = None

        # 1. Look among individual Erbasts
        if self.cell.get_erbast_individuals():
            erbast_to_hunt = self.cell.get_erbast_with_lowest_energy_single(self.cell.get_erbast_individuals())

        # 2. Otherwise look inside herds
        if not erbast_to_hunt and self.cell.get_herds():
            erbast_to_hunt = self.cell.get_erbast_with_lowest_energy_herds(self.cell.get_herds())

        # 3️. Still none, this implies no hunt, apply penalties and return False
        if not erbast_to_hunt:
            for member in self.members:
                member.set_social_attitude(member.get_social_attitude() - 0.05)
                member.modify_hunting_attributes(-0.05, -0.05)
            return # No hunt

        # Erbast is found, execute the hunt

        # Pay group energy cost due to hunting
        for member in self.members:
            member.set_energy(member.get_energy() - HUNT_ENERGY_COST)

        # Champions attack in descending-energy order until the hunt is success or extinction of the Pride (unlikely but can happen)
        while self.members:
            carviz_highest_energy = self.get_member_with_highest_energy()
            if carviz_highest_energy.hunt(erbast_to_hunt, self.hunting_coordination):
                # Successful kill
                # hunt() method already modifies erbast_to_hunt's attributes and carviz_highest_energy's attributes
                
                # Now modify attributes of other Pride's members
                for member in self.members:
                    if member != carviz_highest_energy:
                        member.set_energy(member.get_energy() + erbast_to_hunt.get_energy() * 0.1) # Only get a fraction of the energy
                        member.modify_hunting_attributes(0.02, 0.02)
                        member.set_days_since_last_hunt(0) # Reset Carviz last hunt counter to 0

                self.hunting_coordination = self.calculate_hunting_coordination()

                # Hunt completed, can return
                return

            # Unsuccessful attempt – recalculate coordination and continue
            self.hunting_coordination = self.calculate_hunting_coordination()

        # Worst case: entire Pride dies, remove it from the cell (unlikely but can happen)
        self.cell.remove_pride(self)