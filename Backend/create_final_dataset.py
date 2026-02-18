import csv
import random

rows = []

with open("damage_scores.csv", "r") as f:
    reader = csv.DictReader(f)
    for r in reader:
        damage = float(r["damage_score"])

        population = random.randint(10000, 100000)
        hospitals = random.randint(0, 5)
        roads = random.choice([0, 1])

        if damage > 7 and population > 50000:
            priority = "High"
        elif damage > 4:
            priority = "Medium"
        else:
            priority = "Low"

        rows.append([
            r["region_id"],
            damage,
            population,
            hospitals,
            roads,
            priority
        ])

with open("final_dataset.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "region_id",
        "damage_score",
        "population",
        "hospitals",
        "roads",
        "priority"
    ])
    writer.writerows(rows)

print("final_dataset.csv created with", len(rows), "rows")
input("PRESS ENTER TO EXIT")