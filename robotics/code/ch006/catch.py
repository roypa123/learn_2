# catch.py - a hand moves to where the ball will land: measure, compare, correct, repeat
setpoint = 1.2        # the ball will land 1.2 m to the right (where we WANT the hand)
hand = 0.0            # the hand starts at 0 m
gain = 4              # how strongly we correct: hand speed = gain x error
dt = 0.05             # one loop every 0.05 s (20 loops per second)

for step in range(21):
    t = step * dt
    measurement = hand                 # SENSE: where is my hand?
    error = setpoint - measurement     # THINK: how far is it from where it should be?
    speed = gain * error               #        correct more when the error is bigger
    if step % 4 == 0:
        print("t =", round(t, 2), "s | hand", round(hand, 3), "m | error", round(error, 3), "m | speed", round(speed, 2), "m/s")
    hand = hand + speed * dt           # ACT: move the hand for one loop
