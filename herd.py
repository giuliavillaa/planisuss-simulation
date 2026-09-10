from __future__ import annotations 
from typing import List, TYPE_CHECKING
from constants import *

if TYPE_CHECKING: # For static checkers only
    from cell import Cell
    from erbast import Erbast

class Herd:
    """
    Social group for Erbast animals
    Herds are formed when multiple Erbasts are in the same cell and coordinate their movements
    """
    
    def __init__(self, cell: 'Cell', members: List['Erbast']):
        """
        Initialize a Herd with a list of Erbast members
        
        Args:
            cell (Cell): Cell where the Herd is located
            members (List['Erbast']): List of Erbast objects to form the Herd
        """
        
        self.cell = cell
        self.members = members[:] # Copy the list of members to avoid reference issues
        self.visited_cells: List['Cell'] = []
        self.can_move = True # Herd can move by default
        self.forced_to_move = False # Default value: Herd is not forced to move

        for member in self.members:
            # Set all members' current_group reference to this Herd
            member.set_current_group(self)

            # Remove members from the cell's list of individual Erbast
            self.cell.remove_erbast(member)
    
    # Now I implement getter and setter methods for Herd's attributes

    # cell (Cell)
    def get_cell(self) -> 'Cell':
        """
        Getter method of cell attribute

        Returns:
            Cell: Cell where the Herd is located
        """

        return self.cell

    def set_cell(self, cell: 'Cell'):
        """
        Setter method of cell attribute

        Args:
            cell (Cell): Cell to set to the Herd
        """

        self.cell = cell

    # members (List['Erbast'])
    def get_members(self) -> List['Erbast']:
        """
        Getter method of members attribute

        Returns:
            List[Erbast]: list of Erbasts in the Herd
        """

        return self.members

    def set_members(self, members: List['Erbast']):
        """
        Setter method of members attribute

        Args:
            members (List[Erbast]): list of Erbasts to set
        """

        self.members = members

    # visited_cells (List['Cell'])
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

    # forced_to_move (bool)
    def get_forced_to_move(self) -> bool:
        """
        Getter method of forced_to_move attribute

        Returns:
            bool: True if the Herd is forced to move, False otherwise
        """

        return self.forced_to_move

    def set_forced_to_move(self, forced_to_move: bool):
        """
        Setter method of forced_to_move attribute

        Args:
            forced_to_move (bool): True if the Herd must move, False otherwise
        """

        self.forced_to_move = forced_to_move

    # Now I define other methods
    
    def get_size(self) -> int:
        """
        Get number of members in the Herd
        
        Returns:
            int: Number of members in the Herd
        """
        
        return len(self.members)
    
    def eliminate(self):
        """
        Eliminate the Herd is there are no members or there is only one
        It also deals with the cell's lists attributes
        """

        if len(self.members) == 0:
            # Herd is empty => Remove it from the cell
            self.cell.remove_herd(self)
        
        if len(self.members) == 1:
            # Only 1 member => Remove from the Herd and consider it as an individual, re-set its attributes
            self.remove_member(self.members[0])

            # Modify cell's lists
            self.cell.remove_herd(self)
        
        # Do nothing if there are at least 2 members

    def add_member(self, erbast: 'Erbast') -> bool:
        """
        Add an Erbast to the Herd
        
        Args:
            erbast (Erbast): Erbast object to add
            
        Returns:
            bool: True if successfully added, False if Herd is full
        """
        
        if len(self.members) >= MAX_HERD:
            return False
        
        if erbast not in self.members:
            self.cell.remove_erbast(erbast) # Remove Erbast from the cell's list of individual Erbast
            erbast.set_current_group(self) # Set Erbast's current group attribute
            erbast.set_social_attitude(erbast.get_social_attitude() + 0.1) # Increase Erbast's social attitude
            self.members.append(erbast) # Add given Erbast to the Herd
            return True
    
        return False # Erbast already in the Herd

    def remove_member(self, erbast: 'Erbast'):
        """
        Remove an Erbast from the Herd, if present in the Herd
        
        Args:
            erbast (Erbast): Erbast object to remove
        """
        
        try:
            self.members.remove(erbast) # Remove given Erbast
            
             # Re-set Erbast's attributes
            erbast.set_current_group(None)
            erbast.set_cell(self.cell)
            erbast.set_social_attitude(erbast.get_social_attitude() - 0.1)
            erbast.set_visited_cells(self.visited_cells)

            # Add Erbast in the cell's list of Erbast individuals
            self.cell.add_erbast(erbast)

        except ValueError:
            pass # Erbast not present in the Herd, do nothing

    def age_all_members(self):
        """
        Age all members
        Removal of dead ones and addition of new generated offsprings in the Herd is done in Erbast.age_one_day() follow-up calls
        Herd capacity limit already checked in the method Erbast.age_one_day() follow-up calls
        """
        
        for member in self.members:
            # Age member
            member.age_one_day()

    def collective_graze(self):
        """
        Have all Herd members graze in the cell
        Need to handle the case where len(Herd) > amount of Vegetob in the cell
        """

        # Herd decides to graze, so it cannot move anymore
        self.can_move = False
        for member in self.members:
            member.set_can_move(False)

        # Check number of members and available vegetob density
        if len(self.members) > self.cell.get_vegetob_density():
            # "More members than Vegetob density"
            # => Energy points are assigned to those Erbast having the lowest value of Energy, up to exhaustion of the Vegetob of the cell
            
            # Define a list of Erbast in "amount of energy crescent order"
            self.members = sorted(self.members, key=lambda e: e.energy)

            # Now consume Vegetob and increase energy
            current_index = 0
            while self.cell.get_vegetob_density() > 0 and current_index < len(self.members):
                if self.members[current_index].alive:
                    self.members[current_index].graze()
                    current_index += 1

        else: # "More Vegetob density than members"
            for member in self.members:
                if member.alive:
                    member.graze()
    
    def decide_collective_movement(self, available_cells: List['Cell']) -> 'Cell':
        """
        Decide where the Herd should move based on collective evaluation
        
        Args:
            available_cells (List[Cell]): List of cells the herd can move to
                                          The current cell is not present in this list
                                          No "water" cells are present
            
        Returns:
            Cell: Chosen destination cell, can also be the current cell if its have the highest score
        """

        # No available cells, stay in the current cell
        if not available_cells:
            return self.cell
        
        # If the Herd is not forced to move, then also the current cell must be evaluated
        if not self.forced_to_move:
            available_cells.append(self.cell) # Current cell must be considered
            
        # Evaluate each available cell
        cell_scores = {} # Dict containing cells - scores values
        index = 0 # Set index of the dict

        for cell in available_cells:
            # Collective evaluation - average of all members' preferences
            total_score = 0.0
            for member in self.members:
                score = member.evaluate_cell_desirability_erbast(cell)
                total_score += score
            
            avg_score = total_score / len(self.members)
            cell_scores[index] = avg_score
            index += 1
        
        # Choose the best cell
        index_best_cell = max(cell_scores.keys(), key=lambda index: cell_scores[index])
        return available_cells[index_best_cell]
    
    def collective_move_to(self, new_cell: 'Cell'):
        """
        Move to a new cell and pay movement cost
        First it separates the Erbasts who don't follow the Herd (using method Erbast.can_follow_group()) and make them graze
        Then it moves the Herd from the current cell to the new cell, while changing the involved attributes

        Args:
            new_cell (Cell): New cell where to move
        """

        for member in self.members:
            if not member.can_follow_group():
                # Erbast decides not to move, so remove it from the Herd
                self.remove_member(member)

                # Such erbast grazes
                member.graze()

        # Now the Herd moves to the new cell
        # Add to visited cells memory (keep last 10 cells)
        self.visited_cells.append(self.cell)
        if len(self.visited_cells) > 10:
            self.visited_cells.pop(0)

        # Remove Herd from old cell
        self.cell.remove_herd(self)

        # Update position and decrease energy
        self.cell = new_cell # Set new cell
        for member in self.members:
            member.set_cell(new_cell)
            member.set_energy(member.get_energy() - MOVEMENT_COST) # Movement cost
            member.set_can_move(False)

        # Add Herd to new cell's list of Herds
        self.cell.add_herd(self)

        self.can_move = False # Herd cannot move again until next day