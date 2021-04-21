import keyring
import sys

from getpass import getuser


# This is required for PyInstaller to correctly bundle the keyring backends
if hasattr(sys, 'frozen'):
    if sys.platform.startswith('win'):
        from keyrings.alt import Windows
        keyring.set_keyring(Windows.RegistryKeyring())
    elif sys.platform.startswith('darwin'):
        import keyring.backends.OS_X
        keyring.set_keyring(keyring.backends.OS_X.Keyring())


SERVICE_NAME = 'ExportContacts'
SYSTEM_USERNAME = getuser()


def get_email_service_address():
    return keyring.get_password(
        SERVICE_NAME + '_email_service_address',
        SYSTEM_USERNAME
    )


def get_username():
    return keyring.get_password(
        SERVICE_NAME + '_username',
        SYSTEM_USERNAME
    )


def get_email():
    return keyring.get_password(
        SERVICE_NAME + '_email',
        SYSTEM_USERNAME
    )


def get_password():
    return keyring.get_password(
        SERVICE_NAME + '_password',
        SYSTEM_USERNAME
    )


def set_credentials(email_service_address, username, email, password):
    keyring.set_password(
        SERVICE_NAME + '_email_service_address',
        SYSTEM_USERNAME,
        email_service_address
    )
    keyring.set_password(
        SERVICE_NAME + "_username",
        SYSTEM_USERNAME,
        username
    )
    keyring.set_password(
        SERVICE_NAME + "_email",
        SYSTEM_USERNAME,
        email
    )
    keyring.set_password(
        SERVICE_NAME + "_password",
        SYSTEM_USERNAME,
        password
    )
