import json
import sys
import time

import requests

from cross_product import RandomCrossProduct
from ticket_info import tickets_for_plate, ticket_details


def all_plates():
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numbers = "1234567890"
    num_plates = [
        n1 + n2 + n3 + n4
        for n1 in numbers
        for n2 in numbers
        for n3 in numbers
        for n4 in numbers
    ]
    letter_plates = [l1 + l2 + l3 for l1 in letters for l2 in letters for l3 in letters]
    for letters, numbers in RandomCrossProduct(letter_plates, num_plates):
        yield letters + numbers


def main():
    # verify=False normally causes a ton of verbose output
    requests.packages.urllib3.disable_warnings()  # pylint: disable=no-member

    session = requests.Session()
    for plate in all_plates():
        try:
            for ticket in tickets_for_plate(plate, session=session):
                if ticket["details_id"]:
                    details = ticket_details(ticket["details_id"], session=session)
                    ticket["details"] = details
                print(json.dumps(ticket))
        except ValueError:
            print(f"failed to fetch info for plate: {plate}", file=sys.stderr)
            time.sleep(1)  # so we don't thrash some failing network


if __name__ == "__main__":
    main()
