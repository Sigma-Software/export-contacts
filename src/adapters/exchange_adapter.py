from typing import Tuple, Iterable

from exchangelib import (
    Account,
    Configuration,
    Credentials,
    DELEGATE,
    Folder,
    Mailbox,
    Message,
    NTLM,
    Q
)
from exchangelib.errors import (
    ErrorFolderNotFound,
    ErrorItemNotFound,
    ErrorNonExistentMailbox,
    UnauthorizedError
)
from exchangelib.queryset import QuerySet
from requests.exceptions import ConnectionError

from domain.entities import ExportContactException, Contact
from utils.logger import LOGGER


def is_email_address_domain_excluded(email_address: str, excluded_domains: list) -> bool:
    """Determines if the recipient's email is an email that should be excluded"""

    return any(email_address.endswith(i) for i in excluded_domains)


def sort_sent_emails(emails: Folder) -> QuerySet:
    """Sorts folder with sent emails"""

    # We want only emails (but not meeting request responses, for example)
    query: Q = Q(item_class__iexact='IPM.Note')

    sorted_sent_emails = emails.filter(query).only(
        'subject',
        'to_recipients',
        'cc_recipients',
        'bcc_recipients',
        'datetime_sent'
    ).order_by('-datetime_sent')

    return sorted_sent_emails


def get_all_recipients(email: Message) -> list:
    """Retrieves and join all the recipients of email into list"""
    recipients = []
    if email.to_recipients:
        recipients.extend(email.to_recipients)
    if email.cc_recipients:
        recipients.extend(email.cc_recipients)
    if email.bcc_recipients:
        recipients.extend(email.bcc_recipients)

    return recipients


def connect_to_ews(
        username: str, pwd: str, primary_email: str, email_service_address: str
) -> Account:
    """
    Connects to EWS and returns Account object
    """

    LOGGER.info('Connecting to EWS')
    if not pwd:
        LOGGER.info('Password is empty')
        raise ExportContactException('Password is empty')

    credentials: Credentials = Credentials(username, pwd)
    config: Configuration = Configuration(
        server=email_service_address,
        credentials=credentials,
        auth_type=NTLM
    )

    try:
        account: Account = Account(
            primary_smtp_address=primary_email,
            autodiscover=False,
            config=config,
            access_type=DELEGATE
        )
        account.root.refresh()
        return account
    except UnauthorizedError as ex:
        LOGGER.error(
            f'Password and username do not match. Full error text: {str(ex)}'
        )
        raise ExportContactException('Password and username do not match.')
    except (ConnectionError, ErrorNonExistentMailbox) as ex:
        error_text = 'User does not exist or does not have access to the specified email.'
        LOGGER.error(f'{error_text} Full error text: {str(ex)}')
        raise ExportContactException(error_text)


def retrieve_sent_items(account: Account) -> Tuple[Folder, Folder]:
    """
    Retrieves a tuple containing references to Sent Items
    and archived Sent Items
    """
    try:
        account.archive_root.refresh()
        archive: Folder = account.archive_msg_folder_root
    except ErrorFolderNotFound:
        archive_sent = None
    else:
        try:
            archive_sent = archive / 'Sent Items'
            LOGGER.info('Online archiving is enabled')
        except ErrorFolderNotFound:
            archive_sent = None
            LOGGER.info('Online archiving is disabled')

    try:
        LOGGER.info('Connected.')
        return account.sent, archive_sent
    except ErrorItemNotFound as ex:
        error_text = 'User does not exist or does not have access to the specified email.'
        LOGGER.error(f'{error_text} Full error text: {str(ex)}')
        raise ExportContactException(error_text)


def count_sent_emails(sent_emails: QuerySet, archived_sent_emails: QuerySet) -> int:
    if archived_sent_emails:
        return sent_emails.count() + archived_sent_emails.count()
    else:
        return sent_emails.count()


def extract_contacts(emails: Iterable):
    """Walk through a collection of emails and yields a Contact object for each email"""

    if not emails:
        return

    for email_index, email in enumerate(emails):
        all_recipients: list = get_all_recipients(email)
        recipient: Mailbox
        for recipient in all_recipients:
            yield (email_index, Contact(
                    name=recipient.name,
                    email=recipient.email_address,
                    subject=email.subject,
                    date=email.datetime_sent
                ))


def sort_all_emails(connection_data: tuple) -> tuple:
    """Sorts and joins sent emails and archive emails"""

    sent_emails, archived_sent_emails = connection_data

    sorted_sent_emails: QuerySet = sort_sent_emails(sent_emails)

    # Sent items in the online archive are always older than the
    # sent items in the main mailbox. Therefore, we process them last, reusing
    # the already populated dictionary from the main 'Sent Items' folder.

    if archived_sent_emails:
        sorted_archived_sent_emails = sort_sent_emails(archived_sent_emails)
    else:
        sorted_archived_sent_emails = None
    return sorted_sent_emails, sorted_archived_sent_emails
