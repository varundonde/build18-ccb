# create the file for dispensing instruction

# This is a draft for the main functionality of the dispenser
import random


# Assuming we generate random volumes to dispense
def generate_dispensing_volumes(num_pumps=6, total_volume=100):
    # Generate (num_pumps - 1) random cut points between 1 and total_volume-1
    cut_points = sorted(random.sample(range(1, total_volume), num_pumps - 1))

    # Add start and end to the cut points for slicing
    cut_points = [0] + cut_points + [total_volume]

    # Generate the volumes as differences between consecutive cut points
    volumes_to_dispense = [cut_points[i + 1] - cut_points[i] for i in range(num_pumps)]

    return volumes_to_dispense


dispensing_volumes = generate_dispensing_volumes()

# Output results
print("Dispensing Volumes:", dispensing_volumes)
print("Sum of Volumes:", sum(dispensing_volumes))
