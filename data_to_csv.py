"""
Convert output from scan.py to an anonymized CSV file.
"""

import csv
import json
import random


def main():
    # Assumes data.json comes from `python scan.py >data.json`.
    with open("data.json", "rt") as f:
        lines = [x.strip() for x in f.readlines()]
    objs = [json.loads(x) for x in lines]
    objs = [x for x in objs if "details" in x and x["details"] and x["date"]]
    for obj in objs:
        obj["plate"] = obj["details"]["License Plate"]

    plates = list(set([obj["plate"] for obj in objs]))
    random.shuffle(plates)
    plate_to_id = {x: i for i, x in enumerate(plates)}

    with open("data.csv", "wt") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "car_id",
                "year",
                "month",
                "day",
                "amount",
                "violation",
                "vehicle_make",
            ],
        )
        writer.writeheader()
        for obj in sorted(objs, key=date_key):
            month, day, year = obj["date"].split("/")
            writer.writerow(
                {
                    "car_id": plate_to_id[obj["plate"]],
                    "year": int(year),
                    "month": int(month),
                    "day": int(day),
                    "amount": float(obj["amount"]),
                    "violation": obj["details"]["Violation"],
                    "vehicle_make": obj["details"]["Vehicle Make"],
                }
            )


def date_key(obj):
    month, day, year = obj["date"].split("/")
    return (int(year), int(month), int(day))


if __name__ == "__main__":
    main()
