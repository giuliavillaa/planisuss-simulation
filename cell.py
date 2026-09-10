from __future__ import annotations
from typing import List, Optional, Tuple, TYPE_CHECKING
import random
from constants import *
from vegetob import Vegetob

if TYPE_CHECKING: # Only for type checkers
    from erbast import Erbast
    from carviz import Carviz
    from herd import Herd
    from pride import Pride

class Cell:
    """
    Represents a single cell in the Planisuss world grid
    Each cell has a position, terrain type ("water" or "ground") and can contain species and Vegetob
    """
    
    def __init__(self, row: int, col: int, terrain_type: str):
        """
        Initialize a cell with its position and terrain type
        Define species' attributes only if the cell is a "ground" cell
        
        Args:
            row (int): Row coordinate in the grid (start from 0)
            col (int): Column coordinate in the grid (start from 0)
            terrain_type (str): Either "water" or "ground"
        """

        self.position = (row, col)
        self.terrain_type = terrain_type
        
        # Initialize attributes related to species only for "ground" cell
        if self.terrain_type == "ground":
            # Random initial Vegetob density
            self.vegetob = Vegetob(random.uniform(INITIAL_VEGETOB_MIN, INITIAL_VEGETOB_MAX))

            # Individual animal lists (before social grouping)
            self.erbast_individuals: List['Erbast'] = [] # Will contain Erbast objects
            self.carviz_individuals: List['Carviz'] = [] # Will contain Carviz objects
            
            # Social group lists (after daily grouping)
            self.herds: List['Herd'] = [] # Will contain Herd objects
            self.prides: List['Pride'] = [] # Will contain Pride objects

    # Now I implement getter and setter methods for Cell's attributes

    # position (Tuple[int, int])
    def get_position(self) -> Tuple[int, int]:
        """
        Getter method of position attribute

        Returns:
            Tuple[int, int]: (row, column) coordinates of the cell
        """

        return self.position

    def set_position(self, position: Tuple[int, int]):
        """
        Setter method of position attribute

        Args:
            position (Tuple[int, int]): (row, column) coordinates to set
        """

        self.position = position

    # terrain_type (str)
    def get_terrain_type(self) -> str:
        """
        Getter method of terrain_type attribute

        Returns:
            str: terrain type of the cell ("water" or "ground")
        """

        return self.terrain_type

    def set_terrain_type(self, terrain_type: str):
        """
        Setter method of terrain_type attribute

        Args:
            terrain_type (str): terrain type to set to the cell
        """

        self.terrain_type = terrain_type

    # vegetob (Vegetob)
    def get_vegetob(self) -> 'Vegetob':
        """
        Getter method of vegetob attribute

        Returns:
            Vegetob: Vegetob object contained in the cell
        """

        return self.vegetob

    def set_vegetob(self, vegetob: 'Vegetob'):
        """
        Setter method of vegetob attribute

        Args:
            vegetob (Vegetob): Vegetob object to set
        """

        self.vegetob = vegetob

    # erbast_individuals (List[Erbast])
    def get_erbast_individuals(self) -> List['Erbast']:
        """
        Getter method of erbast_individuals attribute

        Returns:
            List[Erbast]: list of Erbast individuals present in the cell
        """

        return self.erbast_individuals

    def set_erbast_individuals(self, erbast_individuals: List['Erbast']):
        """
        Setter method of erbast_individuals attribute

        Args:
            erbast_individuals (List[Erbast]): list of Erbasts to set
        """

        self.erbast_individuals = erbast_individuals

    # carviz_individuals (List[Carviz])
    def get_carviz_individuals(self) -> List['Carviz']:
        """
        Getter method of carviz_individuals attribute

        Returns:
            List[Carviz]: list of Carviz individuals present in the cell
        """

        return self.carviz_individuals

    def set_carviz_individuals(self, carviz_individuals: List['Carviz']):
        """
        Setter method of carviz_individuals attribute

        Args:
            carviz_individuals (List[Carviz]): list of Carvizs to set
        """

        self.carviz_individuals = carviz_individuals

    # herds (List[Herd])
    def get_herds(self) -> List['Herd']:
        """
        Getter method of herds attribute

        Returns:
            List[Herd]: list of Herds present in the cell
        """

        return self.herds

    def set_herds(self, herds: List['Herd']):
        """
        Setter method of herds attribute

        Args:
            herds (List[Herd]): list of Herds to set
        """

        self.herds = herds

    # prides (List[Pride])
    def get_prides(self) -> List['Pride']:
        """
        Getter method of prides attribute

        Returns:
            List[Pride]: list of Prides present in the cell
        """

        return self.prides

    def set_prides(self, prides: List['Pride']):
        """
        Setter method of prides attribute

        Args:
            prides (List[Pride]): list of Prides to set
        """

        self.prides = prides

    # Now I define other methods

    def is_ground(self) -> bool:
        """
        Check if this cell contains ground
        
        Returns:
            bool: True if "ground" cell, False if "water" cell
        """

        return self.terrain_type == "ground"
    
    def get_erbast_with_lowest_energy_single(self, list_erbast: List['Erbast']) -> Optional['Erbast']:
        """
        Get the Erbast with lowest level of energy in the list given as parameter
        If no Erbast is present in the list, the None is returned

        Args:
            list_erbast (List[Erbast]): List of Erbasts where to find the one with lowest energy, can be empty
        
        Returns:
            Optional[Erbast]: Erbast with lowest energy or None if the list is empty
        """

        if not list_erbast: # Empty list
            return None

        # At beginning, the Erbast with lowest energy is the first one
        erbast_lowest_energy = list_erbast[0]
        lowest_energy = erbast_lowest_energy.get_energy()

        # Iterate through the other Erbasts and check their level of energy
        for erbast in list_erbast[1:]:
            if(erbast.get_energy() < lowest_energy):
                # Found new Erbast with lower energy than the current lowest
                erbast_lowest_energy = erbast
                lowest_energy = erbast.get_energy()

        return erbast_lowest_energy
    
    def get_erbast_with_lowest_energy_herds(self, list_herds: List['Herd']) -> Optional['Erbast']:
        """
        Get the Erbast with lowest level of energy in the list of Herds given as parameter
        In no Erbast is present in any list of Herds, then None is returned

        Args:
            list_herds (List[Herd]): List of Herds where to find the Erbast with lowest energy
        
        Returns:
            Optional[Erbast]: Erbast with lowest energy, or None if the list is empty
        """

        if not list_herds: # Empty list
            return None

        # While loop to find the first Herd that contains at least an Erbast
        # Then find the Erbast with lowest energy in that herd
        i = 0
        while i < len(list_herds) and not list_herds[i].get_members():
            i += 1
        
        # Check if no Erbast is found in any Herd
        if i == len(list_herds):
            return None
        
        # Use the method get_erbast_with_lowest_energy_single() to find the Erbast with lowest Erbast energy in the Herd
        erbast_lowest_energy = self.get_erbast_with_lowest_energy_single(list_herds[i].get_members())
        if not erbast_lowest_energy:
            return None
        
        lowest_energy = erbast_lowest_energy.get_energy()

        # Iterate through list_herds and check if there is one Erbast with lower energy
        for j in range(i + 1, len(list_herds)):
            members = list_herds[j].get_members()
             # Check if the Herd has no members
            if not members:
                continue # Skip

            # Get the Erbast with lowest energy in the current Herd using the method get_erbast_with_lowest_energy_single()
            herd_erbast_lower_energy = self.get_erbast_with_lowest_energy_single(members)

            # If the Erbast has lower energy than the current lowest, update it
            if herd_erbast_lower_energy and herd_erbast_lower_energy.get_energy() < lowest_energy:
                erbast_lowest_energy = herd_erbast_lower_energy
                lowest_energy = herd_erbast_lower_energy.get_energy()

        return erbast_lowest_energy
    
    def get_erbast_count(self) -> int:
        """
        Get total number of Erbast in this cell (individuals + those in Herds)

        Returns:
            int: Integer value representing the total number of Erbasts
        """

        # Check cell type
        if self.terrain_type == "ground": # Cell is a "ground" cell, so return the actual value
            individual_count = len(self.erbast_individuals)
            herd_count = sum(herd.get_size() for herd in self.herds)
            return individual_count + herd_count
        
        return 0 # The cell is a "water" cell, so return 0
    
    def get_carviz_count(self) -> int:
        """
        Get total number of Carviz in this cell (individuals + those in Prides)

        Returns:
            int: Integer value representing the total number of Carvizs
        """

        # Check cell type
        if self.terrain_type == "ground": # Cell is a "ground" cell, so return the actual value
            individual_count = len(self.carviz_individuals)
            pride_count = sum(pride.get_size() for pride in self.prides)
            return individual_count + pride_count

        return 0 # The cell is a "water" cell, so return 0
    
    def add_erbast(self, erbast: 'Erbast'):
        """
        Add an Erbast individual to this cell
        
        Args:
            erbast (Erbast): Erbast object to add
        """

        if self.terrain_type == "ground":
            self.erbast_individuals.append(erbast) # Successfully added
        
    def add_carviz(self, carviz: 'Carviz'):
        """
        Add a Carviz individual to this cell
        
        Args:
            carviz (Carviz): Carviz object to add
        """

        if self.terrain_type == "ground":
            self.carviz_individuals.append(carviz) # Successfully added
          
    def remove_erbast(self, erbast: 'Erbast'):
        """
        Remove a given Erbast individual from this cell
        
        Args:
            erbast (Erbast): Erbast object to remove
        """

        try:
            self.erbast_individuals.remove(erbast) # Erbast object is found and removed
        except ValueError:
            pass # Erbast object is not found
    
    def remove_carviz(self, carviz: 'Carviz'):
        """
        Remove a given Carviz individual from this cell
        
        Args:
            carviz (Carviz): Carviz object to remove
        """
        
        try:
            self.carviz_individuals.remove(carviz) # Carviz object is found and removed
        except ValueError:
            pass # Carviz object is not found
    
    def add_herd(self, herd: 'Herd'):
        """
        Add a Herd in this cell
        
        Args:
            herd (Herd): Herd of Erbasts object to add
        """

        if self.terrain_type == "ground":
            self.herds.append(herd) # Successfully added
        
    def add_pride(self, pride: 'Pride'):
        """
        Add a Pride in this cell
        
        Args:
            pride (Pride): Pride of Carvizs object to add
        """

        if self.terrain_type == "ground":
            self.prides.append(pride) # Successfully added
          
    def remove_herd(self, herd: 'Herd'):
        """
        Remove a given Herd from this cell
        
        Args:
            herd (Herd): Herd of Erbasts object to remove
        """

        try:
            self.herds.remove(herd) # Herd object is found and removed
        except ValueError:
            pass # Herd object is not found
    
    def remove_pride(self, pride: 'Pride'):
        """
        Remove a given Pride from this cell
        
        Args:
            pride (Pride): Pride of Carvizs object to remove
        """
        
        try:
            self.prides.remove(pride) # Pride object is found and removed
        except ValueError:
            pass # Pride object is not found

    def get_vegetob_density(self) -> float:
        """
        Get current Vegetob density in this cell
        
        Returns:
            float: vegetob density value (0.0 for "water" cell)
        """
        
        if self.terrain_type == "ground":
            return self.vegetob.get_density() # The cell is a "ground" cell, so return the actual value
        
        return 0.0 # The cell is a "water" cell, so return 0.0
    
    def grow_vegetob(self):
        """
        Increase Vegetob density in this cell
        Call to method vegetob.grow()
        """

        self.vegetob.grow() # Vegetob density successful grow
    
    def consume_vegetob(self, amount: float) -> float:
        """
        Consume Vegetob from this cell and return the amount actually consumed
        
        Args:
            amount (float): Desired amount to consume

        Returns:
            float: Actual amount consumed (may be less than the desidered amount)
        """
        
        return self.vegetob.consume(amount)
        
    def initiate_daily_social_groups(self):
        """
        Group individual animals into herds and prides at the start of each day
        This method implements the social group formation, following a five-phase logic:
        1. Herds and Prides with 0 or 1 member are eliminated
        2. Individual Erbasts are aggregated in already existing Herds or new ones
        3. Individual Carvizs are aggregated in already existing Prides oe new ones
        4. Merge existing Herds
        5. Merge existing Prides or make them fight between each other
        """

        # Check type: handle animals and social groups for "ground" cell, do nothing for "water" cell
        if self.terrain_type == "ground":
            # 1. Clear Herds and Prides if a single Herd and Pride has 0 or only 1 member
            for herd in self.herds[:]: # Iterate over a copy to safely remove
                herd.eliminate()

            for pride in self.prides[:]: # Iterate over a copy to safely remove
                pride.eliminate()

            # 2. Form new Herds from Erbast individuals
            self.handle_single_erbasts()

            # 3. Form new Prides from Carviz individuals
            self.handle_single_carvizs()

            # 4. Merge Herds in a single Herd
            self.merge_herds()

            # 5. Merge Prides in a single Pride or make them fight between each other until only 1 Pride survive
            self.merge_or_fight_prides()

    def handle_single_erbasts(self):
        """
        This method organizes Erbast individuals into Herds, following a three-phase logic:
        1. Attempt to fill existing Herds with ungrouped Erbasts until each Herd reaches MAX_HERD
        2. Form as many new full Herds (size == MAX_HERD) as possible from the remaining Erbast individuals
        3. If 2 or more Erbasts are still ungrouped, create a final Herd with them
        If only one Erbast remains, it stays as an individual

        Note: Herd constructor automatically removes added members from self.erbast_individuals
        """

        # 1. Try to insert each individual Erbast into any existing Herd
        for erbast in self.erbast_individuals[:]: # Iterate over a copy
            for herd in self.herds:
                if herd.get_size() < MAX_HERD and herd.add_member(erbast):
                    break # Successfully placed; go to next Erbast
            
            # If the loops ends without a break, the Erbast remains in erbast_individuals and will be handled below

        # 2. Remaining Erbasts form new Herds
        from herd import Herd
        while len(self.erbast_individuals) >= MAX_HERD:
            self.herds.append(Herd(self, self.erbast_individuals[:MAX_HERD]))

        # 3. If at least 2 Erbasts are still ungrouped, create one last Herd
        if len(self.erbast_individuals) >= 2:
            self.herds.append(Herd(self, self.erbast_individuals))

    def handle_single_carvizs(self):
        """
        This method organizes Carviz individuals into Pride, following a three-phase logic:
        1. Attempt to fill existing Prides with ungrouped Carvizs until each Pride reaches MAX_PRIDE
        2. Form as many new full Prides (size == MAX_PRIDE) as possible from the remaining Carviz individuals
        3. If 2 or more Carvizs are still ungrouped, create a final Pride with them
        If only one Carviz remains, it stays as an individual

        Note: Pride constructor automatically removes added members from self.carviz_individuals
        """

        # 1. Try to insert each individual Carviz into any existing Pride
        for carviz in self.carviz_individuals[:]: # Iterate over a copy
            for pride in self.prides:
                if pride.get_size() < MAX_PRIDE and pride.add_member(carviz):
                    break # Successfully placed; go to next Carviz
            
            # If the loops ends without a break, the Carviz remains in carviz_individuals and will be handled below

        # 2. Remaining Carvizs form new Prides
        from pride import Pride
        while len(self.carviz_individuals) >= MAX_PRIDE:
            self.prides.append(Pride(self, self.carviz_individuals[:MAX_PRIDE]))

        # 3. If at least 2 Carvizs are still ungrouped, create one last Pride
        if len(self.carviz_individuals) >= 2:
            self.prides.append(Pride(self, self.carviz_individuals))

    def merge_herds(self):
        """
        This method merges partially filled Herds to reduce fragmentation and maximize Herd sizes

        - Begin with the first Herd (herds[0]) and attempt to fill it with members from subsequent Herds
        - Once herds[0] is full, move on to herds[1], and so on
        - For each Herd, add members from later Herds until full or until no more members are available
        - After each transfer, the source Herd is checked and possibly eliminated via herd.eliminate():
        """

        i = 0 # index of the “target” Herd
        while i < len(self.herds):
            target = self.herds[i]

            # Redundant check: skip / drop empty target Herds
            if target.get_size() == 0:
                target.eliminate() # Herd.eliminate(), removes itself from the cell
                continue

            # Target already full, so move on to next Herd
            if target.get_size() >= MAX_HERD:
                i += 1
                continue

            # Pull members from later (donor) Herds
            donor_idx = i + 1
            while donor_idx < len(self.herds) and target.get_size() < MAX_HERD:
                donor_herd = self.herds[donor_idx]

                # Move members one-by-one from donor Herd into target
                for member in donor_herd.get_members()[:]: # Iterate over a copy
                    if target.get_size() >= MAX_HERD: # Target just filled, so exit the loop
                        break

                    # Member can be added in the target Herd
                    donor_herd.remove_member(member) # Remove member from donor Herd
                    if target.add_member(member): # Add member to target Herd
                        # Merge the member’s visited-cell history into the target Herd
                        for cell in member.get_visited_cells():
                            if cell not in target.get_visited_cells():
                                target.get_visited_cells().append(cell)

                # Now I eliminate donor Herd
                if donor_herd.get_size() <= 1:
                    donor_herd.eliminate() # Herd.eliminate(), removes itself from the cell
                else:
                    donor_idx += 1 # Donor Herd still viable, can be considered in later iterations

            # Done with this target Herd, move to the next one
            i += 1

        # Due to the fact that donor_herd.eliminate() adds single Erbasts in erbast_individuals,
        # I recall method handle_single_erbasts() to further handle them
        self.handle_single_erbasts()
    
    def merge_or_fight_prides(self):
        """
        Merge Prides or make them fight until only one Pride remains in this cell
        Rules implemented:
        - If more than one Pride is present, they evaluate whether to join.
            - A Pride “wants to join” when the average social-attitude of its members is >= JOIN_THRESHOLD
            - If two Prides both want to join, the smaller one merges into the larger (all members move; donor Pride is removed)
        - If either Pride refuses, they fight:
            - Champions (highest-energy members) duel one-to-one
            - The member with lower energy dies; winner gains a small SOCIAL_BOOST
            - Repeat until one Pride has no members left (last blood fight); the empty Pride is eliminated
        - With more than 2 Prides, the procedure is applied iteratively, starting with the two smallest
          Whenever a merge or a fight ends, the list is resorted by size so the next pair is always the two smallest
        - The loop stops when either one Pride remains in self.prides
        """

        # Nothing to do if 0 or 1 pride

        if len(self.prides) > 1:
            while len(self.prides) > 1:
                # Always keep the list sorted by ascending size
                self.prides.sort(key=lambda p: len(p.members))
                
                pride_a = self.prides[0] # Smallest
                pride_b = self.prides[1] # Second-smallest

                join_a = pride_a.pride_wants_to_join()
                join_b = pride_b.pride_wants_to_join()

                # Join case: both are True and MAX_PRIDE limit is respected, otherwise a fight takes place
                if join_a and join_b and pride_a.get_size() + pride_b.get_size() <= MAX_PRIDE:
                    # Merge the smaller Pride (pride_a) into pride_b
                    for member in pride_a.get_members()[:]: # Iterate over a copy
                        pride_a.remove_member(member)
                        pride_b.add_member(member)
                        
                        # Merge the member’s visited-cell history into the pride_b
                        for cell in member.get_visited_cells():
                            if cell not in pride_b.get_visited_cells():
                                pride_b.get_visited_cells().append(cell)

                    # donor pride becomes empty, so eliminate it
                    pride_a.eliminate()

                # Fight case
                else:
                    while pride_a.get_size() > 0 and pride_b.get_size() > 0:
                        champ_a = pride_a.get_member_with_highest_energy()
                        champ_b = pride_b.get_member_with_highest_energy()

                        if champ_a.get_energy() >= champ_b.get_energy(): # Champ_a won
                            # Champ_b dies, no offsprings generated
                            champ_b.die()
                        
                        else: # Champ_b won
                            # Champ_a dies, no offsprings generated
                            champ_a.die()

                    # Eliminate whichever pride is now empty and increase other Pride's members social_attitude
                    if pride_a.get_size() == 0:
                        pride_a.eliminate()
                        pride_b.modify_social_attitude_from_fight(SOCIAL_BOOST_FROM_FIGHT)
                    
                    if pride_b.get_size() == 0:
                        pride_b.eliminate()
                        pride_a.modify_social_attitude_from_fight(SOCIAL_BOOST_FROM_FIGHT)

                # Resort so that the next iteration starts with two smallest prides
                self.prides.sort(key=lambda p: len(p.members))

    def is_overwhelmed_by_vegetob(self, ground_neighbors: List['Cell']):
        """
        A cell is overwhelmed by Vegetob when all of its "ground" neighbors have maximum Vegetob density
        The rule of overwhelming still applies even if neighbors are "water" cells, in that case only consider "ground" cells
        Check if this cell is completely surrounded by cells with maximum Vegetob density
        When this happens, animals in the cell are overwhelmed and die
        
        Args:
            ground_neighbors (List[Cell]): List of "ground" neighbors cells
        """
        
        # If no "ground" neighbors, can't be overwhelmed, the cell is isolated
        if not ground_neighbors:
            return # No overwhelming
        
        # Check if all neighboring "ground" cells have maximum Vegetob density
        for ground_neighbor in ground_neighbors:
            if ground_neighbor.get_vegetob_density() < MAX_VEGETOB_DENSITY:
                return # No overwhelming
        
        # If this point is reach => There is overwhelming
        # Clear all animals
        self.clear_animals()
    
    def clear_animals(self):
        """
        Remove all animals from this cell (used when overwhelmed by Vegetob) and kill them
        No need to check for type of the cell, it is called only when the cell is a "ground" cell
        """

        # Erbast individuals die and they will be removed from the cell directly in die() method
        for erbast in self.erbast_individuals[:]: # Loop over a copy to avoid skips, die() can safely remove the Erbast from the original list
            erbast.die() # No offsprings generated
        
        # Carviz individuals die and they will be removed from the cell directly in die() method
        for carviz in self.carviz_individuals[:]: # Loop over a copy to avoid skips, die() can safely remove the Carviz from the original list
            carviz.die() # No offsprings generated

        # All Erbast in all Herds die and they will be removed from the cell directly in die() method
        for herd in self.herds[:]:
            for erbast in herd.get_members()[:]: # Loop over a copy to avoid skips, die() can safely remove the Erbast from the original list
                erbast.die() # No offsprings generated
        self.herds.clear()

        # All Carviz in all Prides die and they will be removed from the cell directly in die() method
        for pride in self.prides[:]:
            for carviz in pride.get_members()[:]: # Loop over a copy to avoid skips, die() can safely remove the Carviz from the original list
                carviz.die() # No offsprings generated
        self.prides.clear()