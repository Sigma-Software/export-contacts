from dataclasses import dataclass

from exchangelib import EWSDateTime


class ExportContactException(Exception):
    def __init__(self, *args):
        super(ExportContactException, self).__init__(*args)
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return self.message
        return 'ExportContactException has been raised'


@dataclass(frozen=True)
class Contact:
    """A dataclass for capturing the contact"""

    email: str
    name: str
    subject: str
    date: EWSDateTime
