from constants import *

class Vegetob:
    """
    Represents the "plant life" in the Planisuss world
    Vegetob grows in ground cells and serves as food for Erbasts
    """
    
    def __init__(self, density: float):
        """
        Initialize Vegetob with a given density (not validated)
        
        Args:
            density (float): Initial density value with bound checking
        """

        self.density = max(MIN_VEGETOB_DENSITY, min(MAX_VEGETOB_DENSITY, density))
    
    # Now I implement getter and setter methods for Vegetob's attribute

    # density (float)
    def get_density(self) -> float:
        """
        Getter method of density attribute
        
        Returns: 
            float: Vegetob density
        """

        return self.density
    
    def set_density(self, density: float):
        """ 
        Setter method of density attribute with bound check
        
        Args:
            density (float): Density value to set
        """

        self.density = max(MIN_VEGETOB_DENSITY, min(MAX_VEGETOB_DENSITY, density))

    # Now I define other methods

    def grow(self):
        """
        The Vegetob density grows dynamically based on its current value
        Instead of growing by a fixed amount each day, the growth rate is proportional to how much "room"
        is left to reach the maximum density (i.e., the lower the density, the faster it grows)
        - When density is low  => growth is near maximum (DYNAMIC_GROWING_RATE)
        - When density is high => growth slows down
        """

        self.density = min(MAX_VEGETOB_DENSITY, self.density + DYNAMIC_GROWING_RATE * (1 - self.density / MAX_VEGETOB_DENSITY))
        
    def consume(self, amount: float) -> float:
        """
        Consume a specified amount of Vegetob
        
        Args:
            amount (float): Amount to consume

        Returns:
            float: Actual amount consumed (may be less if Vegetob density is lower than the requested amount)
        """

        consumed = min(amount, self.density)
        self.density -= consumed
        
        return consumed