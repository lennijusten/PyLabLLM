import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap, to_rgba_array, Normalize

with open('pca-assembly-operations.json', 'r') as file:
    assembly_operations = json.load(file)


def plot_well_plate(stage_data, stage):
    # Initialize a 96-well plate as an 8x12 grid
    plate = np.zeros((8, 12))

    # Get source and destination wells
    well_mapping = stage_data["well_mapping"]

    # Convert well IDs to indices
    def well_to_index(well_id):
        row = ord(well_id[0].upper()) - ord('A')
        col = int(well_id[1:]) - 1
        return (row, col)

    # Mark the destination wells
    for dest_well in well_mapping.keys():
        row, col = well_to_index(dest_well)
        plate[row, col] = 1  # Mark this well as containing a liquid

    # Create a plot
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.imshow(plate, cmap="Greens", interpolation='nearest')

    # Setting grid
    ax.set_xticks(np.arange(-.5, 12, 1), minor=True)
    ax.set_yticks(np.arange(-.5, 8, 1), minor=True)
    ax.grid(which='minor', color='black', linestyle='-', linewidth=2)

    # Adding well identifiers
    for i in range(8):
        for j in range(12):
            ax.text(j, i, f"{chr(65 + i)}{j + 1}", ha='center', va='center', color='black')

    ax.set_title(f"Stage {stage} 96-Well Plate")
    plt.show()


plot_well_plate(assembly_operations["1"], stage=1)
plot_well_plate(assembly_operations["2"], stage=2)
plot_well_plate(assembly_operations["3"], stage=3)
plot_well_plate(assembly_operations["4"], stage=4)

# Define colors for each stage (extend this list if there are more stages)
hex_colors = ['#FFFFFF', '#38b0de', '#f34c0d', '#ab910b', '#ebb512', '#d5caf0']
colors = to_rgba_array(hex_colors)

custom_cmap = LinearSegmentedColormap.from_list("custom_cmap", colors, N=len(hex_colors))
norm = Normalize(vmin=0, vmax=len(hex_colors)-1)

def well_to_index(well_id):
    row = ord(well_id[0].upper()) - ord('A')
    col = int(well_id[1:]) - 1
    return (row, col)

def update(stage_key):
    stage_data = assembly_operations[stage_key]
    stage = int(stage_key)
    # Initialize a 96-well plate as an 8x12 grid
    plate = np.zeros((8, 12))
    well_mapping = stage_data["well_mapping"]
    # Mark the destination wells with a unique value per stage, using precise indexing for colors
    for dest_well in well_mapping.keys():
        row, col = well_to_index(dest_well)
        plate[row, col] = stage  # Direct stage indexing

    ax.clear()
    ax.imshow(plate, cmap=custom_cmap, norm=norm, interpolation='nearest')
    ax.set_xticks(np.arange(-.5, 12, 1), minor=True)
    ax.set_yticks(np.arange(-.5, 8, 1), minor=True)
    ax.grid(which='minor', color='black', linestyle='-', linewidth=2)
    ax.set_title(f"Stage {stage} 96-Well Plate")
    for i in range(8):
        for j in range(12):
            ax.text(j, i, f"{chr(65 + i)}{j + 1}", ha='center', va='center', color='black')

fig, ax = plt.subplots(figsize=(8, 4))
ani = FuncAnimation(fig, update, frames=sorted(assembly_operations.keys()), repeat=False)
plt.show()

ani.save('assembly_operations.gif', writer='pillow', fps=2)

