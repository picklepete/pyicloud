"""Hide my email service."""


import json


class HideMyEmailService:
    """
    The 'Hide My Email' iCloud service, connects to iCloud and create alias emails.
    """

    def __init__(self, service_root, session, params):
        self.session = session
        self.params = params
        self._service_root = service_root
        hme_endpoint = "%s/v1/hme" % service_root
        self._hidemyemail_generate = "%s/generate" % hme_endpoint
        self._hidemyemail_reserve = "%s/reserve" % hme_endpoint

        self.response = {}

    def generate(self):
        """
        Generate alias for the emails
        """
        req = self.session.post(self._hidemyemail_generate, params=self.params)
        self.response = req.json()
        return self.response.get("result").get("hme")


    def reserve(self, email, label, note="Generated"):
        """
        Reserve alias for the emails
        """
        data = json.dumps(
            {
                "hme": email,
                "label": label,
                "note": note
            }
        )
 
        self.session.post(self._hidemyemail_reserve, params=self.params, data=data)

