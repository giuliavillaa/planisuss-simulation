import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import constants

class GameConfigWindow:
    """
    Configuration window for setting game parameters before starting a new game
    The user can adjust various constants that affect the game mechanics
    """
    
    def __init__(self, parent: tk.Toplevel):
        """
        Initialize the configuration window
        
        Args:
            parent (tk.Toplevel): The parent window
        """

        self.parent = parent
        self.config_values = {}
        self.create_config_window()

    # Now I implement getter and setter methods for GameConfigWindow's attributes

    # parent (tk.Toplevel)
    def get_parent(self) -> tk.Toplevel:
        """
        Getter method of parent attribute
        
        Returns:
            The parent window object
        """

        return self.parent

    def set_parent(self, parent: tk.Toplevel):
        """
        Setter method of parent attribute
        
        Args:
            parent (tk.Toplevel): The parent window object
        """
        
        self.parent = parent

    def get_config_values(self) -> dict:
        """
        Getter method of config_values attribute
        
        Returns:
            dict: Dictionary containing configuration entry widgets and their validation info
        """
        return self.config_values

    def set_config_values(self, config_values: dict):
        """
        Setter method of config_values attribute
        
        Args:
            config_values (dict): Dictionary containing configuration entry widgets and their validation info
        """

        if not isinstance(config_values, dict):
            raise TypeError("config_values must be a dictionary")
        
        self.config_values = config_values
    
    # Now I define other methods

    def create_config_window(self):
        """
        Create and display the configuration window
        """
        
        self.config_window = tk.Toplevel(self.parent)
        self.config_window.title("Game Configuration")
        self.config_window.resizable(False, False) # Prevent resizing
        self.config_window.grab_set() # Make window modal
        
        # Main frame with padding
        main_frame = tk.Frame(self.config_window, padx = 20, pady = 15)
        main_frame.pack(fill = 'both', expand = True)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text = "Configure Your Planisuss World",
            font = ("Segoe UI", 14, "bold")
        )
        title_label.pack(pady = (0, 15))
        
        # Create notebook for tabbed interface
        # User can switch between different configuration sections
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill = 'both', expand = True, pady = (0, 15))
        
        # World tab, where user can configure world parameters
        world_frame = ttk.Frame(notebook)
        notebook.add(world_frame, text = "World")
        self.create_world_config(world_frame)

        # Population tab, where user can configure animal populations
        pop_frame = ttk.Frame(notebook)
        notebook.add(pop_frame, text = "Population")
        self.create_population_config(pop_frame)
        
        # Buttons frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill = 'x', pady = (10, 0))
        
        # Default button to reset values to defaults
        tk.Button(
            button_frame,
            text = "Reset to Defaults Values",
            command = self.reset_to_defaults,
            width = 25
        ).pack(side = 'left')
        
        # Cancel button to close the configuration window and go back to launcher
        tk.Button(
            button_frame,
            text = "Cancel",
            command = self.cancel_config,
            width = 12
        ).pack(side = 'right', padx = (5, 0))
        
        # Start Game button to validate inputs and start the game
        tk.Button(
            button_frame,
            text = "Start Game",
            command = self.start_game,
            width = 12,
        ).pack(side = 'right')
        
        # Center the window
        self.center_window()
        
        # Load default values
        self.load_default_values()
    
    def create_world_config(self, parent: ttk.Frame):
        """
        Create world-related configuration options
        Constants that can be set by the user to modify the game world:
        - NUMCELLS_R: Number of rows in the world (between 10 and 30)
        - NUMCELLS_C: Number of columns in the world (between 10 and 30)
        - NUMDAYS: Total simulation days (between 100 and 5000)
        - WATER_RATIO: Fraction of inner cells of the world that will be water (between 0.1 and 0.25)

        Args:
            parent (ttk.Frame): The parent frame to hold the configuration options
        """

        frame = tk.Frame(parent, padx = 25, pady = 10)
        frame.pack(fill = 'both', expand = True)
        
        # Define configuration options
        # Each tuple contains: (label text, constant name, min value, max value, values range string for user)
        configs = [
            ("Number Of Rows", "NUMCELLS_R", 10, 30, "Range: from 10 to 30"),
            ("Number Of Columns", "NUMCELLS_C", 10, 30, "Range: from 10 to 30"),
            ("Maximum Number Of Days", "NUMDAYS", 100, 5000, "Range: from 100 to 5000"),
            ("Fraction Of Inner Cells That Will Be Water", "WATER_RATIO", 0.1, 0.25, "Range: from 0.1 to 0.25")
        ]
        
        # Create each configuration row
        for i, (label, const_name, min_val, max_val, range) in enumerate(configs):
            self.create_config_row(frame, label, const_name, min_val, max_val, range, i)
    
    def create_population_config(self, parent: ttk.Frame):
        """
        Create population-related configuration options
        Constants that can be set by the user to modify the game world:
        - INITIAL_ERBAST_RATIO: Initial ratio of Erbasts per ground cell (between 1 and 4)
        - INITIAL_CARVIZ_RATIO: Initial ratio of Carvizs per ground cell (between 0.20 and 1)
        - MAX_HERD: Maximum number of Erbasts in a Herd (between 10 and 50)
        - MAX_PRIDE: Maximum number of Carvizs in a Pride (between 10 and 40)
        
        Args:
            parent (ttk.Frame): The parent frame to hold the configuration options
        """

        frame = tk.Frame(parent, padx = 25, pady = 10)
        frame.pack(fill = 'both', expand = True)
        
        # Define configuration options
        # Each tuple contains: (label text, constant name, min value, max value, values range string for user)
        configs = [
            ("Initial Erbast Ratio In Cell", "INITIAL_ERBAST_RATIO", 1.0, 4.0, "Range: from 1 to 4"),
            ("Initial Carviz Ratio In Cell", "INITIAL_CARVIZ_RATIO", 0.2, 1.0, "Range: from 0.2 to 1"),
            ("Max Herd Size", "MAX_HERD", 10, 50, "Range: from 10 to 50"),
            ("Max Pride Size", "MAX_PRIDE", 10, 40, "Range: from 10 to 40"),
        ]
        
        # Create each configuration row
        for i, (label, const_name, min_val, max_val, range) in enumerate(configs):
            self.create_config_row(frame, label, const_name, min_val, max_val, range, i)
    
    def create_config_row(self, parent: tk.Frame, label_text: str, const_name: str, min_val, max_val, range: str, row: int):
        """
        Create a configuration row with label, entry, ranges and range suggestion for user input
        
        Args:
            parent (tk.Frame): The parent frame to hold the row
            label_text (str): Text for the label
            const_name (str): Name of the constant to be configured
            min_val: Minimum value allowed for this constant (can be int or float)
            max_val: Maximum value allowed for this constant (can be int or float)
            range (str): Text to display the values range for user input
            row (int): Row index for grid layout
        """

        # Set label values
        label = tk.Label(parent, text = label_text + ":", width = 35, anchor = 'w')
        label.grid(row = row, column = 0, sticky = 'w', pady = 2)
        
        # User entry form
        entry = tk.Entry(parent, width=15)
        entry.grid(row = row, column = 1, padx = (10, 5), pady = 2)
        
        # Store reference to entry
        self.config_values[const_name] = {
            'entry': entry,
            'min': min_val,
            'max': max_val,
            'type': type(getattr(constants, const_name, min_val))
        }
        
        # Range value for user
        range_label = tk.Label(parent, text = range, width = 35, anchor = 'w')
        range_label.grid(row = row, column = 2, sticky='w', padx = (5, 0), pady = 2)
    
    def load_default_values(self):
        """
        Load default values from constants.py into the entry fields
        """
        
        for const_name, config in self.config_values.items():
            # Get the default value from constants.py
            default_value = getattr(constants, const_name)
            config['entry'].delete(0, tk.END)
            config['entry'].insert(0, str(default_value))
    
    def reset_to_defaults(self):
        """
        Reset all values to their defaults set in constants.py
        """
        
        self.load_default_values()
        messagebox.showinfo("Reset", "All values have been reset to defaults.")
    
    def validate_inputs(self) -> list[str]:
        """
        Validate all input values
        Ensure they are within the specified bounds and of correct type
        
        Returns:
            list[str]: A list of error messages for any invalid inputs
        """
        
        errors = []
        
        # Iterate through all configured constants
        for const_name, config in self.config_values.items():
            try:
                value_str = config['entry'].get().strip()
                # Check if the entry is empty
                if not value_str:
                    errors.append(f"{const_name}: Value cannot be empty")
                    continue
                
                # Convert to appropriate type
                if config['type'] == int:
                    value = int(float(value_str)) # Allow decimal input from user but convert it to int
                else:
                    value = float(value_str)
                
                # Check bounds
                if value < config['min'] or value > config['max']:
                    errors.append(f"{const_name}: Value must be between {config['min']} and {config['max']}")
                
            except ValueError:
                errors.append(f"{const_name}: Invalid number format") # Error accoured, there mist be a valid number input
        
        return errors
    
    def apply_config_values(self):
        """
        Apply the configured values to the constants.py module
        """
        
        # Iterate through config_values
        for const_name, config in self.config_values.items():
            try:
                # Try to set the value
                value_str = config['entry'].get().strip()
                if config['type'] == int:
                    value = int(float(value_str))
                else:
                    value = float(value_str)
                
                setattr(constants, const_name, value)
            except (ValueError, AttributeError) as e:
                print(f"Error setting {const_name}: {e}") # Handle any errors in setting the constant, should not crash the game
    
    def cancel_config(self):
        """
        Cancel configuration and return to launcher window
        This will close the configuration window without starting the game
        """
        
        self.config_window.destroy()
    
    def center_window(self):
        """
        Center the configuration window on screen
        """

        self.config_window.update_idletasks()
        width = 900
        height = 500
        x = (self.config_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.config_window.winfo_screenheight() // 2) - (height // 2)
        self.config_window.geometry(f'{width}x{height}+{x}+{y}')

    def start_game(self):
        """
        Validate user inputs and start the game
        """
        
        errors = self.validate_inputs()
        
        # Check if there are any validation errors, if so, show them in a messagebox
        if errors:
            error_message = "Please fix the following errors:\n\n" + "\n".join(errors)
            messagebox.showerror("Configuration Errors", error_message)
            return
        
        # Apply the configuration values
        self.apply_config_values()

        # Import modules after configuration is applied
        # This ensures they see the updated constants
        from game_manager import GameManager
        from user_interface import PlanisussUI
        
        # Close configuration window
        self.config_window.destroy()
        
        # Close launcher window
        self.parent.destroy()
        
        # Initialize and start the game
        gm = GameManager()
        gm.initialize_world()
        PlanisussUI(gm)

def launch_new():
    """
    Start a fresh simulation with configuration options, where the user can insert constants' values
    """
    
    # Instead of directly starting the game, open configuration window
    GameConfigWindow(welcome)

def launch_load():
    """
    Open file-dialog and load a saved .pkl game
    """
    
    # Open a file dialog to select a saved game file
    path = filedialog.askopenfilename(
        parent = welcome,
        title = "Load saved Planisuss game",
        filetypes = [("Planisuss save files", "*.pkl")]
    )
    
    # If the user cancels the dialog, path will be empty
    if not path:
        return # User cancelled

    # Attempt to load the game state from the selected file
    try:
        # Import GameManager only when needed for loading
        from game_manager import GameManager

        gm = GameManager.load_state(path)
    except Exception as exc: # Error occured
        messagebox.showerror(
            "Load error",
            f"Could not open save file:\n{exc}",
            parent = welcome
        )
        return

    # If successful, close the launcher and start the GUI
    from user_interface import PlanisussUI
    welcome.destroy()
    PlanisussUI(gm)

# Build launcher window to ask for new or load game
root = tk.Tk() # Create the main Tkinter root window
root.withdraw() # Hide the root window

welcome = tk.Toplevel(root) # Create a new top-level window for the launcher
welcome.title("Planisuss") # Set the window title
welcome.resizable(False, False) # Prevent resizing of the launcher window

# Add a welcome label with styling
tk.Label(
    welcome,
    text = "Welcome to Planisuss!",
    font = ("Segoe UI", 16, "bold"),
    padx = 25,
    pady = 25
).pack()

# Create a frame to hold the buttons
btn_frame = tk.Frame(welcome, padx = 20, pady = 10)
btn_frame.pack()

# Button to start a new game
tk.Button(
    btn_frame,
    text = "New Game",
    width = 15,
    command = launch_new
).grid(row = 0, column = 0, padx = 5, pady = 5)

# Button to load a saved game
tk.Button(
    btn_frame,
    text = "Load Game",
    width = 15,
    command = launch_load
).grid(row = 0, column = 1, padx = 5, pady = 5)

# Center the launcher window on the screen
welcome.update_idletasks() # Ensure all geometry has been calculated
window_width = welcome.winfo_width()
window_height = welcome.winfo_height()
screen_width = welcome.winfo_screenwidth()
screen_height = welcome.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
welcome.geometry(f'{window_width}x{window_height}+{x}+{y}')

# Quit if the user closes the launcher
welcome.protocol("WM_DELETE_WINDOW", root.quit)

# Hand control to Tk
root.mainloop()