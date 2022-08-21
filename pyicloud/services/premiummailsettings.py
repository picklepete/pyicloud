"""Premium Mail Settings service"""

import typing as t
from enum import Enum


class HmeEmailOrigin(Enum):
    """Hme Email generation origin"""

    SAFARI = "SAFARI"
    ON_DEMAND = "ON_DEMAND"


class HmeEmail(t.NamedTuple):
    """HME Email model"""

    origin: HmeEmailOrigin
    anonymous_id: str
    domain: str
    hme: str
    label: str
    note: str
    create_timestamp: int
    is_active: bool
    recipient_mail_id: str
    forward_to_email: t.Optional[str]

    @classmethod
    def deserialize(cls, data: t.Mapping[str, str]) -> "HmeEmail":
        """Converts dict data into a well defined type"""
        return cls(
            origin=HmeEmailOrigin(data["origin"]),
            anonymous_id=data["anonymousId"],
            domain=data["domain"],
            forward_to_email=data.get("forwardToEmail"),
            hme=data["hme"],
            label=data["label"],
            note=data["note"],
            create_timestamp=data["createTimestamp"],
            is_active=data["isActive"],
            recipient_mail_id=data["recipientMailId"],
        )


class PremiumMailSettings:
    """The 'Premium Mail Settings' iCloud service
    https://support.apple.com/en-us/HT210425 
    """
    def __init__(self, service_root, session):
        self._service_root = service_root
        self.session = session
        self.service_endpoint = self._service_root + "/v1"

    @property
    def hme_emails(self) -> t.Sequence[HmeEmail]:
        """Lists all the HME emails that have been reserved"""

        resp = self.session.get(f"{self.service_endpoint}/hme/list")
        return [
            HmeEmail.deserialize(data) for data in resp.json()["result"]["hmeEmails"]
        ]

    def generate_hme(self) -> str:
        """Generates a new HME"""
        resp = self.session.post(f"{self.service_endpoint}/hme/generate")
        return resp.json()["result"]["hme"]

    def reserve_hme(
        self, hme: str, label: str, note: t.Optional[str] = "Generated from pyiCloud"
    ) -> HmeEmail:
        """Resnerves/activates a newly generated HME"""
        resp = self.session.post(
            f"{self.service_endpoint}/hme/reserve",
            json={
                "hme": hme,
                "label": label,
                "note": note,
            },
        )

        return HmeEmail.deserialize(resp.json()["result"]["hme"])
