from constants import *
from game_manager import GameManager
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

class PlanisussUI:
    def __init__(self, game_manager: 'GameManager'):
        """
        Initializes the Planisuss GUI with the given game manager
        
        Args:
            game_manager (GameManager): The game manager instance that controls the simulation
        """
        
        self.game = game_manager
        
        # Initialize the game if it hasn't been set up yet
        if self.game.get_size() == 0:
            self.game.initialize_world()

        self.window_size = 200 
        self.simulation_ended = False # Track if simulation has ended

        # Get the effective NUMDAYS for this game instance
        # For loaded games, this might be different from constants.NUMDAYS
        self.effective_numdays = self.get_effective_numdays()

        # create the main window and subplots
        self.fig, (self.ax_map, self.ax_pop, self.ax_veg) = plt.subplots(
            1, 3, figsize = (13, 5),
            gridspec_kw = {'width_ratios': [1, 1, 1]}
        )
        
        plt.subplots_adjust(left = 0.05, right = 0.97, bottom = 0.18)

        # World Map
        self.im = self.ax_map.imshow(self.game.get_map_rgb(), vmin = 0, vmax = 1)
        self.ax_map.set_title("Planisuss World")
        self.ax_map.set_xticks([])
        self.ax_map.set_yticks([])

        # Population Plot
        self.lines = {
            sp: self.ax_pop.plot([], [], color = col, label = sp)[0] for sp, col in COLORS.items()
        }
        self.ax_pop.set_title("Population Over Time")
        self.ax_pop.set_xlabel("Day")
        self.ax_pop.set_ylabel("Count")
        self.ax_pop.legend(loc = 'lower left') # Legend will be shown in the lower left corner

        # Vegetob Plot
        self.veg_line, = self.ax_veg.plot([], [], color = 'gold')
        self.ax_veg.set_title("Average Vegetob Density Over Time")
        self.ax_veg.set_xlabel("Day")
        self.ax_veg.set_ylabel("Avg")

        # Day Label
        self.day_label = self.fig.text(0.5, 0.94, "Day 0", ha = 'center', va = 'center', fontsize = 12)

        # Control buttons, centered in the lower part of the plot
        button_width = 0.1
        button_height = 0.05
        button_spacing = 0.01
        total_width = 5 * button_width + 4 * button_spacing
        start_x = (1.0 - total_width) / 2 # Center the buttons horizontally
        
        self.btn_pause = Button(plt.axes([start_x, 0.05, button_width, button_height]), "Pause")
        self.btn_speed = Button(plt.axes([start_x + button_width + button_spacing, 0.05, button_width, button_height]), "×1")
        self.btn_info = Button(plt.axes([start_x + 2 * (button_width + button_spacing), 0.05, button_width, button_height]), "Get Info")
        self.btn_constants = Button(plt.axes([start_x + 3 * (button_width + button_spacing), 0.05, button_width, button_height]), "Get Constants")
        self.btn_save = Button(plt.axes([start_x + 4 * (button_width + button_spacing), 0.05, button_width, button_height]), "Save")

        # Bind button actions when clicked
        self.btn_pause.on_clicked(self.toggle_pause)
        self.btn_speed.on_clicked(self.cycle_speed)
        self.btn_info.on_clicked(self.get_info)
        self.btn_constants.on_clicked(self.get_constants)
        self.btn_save.on_clicked(self.save_game)
        
        self.fig.canvas.mpl_connect('close_event', self.on_close) # Event handler for window close

        # Set and start timer
        self.timer = self.fig.canvas.new_timer(interval = 50)
        self.timer.add_callback(self.tick)
        self.timer.start()
        self.speed_idx = 0
        self.paused = False

        # Center the Matplotlib (Tkinter) window with fixed preferred size
        manager = plt.get_current_fig_manager()
        try:
            window = manager.window  # This is a Tkinter.Tk() object

            # Set window title
            window.title("Planisuss")
            
            # Set window size
            width = 1300
            height = 650
            x = (window.winfo_screenwidth() // 2) - (width // 2)
            y = (window.winfo_screenheight() // 2) - (height // 2)
            window.geometry(f"{width}x{height}+{x}+{y}")
        except AttributeError:
            pass  # Do nothing if it is not possible to center the window

        # Show the window and plots
        plt.show()

    def get_effective_numdays(self) -> int:
        """
        Get the effective NUMDAYS for this game instance
        For loaded games, this might be different from the current constants.NUMDAYS
        There are three ways to recover the value of effective_numdays:
        1. Try to get constant's value from the GameManager config_values attribute, if possible
        2. Try to infer constant's value directly from the state of the game, if possible
        3. Use default value defined in constants.py
        If option 1 does not work, then option 2 is followed
        If option 2 does not work, then option 3 is followed

        Returns:
            int: value of NUMDAYS
        """
        
        # 1. Try to get it from the game manager if it was saved
        if hasattr(self.game, 'config_values') and 'NUMDAYS' in self.game.config_values:
            return self.game.config_values['NUMDAYS']
        
        # 2. Try to infer from game history if available
        try:
            history = self.game.get_history()
            if history and 'time' in history and len(history['time']) > 0:
                # If the game has run for more days than current NUMDAYS, I know the original NUMDAYS was higher
                max_day_reached = max(history['time'])
                if max_day_reached >= NUMDAYS:
                    # Estimate: assume it was set to at least the max day reached + buffer
                    # Use a reasonable buffer (20% or minimum 100 days)
                    buffer = max(int(max_day_reached * 0.2), 100)
                    return max_day_reached + buffer
        except (AttributeError, KeyError, TypeError):
            pass  # If history is not available or has issues, fall back to default values
        
        # 3. Fallback to current NUMDAYS defined in constants.py
        return NUMDAYS

    def tick(self):
        """ 
        Timer callback to step the game simulation and redraw the plots
        """
        
        # Check if simulation has reached the maximum number of days
        current_day = int(self.game.get_time())
        if current_day >= self.effective_numdays and not self.simulation_ended:
            self.simulation_ended = True
            self.paused = True # Automatically pause when simulation ends
            self.btn_pause.label.set_text("Resume")
            
            # Update the day label to show simulation ended
            self.day_label.set_text(f"Day {current_day} - SIMULATION ENDED")
            self.day_label.set_color('red') # Change color to indicate end
            self.redraw() # Final redraw
            
            return
        
        # Redraw the game if simulation continues
        if not self.paused and not self.simulation_ended:
            self.game.step(dt=SPEEDS[self.speed_idx])
            self.redraw()

    def redraw(self):
        """
        Redraws the game state in the UI
        """
        
        self.im.set_data(self.game.get_map_rgb())
        current_time = int(self.game.get_time())

        # Update day label based on simulation status
        if self.simulation_ended:
            self.day_label.set_text(f"Day {current_time} - SIMULATION ENDED")
            self.day_label.set_color('red')
        else:
            self.day_label.set_text(f"Day {current_time}")
            self.day_label.set_color('black')

        t, stats = self.game.get_time_series()
        t0 = max(0, len(t) - self.window_size)

        # Population plot (Erbast and Carviz)
        for sp in ['Erbast', 'Carviz']:
            self.lines[sp].set_data(t[t0:], stats[sp][t0:])
        self.ax_pop.set_xlim(t0, len(t)) # Set the x-axis limits from t0 to the length of the time series
        self.ax_pop.relim() # Recalculate limits based on current data
        self.ax_pop.autoscale_view(scaley = True) # Automatically adjust the y-axis based on new data limits


        # Vegetob plot (avg_Vegetob)
        self.veg_line.set_data(t[t0:], stats['avg_Vegetob'][t0:])
        self.ax_veg.set_xlim(t0, len(t)) # Set the x-axis limits from t0 to the length of the time series
        self.ax_veg.relim() # Recalculate limits based on current data
        self.ax_veg.autoscale_view(scaley = True) # Automatically adjust the y-axis based on new data limits

        self.fig.canvas.draw_idle()

    def toggle_pause(self, _):
        """
        Toggles the pause state of the simulation
        When paused, the simulation stops updating
        Clicking again resumes it
        
        Note: If simulation has ended, it cannot be resumed
        """

        # Don't allow resuming if simulation has ended
        if self.simulation_ended and self.paused:
            messagebox.showinfo("Simulation Ended", f"The simulation has completed all {self.effective_numdays} days and cannot be resumed.")
            return
        
        self.paused = not self.paused
        self.btn_pause.label.set_text("Resume" if self.paused else "Pause")

    def cycle_speed(self, _):
        """
        Cycles through the predefined speed multipliers for the simulation
        Each click changes the speed to the next multiplier in the SPEEDS list
        
        Note: Speed cannot be changed if simulation has ended
        """

        # Don't allow speed changes if simulation has ended
        if self.simulation_ended:
            messagebox.showinfo("Simulation Ended", "The simulation has ended. Speed cannot be changed.")
            return
        
        self.speed_idx = (self.speed_idx + 1) % len(SPEEDS)
        self.btn_speed.label.set_text(f"×{SPEEDS[self.speed_idx]}")

    def get_info(self, _):
        """
        Pauses the simulation and opens a new window with additional information
        The following information is displayed:
        - Initial stats - Day 1:
          - Total Erbasts
          - Total Carvizs
          - Total Herds
          - Total Prides
          - Average Vegetob Density
        - Current stats:
          - Total Erbasts
          - Total Carvizs
          - Total Herds
          - Total Prides
          - Average Vegetob Density
        - Changes from initial stats to current stats:
          - Erbast population change
          - Carviz population change
          - Average Vegetob density change
        """
        
        # Pause the simulation if it's not already paused and not ended
        was_paused = self.paused
        if not self.paused and not self.simulation_ended:
            self.toggle_pause(None)
        
        # Get history data to extract statistics
        if not self.game.get_history():
            messagebox.showwarning("No Data", "No simulation data available to display statistics.")
            return
        
        history = self.game.get_history()

        # Get initial stats - Day 1
        initial_stats = self.get_day_stats(history, 0)
        
        # Get current stats
        current_day_index = len(history["time"]) - 1 if history["time"] else 0
        current_stats = self.get_day_stats(history, current_day_index)
        
        # Format the information message
        info_message = self.format_stats_message(initial_stats, current_stats)
        
        # Show the information window
        messagebox.showinfo("Simulation Statistics", info_message)
        
        # Optionally resume the simulation if it wasn't paused before and hasn't ended
        if not was_paused and not self.simulation_ended:
            self.toggle_pause(None) 
    
    def get_constants(self, _):
        """
        Displays the settable constants from the constants module
        Shows only the constants that can be modified to configure the simulation
        """
        
        # Pause the simulation if it's not already paused and not ended
        was_paused = self.paused
        if not self.paused and not self.simulation_ended:
            self.toggle_pause(None)
        
        # Get all constants from the constants module
        constants_message = self.format_constants_message()
        
        # Show the constants window
        messagebox.showinfo("Simulation Constants", constants_message)
        
        # Optionally resume the simulation if it wasn't paused before and not ended
        if not was_paused and not self.simulation_ended:
            self.toggle_pause(None)

    def save_game(self, _):
        """
        Opens a file dialog to save the current game state to a .pkl file
        Use method save_state in GameManager to serialize the game state as binary data
        """
        
        # Pause the simulation if it's not already paused and not ended
        was_paused = self.paused
        if not self.paused and not self.simulation_ended:
            self.toggle_pause(None)

        path = filedialog.asksaveasfilename(defaultextension=".pkl")
        if path:
            self.game.save_state(path)

        # Optionally resume the simulation if it wasn't paused before and not ended
        if not was_paused and not self.simulation_ended:
            self.toggle_pause(None)

    def on_close(self, _):
        """
        Define actions to perform when Planisuss window is closing using the top right X button
        It asks the user if he wants to same the state of the game or just exit
        """
        
        # Event handler for when the window is closed
        if self.paused:
            self.toggle_pause(None)
        
        # Ask user if they want to save the game before quitting
        answer = messagebox.askyesnocancel("Exit", "Save simulation before quitting?")
        if answer is None:
            # User chose to cancel the exit
            if self.paused: 
                self.toggle_pause(None)
            return
        
        if answer:
            # User chose to save the game
            self.save_game(None)

    def get_day_stats(self, history: dict, day_index: int) -> dict:
        """
        Get statistics for a specific day
        
        Args:
            history (dict): The history dictionary containing simulation data
            day_index (int): Index of the day to get stats for (0 = first day)
            
        Returns:
            dict: Dictionary containing all statistics for that day
        """
        
        # Get basic counts from history
        erbasts_count = history["Erbast"][day_index] if day_index < len(history["Erbast"]) else "N/A"
        carvizs_count = history["Carviz"][day_index] if day_index < len(history["Carviz"]) else "N/A"
        avg_vegetob = history["avg_Vegetob"][day_index] if day_index < len(history["avg_Vegetob"]) else "N/A"
        herds_count = history["total_Herds"][day_index] if day_index < len(history["total_Herds"]) else "N/A"
        prides_count = history["total_Prides"][day_index] if day_index < len(history["total_Prides"]) else "N/A"
        
        # Return the statistics as a dictionary
        return {
            "erbasts_count": erbasts_count,
            "carvizs_count": carvizs_count,
            "avg_vegetob": avg_vegetob,
            "herds_count": herds_count,
            "prides_count": prides_count
        }

    def format_stats_message(self, initial_stats: dict, current_stats: dict) -> str:
        """
        Format the statistics into a readable message
        
        Args:
            initial_stats (dict): Initial day statistics
            current_stats (dict): Current day statistics
            
        Returns:
            str: Formatted message string
        """
        
        current_day = int(self.game.get_time())
        
        message = f"=== PLANISUSS SIMULATION STATISTICS ===\n\n"

        # Add simulation status
        if self.simulation_ended:
            message += f"SIMULATION COMPLETED (Day {current_day}/{self.effective_numdays})\n\n"
        else:
            message += f"SIMULATION RUNNING (Day {current_day}/{self.effective_numdays})\n\n"
        
        # Initial stats - Day 1
        message += "INITIAL STATS (Day 1):\n"
        message += f"- Total Erbasts: {initial_stats['erbasts_count']}\n"
        message += f"- Total Carvizs: {initial_stats['carvizs_count']}\n"
        message += f"- Total Herds: {initial_stats['herds_count']}\n"
        message += f"- Total Prides: {initial_stats['prides_count']}\n"
        message += f"- Average Vegetob Density: {initial_stats['avg_vegetob']}\n\n"
        
        # Current stats
        message += f" CURRENT STATS (Day {current_day}):\n"
        message += f"- Total Erbasts: {current_stats['erbasts_count']}\n"
        message += f"- Total Carvizs: {current_stats['carvizs_count']}\n"
        message += f"- Total Herds: {current_stats['herds_count']}\n"
        message += f"- Total Prides: {current_stats['prides_count']}\n"
        message += f"- Average Vegetob Density: {current_stats['avg_vegetob']}\n\n"
        
        # Calculate changes in main stats
        if initial_stats and current_stats:
            message += "CHANGES FROM INITIAL:\n"
            try:
                erbast_change = int(current_stats['erbasts_count']) - int(initial_stats['erbasts_count'])
                carviz_change = int(current_stats['carvizs_count']) - int(initial_stats['carvizs_count'])
                vegetob_change = float(current_stats['avg_vegetob']) - float(initial_stats['avg_vegetob'])
                
                message += f"- Erbast Population: {erbast_change:+d}\n"
                message += f"- Carviz Population: {carviz_change:+d}\n"
                message += f"- Average Vegetob Density: {vegetob_change:+.2f}\n"
                
            except (ValueError, TypeError, KeyError) as e:
                message += "- Error calculating population changes\n" # Got errors while loading current day's stats because of N/A
                
        return message
    
    def format_constants_message(self) -> str:
        """
        Format the settable constants into a readable message
        
        Returns:
            str: Formatted constants message string
        """
        
        message = "=== PLANISUSS SIMULATION CONSTANTS ===\n\n"
        message += "SETTABLE SIMULATION PARAMETERS:\n\n"
        
        # List of specific constants to display
        constants_to_show = [
            'NUMCELLS_R',
            'NUMCELLS_C', 
            'NUMDAYS',
            'WATER_RATIO',
            'INITIAL_ERBAST_RATIO',
            'INITIAL_CARVIZ_RATIO',
            'MAX_HERD',
            'MAX_PRIDE'
        ]
        
        # Get specific constants from the constants module
        import constants
        
        for const_name in constants_to_show:
            try:
                value = getattr(constants, const_name)
                message += f"- {const_name}: {value}\n"
            except AttributeError:
                message += f"- {const_name}: Not found\n"
        
        message += "\nNote: These constants control key aspects of the simulation.\n"
        message += "Modify them in the constants.py file to change simulation behavior."
        
        return message