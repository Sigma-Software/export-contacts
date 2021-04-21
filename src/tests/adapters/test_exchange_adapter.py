import datetime

import pytest
from exchangelib import Account, Folder, Mailbox, Message
from exchangelib.errors import UnauthorizedError
from exchangelib.queryset import QuerySet

from adapters.exchange_adapter import (
    connect_to_ews,
    count_sent_emails,
    extract_contacts,
    get_all_recipients,
    is_email_address_domain_excluded,
    retrieve_sent_items,
    sort_all_emails,
    sort_sent_emails
)
from domain.entities import Contact, ExportContactException


class TestExchangeAdapter:
    def test_is_email_address_domain_excluded(self):
        test_domains_list = ['test.com', 'example.org', 'mail.net']
        test_correct_email = 'export.contacts@test.com'
        assert is_email_address_domain_excluded(test_correct_email, test_domains_list)
        test_incorrect_email = 'export.contacts@instance.io'
        assert not is_email_address_domain_excluded(test_incorrect_email, test_domains_list)

    def test_sort_sent_emails(self):
        assert isinstance(sort_sent_emails(Folder()), QuerySet)

    def test_get_all_recipients(self):
        email = Message()
        assert get_all_recipients(email) == []
        email = Message(
            to_recipients=['recipient1@example.com'],
            cc_recipients=[],
            bcc_recipients=[]
        )
        assert len(get_all_recipients(email)) == 1
        email = Message(
            to_recipients=['recipient1@example.com'],
            cc_recipients=['cc_recipient1@example.com'],
            bcc_recipients=[]
        )
        assert len(get_all_recipients(email)) == 2
        email = Message(
            to_recipients=['recipient1@example.com'],
            cc_recipients=['cc_recipient1@example.com'],
            bcc_recipients=['bcc_recipient1@example.com']
        )
        assert len(get_all_recipients(email)) == 3

    def test_connect_to_ews(self, mocker):
        with pytest.raises(ExportContactException) as exception:
            connect_to_ews('test_username', 'test_password', 'test_email@example.com', 'test_email_service_address')
        assert 'User does not exist or does not have access to the specified email.' == str(exception.value)
        mocked_account = Account
        mocked_account.root.refresh = lambda: True
        mocker.patch('adapters.exchange_adapter.Account', return_value=mocked_account)
        connect_to_ews('test_username', 'test_password', 'test_email@example.com', 'test_email_service_address')

        def raise_unauthorized_exception():
            raise UnauthorizedError('Error')

        mocked_account.root.refresh = raise_unauthorized_exception
        mocker.patch('adapters.exchange_adapter.Account', return_value=mocked_account)
        with pytest.raises(ExportContactException) as exception:
            connect_to_ews('test_username', 'test_password', 'test_email@example.com', 'test_email_service_address')
        assert 'Password and username do not match.' == str(exception.value)

    def test_count_sent_emails(self):
        sent_emails = QuerySet
        sent_emails.count = lambda: 3
        archived_sent_emails = QuerySet
        archived_sent_emails.count = lambda: 3
        assert 3 == count_sent_emails(sent_emails, None)
        assert 6 == count_sent_emails(sent_emails, archived_sent_emails)

    def test_extract_contacts(self, mocker):
        emails = [Message(subject='test', datetime_sent=datetime.date.today())]
        mocker.patch('adapters.exchange_adapter.get_all_recipients', return_value=[
            Mailbox(email_address='simple@example.com', name='test 1'),
            Mailbox(email_address='very.common@example.com', name='test 2'),
            Mailbox(email_address='too.common@example.com', name='test 3')
        ])

        for contact_index, contact in extract_contacts(None):
            assert isinstance(contact_index, int)
            assert isinstance(contact, Contact)
            assert contact.subject == emails[contact_index].subject
            assert contact.date == emails[contact_index].datetime_sent

    def test_sort_all_emails(self, mocker):
        mocker.patch('adapters.exchange_adapter.sort_sent_emails', return_value=True)
        assert (True, True) == sort_all_emails((True, True))
        assert (True, None) == sort_all_emails((True, None))
        mocker.patch('adapters.exchange_adapter.sort_sent_emails', return_value=False)
        assert (False, None) == sort_all_emails((None, None))
