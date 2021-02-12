import requests


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
