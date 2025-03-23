import streamlit as st # type: ignore
import math
import matplotlib.pyplot as plt

# Set the title and description
st.set_page_config(page_title="Gear Design Calculator", layout="wide")
st.title("⚙️ Gear Design Calculator")
st.write("This app calculates gear parameters based on the number of teeth and module value.")

# Sidebar inputs
st.sidebar.header("Gear Input Parameters")
teeth = st.sidebar.slider("Number of Teeth", min_value=5, max_value=100, value=20, step=1)
module = st.sidebar.slider("Module", min_value=0.5, max_value=10.0, value=2.5, step=0.1)

# Function to calculate gear parameters
def gear_calculator(teeth, module):
    if teeth <= 0 or module <= 0:
        return None, "Error: Teeth and module must be positive numbers."
    
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
    }, None

# Function to draw the gear
def draw_gear(teeth, module):
    pitch_radius = (module * teeth) / 2
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_aspect('equal')
    
    # Draw pitch circle
    pitch_circle = plt.Circle((0, 0), pitch_radius, color='b', fill=False, linestyle='dashed', label='Pitch Circle')
    ax.add_patch(pitch_circle)
    
    # Draw gear teeth
    for i in range(teeth):
        angle = (2 * math.pi * i) / teeth
        x1, y1 = pitch_radius * math.cos(angle), pitch_radius * math.sin(angle)
        x2, y2 = (pitch_radius + module) * math.cos(angle), (pitch_radius + module) * math.sin(angle)
        ax.plot([x1, x2], [y1, y2], 'r')
    
    ax.set_xlim(-pitch_radius - module, pitch_radius + module)
    ax.set_ylim(-pitch_radius - module, pitch_radius + module)
    plt.title("Gear Visualization", fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid()

    return fig

# Calculate gear parameters
gear_params, error = gear_calculator(teeth, module)

# Display results in columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Gear Parameters")
    if error:
        st.error(error)
    else:
        for key, value in gear_params.items():
            st.metric(label=key, value=f"{value:.2f}")

with col2:
    st.subheader("🛠️ Gear Visualization")
    fig = draw_gear(teeth, module)
    st.pyplot(fig)

st.sidebar.write("🔹 Adjust the sliders to see real-time changes.")
