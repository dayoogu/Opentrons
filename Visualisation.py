import re
import matplotlib.pyplot as plt
import imageio
import numpy as np
import os
import pandas as pd

# Define grid layout
grid_rows, grid_cols = 4, 3
numbers = np.array([[1, 2, 3],  
                    [4, 5, 6],
                    [7, 8, 9],
                    [10, 11, 0]])

# Define dictionary for slot positions
slot_positions = {
    1: (0, 0), 2: (1, 0), 3: (2, 0),
    4: (0, 1), 5: (1, 1), 6: (2, 1),
    7: (0, 2), 8: (1, 2), 9: (2, 2),
    10: (0, 3), 11: (1, 3)
}

# Well plate parameters
well_rows = 8  # A to H
well_cols = 12  # 1 to 12
well_radius = 0.04  # Size of each well

# Reservoir parameters
reservoir_rows = 1  
reservoir_cols = 12  

# Directory for storing frames
frame_dir = "frames"
os.makedirs(frame_dir, exist_ok=True)

def parse_steps(user_input):
    """
    Parses user input to extract:
    - Well plate slot number
    - Reservoir slot number
    - Dispensing steps with column information
    - Reservoir column being aspirated
    """
    well_plate_slot = None
    reservoir_slot = None
    steps = []
    reservoir_filled_columns = set()  # To track which columns of the reservoir are used

    # Detect well plate slot
    well_plate_pattern = r"Dispensing.*into (A\d+) of NEST 96 Well Plate.*on slot (\d+)"
    well_plate_matches = re.findall(well_plate_pattern, user_input)

    if well_plate_matches:
        for match in well_plate_matches:
            column_index = int(match[0][1:]) - 1  # Convert A1 -> 0, A2 -> 1, etc.
            well_plate_slot = int(match[1])  # Extract well plate slot
            steps.append((column_index, well_plate_slot))

    # Detect reservoir slot and column
    reservoir_pattern = r"Aspirating.*from (A\d+) of NEST 12 Well Reservoir.*on slot (\d+)"
    reservoir_matches = re.findall(reservoir_pattern, user_input)

    if reservoir_matches:
        for match in reservoir_matches:
            reservoir_column = int(match[0][1:]) - 1  # Extract column index from "A1" -> 0, "A2" -> 1
            reservoir_slot = int(match[1])  # Extract slot number
            reservoir_filled_columns.add(reservoir_column)  # Track filled reservoir columns

    return steps, well_plate_slot, reservoir_slot, reservoir_filled_columns


def draw_grid(frame_num, filled_columns, well_plate_slot=None, reservoir_slot=None, reservoir_filled_columns=set()):
    fig, ax = plt.subplots(figsize=(9, 11))
    ax.set_xlim(0, grid_cols * 1.25)  
    ax.set_ylim(0, grid_rows)  

    slot_width = 1.25
    slot_height = 1

    # Draw grid slots
    for i in range(grid_rows):
        for j in range(grid_cols):
            slot_number = numbers[i, j]
            if slot_number != 0:
                ax.add_patch(plt.Rectangle((j * slot_width, i), slot_width, slot_height, 
                                           fill=True, facecolor='lightgray', edgecolor='white', lw=5))
                ax.text(j * slot_width + slot_width / 2, i + slot_height / 2, str(slot_number), 
                        fontsize=12, color='gray',
                        ha='center', va='center', fontweight='bold')

    # Draw well plate in the correct slot
    if well_plate_slot in slot_positions:
        x_slot, y_slot = slot_positions[well_plate_slot]

        slot_x_pos = x_slot * slot_width
        slot_y_pos = y_slot * slot_height

        plate_x_center = slot_x_pos + slot_width / 2
        plate_y_center = slot_y_pos + slot_height / 2

        plate_x_offset = plate_x_center - (slot_width * 0.8) / 2  
        plate_y_offset = plate_y_center - (slot_height) / 2  

        for row in range(well_rows):
            for col in range(well_cols):
                x = plate_x_offset + (col / well_cols) * slot_width * 0.9  
                y = plate_y_offset + (1 - (row / well_rows)) * slot_height * 0.9  

                color = "blue" if col in filled_columns and row == 0 else "white"

                circle = plt.Circle((x, y), well_radius, edgecolor="black", facecolor=color, lw=0.5)
                ax.add_patch(circle)

    # Draw reservoir in the correct slot
    if reservoir_slot in slot_positions:
        x_slot, y_slot = slot_positions[reservoir_slot]

        slot_x_pos = x_slot * slot_width  
        slot_y_pos = y_slot * slot_height  

        reservoir_x_center = slot_x_pos + slot_width / 2
        reservoir_y_center = slot_y_pos + slot_height / 2

        reservoir_x_offset = reservoir_x_center - (slot_width * 0.9) / 2
        reservoir_y_offset = reservoir_y_center - (slot_height * 0.77) / 2

        for col in range(reservoir_cols):
            x = reservoir_x_offset + (col / reservoir_cols) * slot_width * 0.9
            y = reservoir_y_offset

            color = "lightblue" if col in reservoir_filled_columns else "white"  # Highlight filled column
            rectangle = plt.Rectangle((x, y), slot_width / reservoir_cols, slot_height * 0.8,
                                      edgecolor="black", facecolor=color, lw=0.5)
            ax.add_patch(rectangle)

    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)

    # Save frame
    frame_path = os.path.join(frame_dir, f"frame_{frame_num}.png")
    plt.savefig(frame_path, dpi=100)
    plt.close()
    return frame_path

def generate_animation(user_input):
    steps, well_plate_slot, reservoir_slot, reservoir_filled_columns = parse_steps(user_input)
    frames = []

    filled_columns = set()

    frame_number = 0
    frames.append(draw_grid(frame_number, filled_columns, well_plate_slot, reservoir_slot, reservoir_filled_columns))  

    for step in steps:
        column, slot = step
        well_plate_slot = slot  

        frame_number += 1
        frames.append(draw_grid(frame_number, filled_columns, well_plate_slot, reservoir_slot, reservoir_filled_columns))  
        filled_columns.add(column)
        frame_number += 1
        frames.append(draw_grid(frame_number, filled_columns, well_plate_slot, reservoir_slot, reservoir_filled_columns))  

    output_gif = "well_plate_grid_animation.gif"
    imageio.mimsave(output_gif, [imageio.imread(f) for f in frames], duration=2, loop=0)

    print(f"GIF saved as {output_gif}")


# Example input
user_input = """
	Aspirating 100.0 uL from A1 of NEST 12 Well Reservoir 15 mL on slot 2 at 94.0 uL/sec
	Dispensing 100.0 uL into A1 of NEST 96 Well Plate 200 µL Flat on slot 3 at 94.0 uL/sec
    Aspirating 100.0 uL from A2 of NEST 12 Well Reservoir 15 mL on slot 2 at 94.0 uL/sec
	Dispensing 100.0 uL into A1 of NEST 96 Well Plate 200 µL Flat on slot 3 at 94.0 uL/sec
    Aspirating 100.0 uL from A1 of NEST 96 Well Plate 200 µL Flat on slot 3 at 94.0 uL/sec
	Dispensing 100.0 uL into A2 of NEST 96 Well Plate 200 µL Flat on slot 3 at 94.0 uL/sec
	Aspirating 100.0 uL from A2 of NEST 96 Well Plate 200 µL Flat on slot 3 at 94.0 uL/sec
	Dispensing 100.0 uL into A3 of NEST 96 Well Plate 200 µL Flat on slot 3 at 94.0 uL/sec
	Aspirating 100.0 uL from A3 of NEST 96 Well Plate 200 µL Flat on slot 3 at 94.0 uL/sec
	Dispensing 100.0 uL into A4 of NEST 96 Well Plate 200 µL Flat on slot 3 at 94.0 uL/sec
	Aspirating 100.0 uL from A4 of NEST 96 Well Plate 200 µL Flat on slot 3 at 94.0 uL/sec
	Dispensing 100.0 uL into A5 of NEST 96 Well Plate 200 µL Flat on slot 3 at 94.0 uL/sec
	Aspirating 100.0 uL from A5 of NEST 96 Well Plate 200 µL Flat on slot 3 at 94.0 uL/sec
	Dispensing 100.0 uL into A6 of NEST 96 Well Plate 200 µL Flat on slot 3 at 94.0 uL/sec
	Aspirating 100.0 uL from A6 of NEST 96 Well Plate 200 µL Flat on slot 3 at 94.0 uL/sec
	Dispensing 100.0 uL into A7 of NEST 96 Well Plate 200 µL Flat on slot 3 at 94.0 uL/sec
	Aspirating 100.0 uL from A7 of NEST 96 Well Plate 200 µL Flat on slot 3 at 94.0 uL/sec
	Dispensing 100.0 uL into A8 of NEST 96 Well Plate 200 µL Flat on slot 3 at 94.0 uL/sec
	Aspirating 100.0 uL from A8 of NEST 96 Well Plate 200 µL Flat on slot 3 at 94.0 uL/sec
	Dispensing 100.0 uL into A9 of NEST 96 Well Plate 200 µL Flat on slot 3 at 94.0 uL/sec
	Aspirating 100.0 uL from A9 of NEST 96 Well Plate 200 µL Flat on slot 3 at 94.0 uL/sec
	Dispensing 100.0 uL into A10 of NEST 96 Well Plate 200 µL Flat on slot 3 at 94.0 uL/sec
	Aspirating 100.0 uL from A10 of NEST 96 Well Plate 200 µL Flat on slot 3 at 94.0 uL/sec
	Dispensing 100.0 uL into A11 of NEST 96 Well Plate 200 µL Flat on slot 3 at 94.0 uL/sec
	Aspirating 100.0 uL from A11 of NEST 96 Well Plate 200 µL Flat on slot 3 at 94.0 uL/sec
	Dispensing 100.0 uL into A12 of NEST 96 Well Plate 200 µL Flat on slot 3 at 94.0 uL/sec
"""

# Run animation generator
generate_animation(user_input)
