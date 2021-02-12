import requests


def _iterate_tags(text, open_tag, close_tag):
    while open_tag in text:
        row_start = text.index(open_tag)
        text = text[row_start + len(open_tag) :]
        row_end = text.index(close_tag)
        row = text[:row_end]
        text = text[row_end:]
        yield row


def tickets_for_plate(plate):
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
    if "No search results. Please check" in response.text:
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
        amount = next(_iterate_tags(row, 'citation-value">', "</span>"))
        details_id = next(_iterate_tags(row, "openDetails", '"'))
        results.append(
            dict(status=status, date=date, amount=amount, details_id=details_id)
        )
    return results

