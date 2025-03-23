import math
import tkinter as tk
from tkinter import messagebox

# Ensure Matplotlib is available before importing
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

def gear_calculator(teeth, module):
    if teeth <= 0 or module <= 0:
        raise ValueError("Teeth and module must be positive numbers.")
    
    pitch_diameter = module * teeth
    addendum = module
    dedendum = 1.157 * module
    whole_depth = addendum + dedendum
    circular_pitch = math.pi * module
    
    return {
        "Pitch Diameter": pitch_diameter,
        "Addendum": addendum,
        "Dedendum": dedendum,
        "Whole Depth": whole_depth,
        "Circular Pitch": circular_pitch
    }

def draw_gear(teeth, module, canvas_frame):
    if not MATPLOTLIB_AVAILABLE:
        messagebox.showerror("Error", "Matplotlib is not installed. Please install it using 'pip install matplotlib'.")
        return
    
    pitch_radius = (module * teeth) / 2
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    
    # Draw pitch circle
    pitch_circle = plt.Circle((0, 0), pitch_radius, color='b', fill=False, linestyle='dashed', label='Pitch Circle')
    ax.add_patch(pitch_circle)
    
    # Draw teeth (approximated as small lines)
    for i in range(teeth):
        angle = (2 * math.pi * i) / teeth
        x1, y1 = pitch_radius * math.cos(angle), pitch_radius * math.sin(angle)
        x2, y2 = (pitch_radius + module) * math.cos(angle), (pitch_radius + module) * math.sin(angle)
        ax.plot([x1, x2], [y1, y2], 'r')
    
    ax.set_xlim(-pitch_radius - module, pitch_radius + module)
    ax.set_ylim(-pitch_radius - module, pitch_radius + module)
    plt.title("Gear Visualization")
    plt.legend()
    plt.grid()
    
    # Embed Matplotlib figure in Tkinter
    for widget in canvas_frame.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

def calculate_and_draw():
    try:
        teeth = int(teeth_entry.get())
        module = float(module_entry.get())
        
        if teeth <= 0 or module <= 0:
            raise ValueError
        
        gear_params = gear_calculator(teeth, module)
        
        # Display calculated parameters
        result_text.set("\n".join([f"{key}: {value:.2f}" for key, value in gear_params.items()]))
        
        # Draw gear visualization
        draw_gear(teeth, module, canvas_frame)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid positive numeric values.")

# Create Tkinter GUI
root = tk.Tk()
root.title("Gear Design Calculator")

# Input fields
tk.Label(root, text="Number of Teeth:").pack()
teeth_entry = tk.Entry(root)
teeth_entry.pack()

tk.Label(root, text="Module:").pack()
module_entry = tk.Entry(root)
module_entry.pack()

# Calculate button
tk.Button(root, text="Calculate & Visualize", command=calculate_and_draw).pack()

# Result display
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, justify="left")
result_label.pack()

# Canvas for gear visualization
canvas_frame = tk.Frame(root)
canvas_frame.pack()

# Run the app
root.mainloop()
