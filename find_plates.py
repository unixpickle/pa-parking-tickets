import random

import requests

from cross_product import RandomCrossProduct


def check_response(plate):
    response = requests.post(
        "https://onlineserviceshub.com/ParkingPortal/Philadelphia/Home/DoSearch",
        data={
            "SearchBy": "plate",
            "OtherFirstField": plate,
            "OtherSecondField": "",
            "State": "PA",
            "X-Requested-With": "XMLHttpRequest",
        },
        verify=False,
    )
    return not ("No search results. Please check" in response.text)


def shuffle(arr):
    c = list(arr)
    random.shuffle(c)
    return c


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
    for plate in all_plates():
        if check_response(plate):
            print("-----")
            print("found plate: " + plate)
            print("-----")
            return


if __name__ == "__main__":
    main()
