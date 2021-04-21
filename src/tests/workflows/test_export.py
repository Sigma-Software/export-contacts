from datetime import datetime

from domain.entities import Contact
from workflows.export import (
    connect_to_sent_items,
    export,
    get_all_emails_amount,
    is_email_address_valid
)


class TestExport:
    def test_connect_to_sent_items(self, mocker):
        mocked_connect_to_ews = mocker.patch('workflows.export.connect_to_ews', return_value=True)
        mocked_retrieve_sent_items = mocker.patch('workflows.export.retrieve_sent_items', return_value=True)
        connect_to_sent_items('test_username', 'test_password', 'test_email@example.com', 'test_email_service_address')
        mocked_connect_to_ews.assert_called_with(
            'test_username',
            'test_password',
            'test_email@example.com',
            'test_email_service_address'
        )
        mocked_retrieve_sent_items.assert_called_with(mocked_connect_to_ews.return_value)

    def test_is_email_address_valid(self):
        valid_email_addresses = [
            'simple@example.com',
            'very.common@example.com',
            'disposable.style.email.with+symbol@example.com',
            'other.email-with-hyphen@example.com',
            'fully-qualified-domain@example.com',
            'user.name+tag+sorting@example.com',
            'x@example.com',
            'example-indeed@strange-example.com',
            'admin@mailserver1',
            'example@s.example',
            '" "@example.org',
            '"john..doe"@example.org',
            'mailhost!username@example.org',
            'user%example.com@example.org',
            'user-@example.org'
        ]
        invalid_email_addresses = [
            'Abc.example.com',
            'A@b@c@example.com',
            'a"b(c)d,e:f;g<h>i[j\\k]l@example.com',
            'just"not"right@example.com',
            'this is "not\\allowed@example.com',
            'this\\ still\\"not\\allowed@example.com',
            '1234567890123456789012345678901234567890123456789012345678901234+x@example.com',
            'i_like_underscore@but_its_not_allowed_in_this_part.example.com',
            'test/test@test.com',
            'QA[icon]CHOCOLATE[icon]@test.com'
        ]
        for email_address in valid_email_addresses:
            assert is_email_address_valid(email_address)

        for email_address in invalid_email_addresses:
            assert not is_email_address_valid(email_address)

    def test_get_all_emails_amount(self, mocker):
        mocked_sort_all_emails = mocker.patch('workflows.export.sort_all_emails', return_value=(True, True))
        mocked_count_sent_emails = mocker.patch('workflows.export.count_sent_emails', return_value=True)
        get_all_emails_amount((True, True))
        mocked_sort_all_emails.assert_called_with((True, True))
        mocked_count_sent_emails.assert_called_with(True, True)

    def test_export(self, mocker):
        username = 'test_username'
        path = '/path/'
        test_contacts = [
            (1, Contact(name='test1', email='test_1@example.com', subject='test1', date=datetime.today())),
            (2, Contact(name='test2', email='test_2@example.com', subject='test2', date=datetime.today())),
            (3, Contact(name='test3', email='test_3@example.com', subject='test3', date=datetime.today())),
        ]
        mocked_sort_all_emails = mocker.patch('workflows.export.sort_all_emails', return_value=(True, True))
        mocked_extract_contacts = mocker.patch('workflows.export.extract_contacts', return_value=test_contacts)

        mocked_create_xlsx_file = mocker.patch('workflows.export.create_xlsx_file', return_value=True)
        for expected_index, actual_index in enumerate(export(True, username, [], path), start=1):
            assert expected_index == actual_index

        mocked_sort_all_emails.assert_called_with(connection_data=True)
        mocked_extract_contacts.has_calls()
        mocked_create_xlsx_file.assert_called_with(username, mocker.ANY, path)
