import re
from itertools import chain
from typing import Dict

from adapters.excel_adapter import create_xlsx_file
from adapters.exchange_adapter import (
    connect_to_ews,
    count_sent_emails,
    extract_contacts,
    is_email_address_domain_excluded,
    retrieve_sent_items,
    sort_all_emails
)
from domain.entities import Contact


def connect_to_sent_items(username: str, pwd: str, primary_email: str, email_service_address: str):
    account = connect_to_ews(username, pwd, primary_email, email_service_address)
    return retrieve_sent_items(account)


def is_email_address_valid(email: str) -> bool:
    """Checks if email is valid"""

    pattern = r"^([A-z][a-zA-Z0-9\.?(:)!#$%&'*+\-=?^_`{|}~]{0,63}|(\".+\"))@" \
              r"((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.){0,}[a-zA-Z0-9]{1,}))$"
    return bool(re.search(pattern, email))


def get_all_emails_amount(connection_data):
    sorted_sent_emails, sorted_archived_sent_emails = sort_all_emails(connection_data)
    return count_sent_emails(sorted_sent_emails, sorted_archived_sent_emails)


def export(connection_data, username, domain_list, path):
    accumulator: Dict[str, Contact] = dict()
    sorted_sent_emails, sorted_archived_sent_emails = sort_all_emails(
        connection_data=connection_data
    )
    if sorted_archived_sent_emails:
        emails_container = chain(
            sorted_sent_emails, sorted_archived_sent_emails
        )
    else:
        emails_container = sorted_sent_emails

    for index, contact in extract_contacts(emails_container):
        yield index

        if contact.email not in accumulator \
                and not is_email_address_domain_excluded(
                    contact.email, domain_list
                ):
            accumulator[contact.email] = contact
    create_xlsx_file(username, accumulator.values(), path)
