# joint_path.py - move an arm joint smoothly from one angle to another in equal steps
start_deg = 20.0
end_deg = 80.0
steps = 6                           # how many equal pieces

for i in range(steps + 1):          # + 1 so that we include the last point
    fraction = i / steps            # goes from 0.0 to 1.0
    angle_deg = start_deg + (end_deg - start_deg) * fraction
    print(f"step {i}: {angle_deg:.1f} degrees")
