*terraform-provider-freebox* is a `Terraform <https://www.terraform.io/>`_ (0.12)
`provider <https://www.terraform.io/docs/glossary.html#terraform-provider>`_
for configuring `Freeboxes <https://en.wikipedia.org/wiki/Freebox>`_
(the xDSL/FTTH modems provided by the French ISP `Free <https://free.fr>`_).

This modem provides a `configuration GUI <http://mafreebox.freebox.fr/>`_ for NAT configuration, port forwarding, static DHCP leases, etc.
and a `configuration API <https://dev.freebox.fr/sdk/os/#>`_ with the same capabilities. (The GUI uses the API).

This provider uses the same API to let you configure your Freebox using Terraform's `IaC <https://en.wikipedia.org/wiki/Infrastructure_as_code>`_ approach.


It's licensed under the `MIT license <http://choosealicense.com/licenses/mit/>`_.
It's available on the `Python package index <http://pypi.python.org/pypi/terraform-provider-freebox>`_.
Its `documentation and source code <https://github.com/jacquev6/terraform-provider-freebox>`_ are on GitHub.

Questions? Remarks? Bugs? Want to contribute? `Open an issue <https://github.com/jacquev6/terraform-provider-freebox/issues>`_!

.. image:: https://img.shields.io/github/workflow/status/jacquev6/terraform-provider-freebox/Continuous%20Integration?label=CI&logo=github
    :target: https://github.com/jacquev6/terraform-provider-freebox/actions?query=workflow%3A%22Continuous+Integration%22

.. image:: https://img.shields.io/pypi/v/terraform-provider-freebox?logo=pypi
    :alt: PyPI
    :target: https://pypi.org/project/terraform-provider-freebox/

.. image:: https://img.shields.io/pypi/pyversions/terraform-provider-freebox?logo=pypi
    :alt: PyPI
    :target: https://pypi.org/project/terraform-provider-freebox/


Quick start
===========

Installation
------------

Install from PyPI::

    $ pip install terraform-provider-freebox

Configuration
-------------

The configuration API provided by the Freebox uses a *token* for authentication.

You first need to obtain a token (you'll have to do that only once).
Run the following command and follow its instructions.
You'll have to click on your Freebox' touch display.

::

    $ terraform-provider-freebox create-token

After creating the token, it will give you a `provider` section to copy-paste in your Terraform
configuration files. It should look like::

    provider freebox {
        app_id = "terraform"
        app_token = "9m2KFLflttfuk1h52aiQvna@LWwk%02qPN4Ah3euZpT7YjP!lekb1MmfWR9qL50r"
        ...
    }

You are responsible for keeping this token safe.
If you lose it, you'll have to create a new one.

You are responsible for keeping this token secret.
Ill-intentioned people might use it to hack your network and devices.

Permissions setup
-----------------

@todo Motivate why permissions have to be added manually.
@todo Describe how to add permissions.
@todo List what permissions must be added for each datasource and resource.
