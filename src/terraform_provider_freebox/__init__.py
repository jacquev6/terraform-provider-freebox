import os
import hmac
import json
import logging
import contextlib

import requests
import Pyrraform


log = logging.getLogger(__name__)


class Freebox(contextlib.AbstractContextManager):
    # https://dev.freebox.fr/sdk/os/ documents API v4, even though FreeboxOS uses v8.
    # We stick to v4 to avoid having to reverse-engineer the API for the moment.
    base_url = "http://192.168.1.254/api/v4"

    def __init__(self, *, app_id, app_token, requestor=requests):
        self.__requestor = requestor
        # We don't handle session token invalidation because Terraform providers are short-lived.
        # If this class is used in a more general context, __request should detect when
        # session token is refused and call __login again.
        self.__login(app_id, app_token)

    def __login(self, app_id, app_token):
        self.__headers = {}
        challenge = self.__request("get", "login")["challenge"]
        data = {
            "app_id": app_id,
            "password": hmac.new(
                app_token.encode(),
                challenge.encode(),
                "sha1",
            ).hexdigest(),
        }
        session_token = self.__request("post", "login/session/", data)["session_token"]
        self.__headers = {"X-Fbx-App-Auth": session_token}

    def __exit__(self, exc_type, exc_value, traceback):
        self.__request("post", "login/logout/")

    def get(self, path):
        return self.__request("get", path)

    def put(self, path, data):
        return self.__request("put", path, data)

    def post(self, path, data):
        return self.__request("post", path, data)

    def delete(self, path):
        return self.__request("delete", path)

    def __request(self, method, path, data=None):
        if data is None:
            data = dict()
        else:
            data = dict(data=json.dumps(data))
        r = getattr(self.__requestor, method)(
            f"{self.base_url}/{path}",
            **data,
            headers=self.__headers,
        ).json()
        assert r["success"], r
        return r.get("result")


class ConnectionStatusDataSource(Pyrraform.DataSource):
    config_schema = Pyrraform.Schema(
        version=0,
        block=Pyrraform.schema.Block(
            version=0,
            attributes=[
                Pyrraform.schema.Attribute(
                    name="ipv4",
                    type=Pyrraform.String,
                    description="",
                    required=False,
                    optional=False,
                    computed=True,
                    sensitive=False,
                ),
            ],
            block_types=[],
        )
    )

    def read(self):
        # @todo Do not create a Freebox instance for each interaction
        # (Create a single Freebox instance in FreeboxProvider.__init__)
        # (We still have to logout from the Freebox to avoid leaking sessions, so this
        # requires a way in Pyrraform to free resources allocated by the provider)
        with Freebox(app_id="infrastructure", app_token=self.provider.config["token"]) as freebox:
            return dict(ipv4=freebox.get("connection/")["ipv4"])


class FreeboxProvider(Pyrraform.Provider):
    config_schema = Pyrraform.Schema(
        version=0,
        block=Pyrraform.schema.Block(
            version=0,
            attributes=[
                Pyrraform.schema.Attribute(
                    name="token",
                    type=Pyrraform.String,
                    description="",
                    required=True,
                    optional=False,
                    computed=False,
                    sensitive=True,
                ),
            ],
            block_types=[],
        )
    )

    data_source_classes = {
        "connection_status": ConnectionStatusDataSource,
    }


def main():
    if "DEBUG_TERRAFORM_PROVIDER_FREEBOX" in os.environ:
        logging.basicConfig(filename="terraform-provider-freebox.log", level=logging.DEBUG)
    log.info("Entering main")
    Pyrraform.run_provider(FreeboxProvider)
