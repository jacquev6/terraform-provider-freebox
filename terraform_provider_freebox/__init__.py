import textwrap
import urllib.parse
import socket
import time
import sys
import os
import hmac
import json
import logging
import contextlib
import argparse

import requests
import Pyrraform


log = logging.getLogger(__name__)


class Freebox(contextlib.AbstractContextManager):
    # https://dev.freebox.fr/sdk/os/ documents API v4, even though FreeboxOS uses v8.
    # We stick to v4 to avoid having to reverse-engineer the API for the moment.
    DEFAULT_API_BASE_URL = "http://mafreebox.freebox.fr/api/v4"

    @staticmethod
    def create_app_token(*, api_base_url, app_id, app_name, app_version, device_name, requestor=requests):
        # https://dev.freebox.fr/sdk/os/login/#
        r = requestor.post(
            f"{api_base_url}/login/authorize/",
            data=json.dumps({
                "app_id": app_id,
                "app_name": app_name,
                "app_version": app_version,
                "device_name": device_name,
            }),
        ).json()
        assert r["success"], r
        app_token = r["result"]["app_token"]
        track_id = r["result"]["track_id"]
        status = "pending"
        while status == "pending":
            time.sleep(1)
            r = requestor.get(f"{api_base_url}/login/authorize/{track_id}").json()
            assert r["success"], r
            status = r["result"]["status"]
        assert status == "granted", f"Access refused or not granted in time ({status})"
        return app_token

    def __init__(self, *, api_base_url=DEFAULT_API_BASE_URL, app_id, app_token, requestor=requests):
        self.__api_base_url = api_base_url
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
            f"{self.__api_base_url}/{path}",
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
                # https://dev.freebox.fr/sdk/os/connection/#ConnectionStatus
                Pyrraform.schema.Attribute(
                    name="state",
                    type=Pyrraform.String,
                    description="",
                    required=False,
                    optional=False,
                    computed=True,
                    sensitive=False,
                ),
                Pyrraform.schema.Attribute(
                    name="type",
                    type=Pyrraform.String,
                    description="",
                    required=False,
                    optional=False,
                    computed=True,
                    sensitive=False,
                ),
                Pyrraform.schema.Attribute(
                    name="media",
                    type=Pyrraform.String,
                    description="",
                    required=False,
                    optional=False,
                    computed=True,
                    sensitive=False,
                ),
                Pyrraform.schema.Attribute(
                    name="ipv4",
                    type=Pyrraform.String,
                    description="",
                    required=False,
                    optional=False,
                    computed=True,
                    sensitive=False,
                ),

                Pyrraform.schema.Attribute(
                    name="ipv6",
                    type=Pyrraform.String,
                    description="",
                    required=False,
                    optional=False,
                    computed=True,
                    sensitive=False,
                ),
                Pyrraform.schema.Attribute(
                    name="rate_up",
                    type=Pyrraform.Number,
                    description="",
                    required=False,
                    optional=False,
                    computed=True,
                    sensitive=False,
                ),
                Pyrraform.schema.Attribute(
                    name="rate_down",
                    type=Pyrraform.Number,
                    description="",
                    required=False,
                    optional=False,
                    computed=True,
                    sensitive=False,
                ),
                Pyrraform.schema.Attribute(
                    name="bandwidth_up",
                    type=Pyrraform.Number,
                    description="",
                    required=False,
                    optional=False,
                    computed=True,
                    sensitive=False,
                ),
                Pyrraform.schema.Attribute(
                    name="bandwidth_down",
                    type=Pyrraform.Number,
                    description="",
                    required=False,
                    optional=False,
                    computed=True,
                    sensitive=False,
                ),
                Pyrraform.schema.Attribute(
                    name="bytes_up",
                    type=Pyrraform.Number,
                    description="",
                    required=False,
                    optional=False,
                    computed=True,
                    sensitive=False,
                ),
                Pyrraform.schema.Attribute(
                    name="bytes_down",
                    type=Pyrraform.Number,
                    description="",
                    required=False,
                    optional=False,
                    computed=True,
                    sensitive=False,
                ),
                Pyrraform.schema.Attribute(
                    name="ipv4_port_range",
                    type=Pyrraform.List(Pyrraform.Number),
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
        with Freebox(
                app_id=self.provider.config["app_id"],
                app_token=self.provider.config["app_token"],
        ) as freebox:
            data = freebox.get("connection/")
            return dict(
                state=data["state"],
                type=data["type"],
                media=data["media"],
                ipv4=data["ipv4"],
                ipv6=data["ipv6"],
                rate_up=data["rate_up"],
                rate_down=data["rate_down"],
                bandwidth_up=data["bandwidth_up"],
                bandwidth_down=data["bandwidth_down"],
                bytes_up=data["bytes_up"],
                bytes_down=data["bytes_down"],
                ipv4_port_range=data["ipv4_port_range"],
            )


class FreeboxProvider(Pyrraform.Provider):
    config_schema = Pyrraform.Schema(
        version=0,
        block=Pyrraform.schema.Block(
            version=0,
            attributes=[
                Pyrraform.schema.Attribute(
                    name="app_id",
                    type=Pyrraform.String,
                    description="",
                    required=True,
                    optional=False,
                    computed=False,
                    sensitive=False,
                ),
                Pyrraform.schema.Attribute(
                    name="app_token",
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

    if len(sys.argv) > 1 and sys.argv[1] == "create-token":
        parser = argparse.ArgumentParser(
            prog=f"{os.path.basename(sys.argv[0])} {sys.argv[1]}",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

        api_location = parser.add_argument_group(
            title="API location",
        )
        api_location.add_argument(
            "--api-base-url",
            default=Freebox.DEFAULT_API_BASE_URL,
            help=f"The base URL for the Freebox API. In the exact same format as the following default",
        )

        app_definition = parser.add_argument_group(
            title="Application definition",
            description=textwrap.dedent("""\
                The token is associated to an "application" visible in FreeboxOS
                ("Paramètres de la Freebox", "Gestion des accès", "Applications").
                The following options allow you to specify that application
                as described in https://dev.freebox.fr/sdk/os/login.
            """)
        )
        app_definition.add_argument(
            "--app-id",
            default="terraform",
            help="The application ID, used to identify the application",
        )
        app_definition.add_argument(
            "--app-name",
            default="Terraform",
            help="The application name, displayed in FreeboxOS",
        )
        app_definition.add_argument(
            "--app-version",
            default="1.0",
            help="The application version",
        )
        app_definition.add_argument(
            "--device-name",
            default=socket.gethostname(),
            help="The devide name, displayed in FreeboxOS",
        )
        args = parser.parse_args(sys.argv[2:])
        print("Registering aplication and token. Please confirm on your Freebox' touch display...", flush=True, end=" ")
        app_token = Freebox.create_app_token(
            api_base_url=args.api_base_url,
            app_id=args.app_id,
            app_name=args.app_name,
            app_version=args.app_version,
            device_name=args.device_name,
        )
        print("OK")
        print()
        print("Final manual steps:")
        print()
        print("1. Grant required permissions to the newly created application in FreeboxOS")
        freebox_os_url = urllib.parse.urlunparse(
            urllib.parse.urlparse(args.api_base_url)._replace(path="/")
        )
        print(f'({freebox_os_url}, "Paramètres de la Freebox", "Gestion des accès", "Applications")')
        print("See https://github.com/jacquev6/terraform-provider-freebox#permissions for details")
        print()
        print("2. Copy-paste the following block in your Terraform configuration. Keep the token secret:")
        print()
        print("provider freebox {")
        print(f'  app_id = "{args.app_id}"')
        print(f'  app_token = "{app_token}"')
        print("}")
    else:
        Pyrraform.run_provider(FreeboxProvider)
