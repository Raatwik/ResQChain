import os
import json
import csv
print("Hello")


LABEL_DIR = "labels/train"

def damage_score(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)

    # Count damage types
    counts = {
        "minor-damage": 0,
        "major-damage": 0,
        "destroyed": 0
    }

    buildings = data.get("features", {}).get("xy", [])
    total = len(buildings)

    if total == 0:
        return 0

    for b in buildings:
        subtype = b.get("properties", {}).get("subtype", "no-damage")
        if subtype in counts:
            counts[subtype] += 1

    # Weighted damage score
    score = (
        counts["minor-damage"] +
        counts["major-damage"] * 2 +
        counts["destroyed"] * 3
    ) / total

    # Scale to 0–10
    return round(score * 3.3, 2)


rows = []

print("Starting damage score extraction...")

for root, _, files in os.walk(LABEL_DIR):
    for file in files:
        if not file.lower().endswith(".json"):
            continue

        path = os.path.join(root, file)
        try:
            score = damage_score(path)
            rows.append([file, score])
        except Exception as e:
            print("Skipped file:", file, "Error:", e)

print("Processed regions:", len(rows))

# Write CSV
with open("damage_scores.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["region_id", "damage_score"])
    writer.writerows(rows)

print("damage_scores.csv created successfully")
input("PRESS ENTER TO EXIT")
