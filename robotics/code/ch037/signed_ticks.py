# signed_ticks.py - forward is plus, backward is minus
TICKS_PER_METRE = 2600

moves = [1300, -650, 2600, -3900, 650]    # encoder ticks for each move

position = 0
travelled = 0

print("  move  position  travelled")
for move in moves:
    position = position + move
    travelled = travelled + abs(move)
    print(f"{move:6d} {position:9d} {travelled:10d}")

print(f"ended {position / TICKS_PER_METRE:+.2f} m from the start")
print(f"wheels rolled {travelled / TICKS_PER_METRE:.2f} m in total")
