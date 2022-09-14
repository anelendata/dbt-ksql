#!/usr/bin/env python
from setuptools import find_namespace_packages, setup

package_name = "dbt-ksql"
# make sure this always matches dbt/adapters/{adapter}/__version__.py
package_version = "1.1.0"
description = """The ksqlDB adapter plugin for dbt"""

setup(
    name=package_name,
    version=package_version,
    description=description,
    long_description=description,
    author="Anelen Co., LLC",
    author_email="daigo@anelen.co",
    url="https://github.com/anelendata/dbt-ksql",
    packages=find_namespace_packages(include=["dbt", "dbt.*"]),
    include_package_data=True,
    install_requires=[
        "dbt-core~=1.1.0",
        "ksql>=0.10.0",
    ],
)
