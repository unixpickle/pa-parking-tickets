"""
Iterate through license plates in a random order and dump any found tickets to
standard output as JSON objects.
"""

import json
import sys
import random
import time

import requests
from tqdm.auto import tqdm


def main():
    # verify=False normally causes a ton of verbose output
    requests.packages.urllib3.disable_warnings()  # pylint: disable=no-member

    session = requests.Session()
    for plate in tqdm(all_plates()):
        try:
            for ticket in tickets_for_plate(plate, session=session):
                if ticket["details_id"]:
                    details = ticket_details(ticket["details_id"], session=session)
                    ticket["details"] = details
                print(json.dumps(ticket))
        except ValueError:
            print(f"failed to fetch info for plate: {plate}", file=sys.stderr)
            time.sleep(1)  # so we don't thrash some failing network


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
    return RandomCrossProduct(letter_plates, num_plates)


def tickets_for_plate(plate: str, state: str = "PA", session: requests.Session = None):
    """
    Get a list of dicts for a given license plate, where each dict describes
    a ticket.

    More details can be obtained for each ticket using ticket_info() with the
    details_id key of the ticket dict.
    """
    response = (session if session is not None else requests).post(
        "https://onlineserviceshub.com/ParkingPortal/Philadelphia/Home/DoSearch",
        data={
            "SearchBy": "plate",
            "OtherFirstField": plate,
            "OtherSecondField": "",
            "State": state,
            "X-Requested-With": "XMLHttpRequest",
        },
        verify=False,
    )
    if (
        "No search results. Please check" in response.text
        or "<tbody>" not in response.text
    ):
        return []
    idx1 = response.text.index("<tbody>")
    idx2 = response.text.index("</tbody>")
    table = response.text[idx1:idx2]
    results = []
    for row in _iterate_tags(table, "<tr >", "</tr>"):
        columns = list(_iterate_tags(row, "<td>", "</td>"))
        if len(columns) != 7:
            raise ValueError(f"expected 7 columns but got {len(columns)}")
        status = columns[-1]
        date = columns[-2]
        amount = _first_tag(row, 'citation-value">', "</span>")
        details_id = _first_tag(row, "openDetails", '"')
        results.append(
            dict(
                plate=plate,
                state=state,
                status=status,
                date=date,
                amount=amount,
                details_id=details_id,
            )
        )
    return results


def ticket_details(details_id: str, session: requests.Session = None):
    """
    Get info for a specific ticket.

    Usually won't work unless the session has already been used to request
    information about a plate.
    """
    response = (session if session is not None else requests).post(
        "https://onlineserviceshub.com/ParkingPortal/Philadelphia/Home/DoTicketDetails",
        data={"detailKey": details_id},
        verify=False,
    )
    pairs = zip(
        _iterate_tags(
            response.text,
            '<div class="col-6 col-md-3 ticket-details__label">',
            "</div>",
        ),
        _iterate_tags(
            response.text,
            '<div class="col-6 col-md-3 ticket-details__value">',
            "</div>",
        ),
    )
    return {x.strip(): y.strip() for x, y in pairs}


def _iterate_tags(text: str, open_tag: str, close_tag: str):
    while open_tag in text:
        row_start = text.index(open_tag)
        text = text[row_start + len(open_tag) :]
        row_end = text.index(close_tag)
        row = text[:row_end]
        text = text[row_end:]
        yield row


def _first_tag(text: str, open_tag: str, close_tag: str):
    for tag in _iterate_tags(text, open_tag, close_tag):
        return tag
    return None


class RandomCrossProduct:
    """
    Efficient way to iterate over a shuffled cross product of two sets without
    having to pre-compute the cross product.
    """

    def __init__(self, set1, set2):
        self._set1 = set1
        self._set2 = set2

    def __iter__(self):
        buckets = {x: None for x in self._set1}
        total_count = len(self._set1) * len(self._set2)
        while total_count > 0:
            i = random.randrange(total_count)
            for bucket, bucket_items in buckets.copy().items():
                i -= len(self._set2) if bucket_items is None else len(bucket_items)
                if i >= 0:
                    continue
                if bucket_items is None:
                    bucket_items = list(self._set2)
                    buckets[bucket] = bucket_items
                idx = random.randrange(len(bucket_items))
                obj = bucket_items[idx]
                del bucket_items[idx]
                yield bucket + obj
                break
            total_count -= 1

    def __len__(self):
        return len(self._set1) * len(self._set2)


if __name__ == "__main__":
    main()
