# error_count.py - count how often each kind of event appears in a robot's log
log = "bump ok ok bump lowbatt ok bump stall ok ok bump lowbatt".split()

counts = {}                     # an empty dictionary
for event in log:
    counts[event] = counts.get(event, 0) + 1     # 0 the first time we see it

for event in sorted(counts):    # going through a dictionary gives its keys
    print(f"{event:8} {counts[event]}")

most = max(counts, key=counts.get)
print("most common:", most, "| different kinds:", len(counts))
