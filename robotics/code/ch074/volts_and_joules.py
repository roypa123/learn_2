# volts_and_joules.py - a volt is a joule per coulomb, so energy = volts x coulombs
batteries = [
    # name, volts, mAh
    ("Rover, 6 x AA NiMH", 7.2, 2000),
    ("USB power bank", 5.0, 10000),
    ("drone 4S LiPo", 14.8, 5000),
    ("9 V block", 9.0, 550),
]
print(f"{'battery':20s} {'volts':>6s} {'mAh':>6s} {'coulombs':>9s} {'joules':>9s} {'Wh':>6s}")
for name, volts, mah in batteries:
    coulombs = mah / 1000 * 3600
    joules = volts * coulombs                 # each coulomb carries 'volts' joules
    print(f"{name:20s} {volts:6.1f} {mah:6d} {coulombs:9.0f} {joules:9.0f} {joules / 3600:6.1f}")

print()
print("check of the Chapter 5 rule 'Wh = V x Ah':")
print(f"  7.2 V x 2.0 Ah = {7.2 * 2.0:.1f} Wh, and 51,840 J / 3,600 = {51840 / 3600:.1f} Wh: the same")
print()
# how much charge does one job cost?
job_j = 1.6 * 9.81 * 60               # lifting a 1.6 kg drone 60 m (Chapter 67)
print(f"lifting 1.6 kg by 60 m needs {job_j:.0f} J")
print(f"at 14.8 V that is {job_j / 14.8:.1f} C of charge if nothing is wasted")
print(f"with half the energy wasted as heat: {job_j / 14.8 / 0.5:.1f} C = {job_j / 14.8 / 0.5 / 3.6:.1f} mAh")
