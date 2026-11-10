# delivery_log.py - Chapter 14's deliveries, now remembering every trip
trips_m = []                         # an empty list: nothing delivered yet

trips_m.append(120.0)
trips_m.append(85.5)
trips_m.append(240.0)
trips_m.append(64.5)

print("trips:", trips_m)
print("deliveries:", len(trips_m))
print("total:", sum(trips_m), "m")
print("average:", sum(trips_m) / len(trips_m), "m")
print("longest:", max(trips_m), "m | shortest:", min(trips_m), "m")
print("trip number of the longest:", trips_m.index(max(trips_m)) + 1)
