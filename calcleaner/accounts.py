from gi.repository import Secret

from . import APPLICATION_ID


_SECRET_SCHEMA = Secret.Schema.new(
    APPLICATION_ID,
    Secret.SchemaFlags.NONE,
    {
        "account_name": Secret.SchemaAttributeType.STRING,
        "url": Secret.SchemaAttributeType.STRING,
        "username": Secret.SchemaAttributeType.STRING,
    },
)


class Accounts(object):
    """Manage accounts."""

    def __init__(self):
        self._accounts = {}

    def load(self):
        secrets = Secret.password_search_sync(
            _SECRET_SCHEMA,
            {},
            Secret.SearchFlags.ALL,
            None,
        )
        for secret in secrets:
            attr = secret.get_attributes()
            self._accounts[attr["account_name"]] = {
                "url": attr["url"],
                "username": attr["username"],
                "password": secret.retrieve_secret_sync().get_text(),
            }

    def add(self, account_name, url="", username="", password=""):
        if not account_name or not url or not username or not password:
            raise ValueError()

        self._accounts[account_name] = {
            "url": url,
            "username": username,
            "password": password,
        }
        Secret.password_store_sync(
            _SECRET_SCHEMA,
            {
                "account_name": account_name,
                "url": url,
                "username": username,
            },
            Secret.COLLECTION_DEFAULT,
            "Calcleaner: password for %s" % account_name,
            password,
            None,
        )

    def remove(self, account_name):
        del self._accounts[account_name]

        Secret.password_clear_sync(
            _SECRET_SCHEMA,
            {"account_name": account_name},
            None,
        )

    def get(self, account_name):
        return self._accounts[account_name]

    def update(self, account_name, **kwargs):
        account = self.get(account_name)
        account.update(kwargs)
        self.remove(account_name)
        self.add(account_name, **account)

    def list(self):
        return self._accounts.keys()
