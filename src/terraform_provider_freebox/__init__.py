import Pyrraform


class ConnectionStatusDataSource(Pyrraform.DataSource):
    config_schema = Pyrraform.Schema(
        version=0,
        block=Pyrraform.schema.Block(
            version=0,
            attributes=[
                Pyrraform.schema.Attribute(
                    name="ip",
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
        return {
            "ip": "aa.bb.cc.dd",
        }


class FreeboxProvider(Pyrraform.Provider):
    data_source_classes = {
        "connection_status": ConnectionStatusDataSource,
    }


def main():
    Pyrraform.run_provider(FreeboxProvider)
