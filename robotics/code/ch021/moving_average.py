# moving_average.py - smooth noisy readings with the average of the last few
WINDOW = 3                           # how many readings to average

readings = [10, 12, 9, 11, 30, 10, 12, 11, 9, 10]    # 30 is a noise spike

smoothed = []
for i in range(len(readings)):
    start = max(0, i - WINDOW + 1)   # never go before the start of the list
    recent = readings[start:i + 1]   # a slice: at most the last WINDOW readings
    smoothed.append(sum(recent) / len(recent))

for raw, avg in zip(readings, smoothed):     # walk both lists together
    print(f"raw {raw:3d}   smoothed {avg:5.1f}")
