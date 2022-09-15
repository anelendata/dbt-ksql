# dbt-ksql

A dbt adapter for ksqlDB

Like in many database projects, managing models becomes increasingly challenging.
dbt-ksql helps to modularize the code, manage the model dependency, and facilitate the model deployment.

## Concepts

This project is in a proof-of-concept phase.

We are trying to use dbt to manage ksqlDB by
- Separating production/staging/development environments through dbt's profile and target.
- Modularize the SQL with dbt's variable, reference, macro, etc.

### Materialization type

Supported:
- stream
- table

Not-suported:
- ephemeral
- incremental

## Example project

See [example](./example) folder for a dbt project.
It has examples for creating stream, stream as, table.
It also has a example of using macros.

## Pre-release warning

- This project is an experimental phase.
- This has not been published to pypi.

## Pre-release install steps

To install, fetch this repository and run a local install:

```
git clone git@github.com:anelendata/dbt-ksql.git
cd dbt-ksql
python -m venv venv
source venv/bin/activate
pip install -U pip
pip install -e .
```

After the successful instsall, the following command will show
```
dbt --version
```

Something like this:
``
Core:
  - installed: 1.1.2
  - latest:    1.2.1 - Update available!

  Your version of dbt-core is out of date!
  You can find instructions for upgrading here:
  https://docs.getdbt.com/docs/installation

  Plugins:
  - ksqldb: 1.1.0 - Could not determine latest version
```

## Example commands

After set up profiles.yml try running the following commands:
- compile: `dbt compile --profiles-dir . --profile prod`
- run: `dbt run --profiles-dir . --profile prod`

## Helper macro

- drop stream: `dbt run-operation drop_stream --args "{relation: some_stream, delete_topic: true}" --profiles-dir . --profile dev`
 
## About dbt

**[dbt](https://www.getdbt.com/)** enables data analysts and engineers to transform their data using the same practices that software engineers use to build applications.

dbt is the T in ELT. Organize, cleanse, denormalize, filter, rename, and pre-aggregate the raw data in your warehouse so that it's ready for analysis.

# About this project

This project is developed by 
ANELEN and friends. Please check out the ANELEN's
[open innovation philosophy and other projects](https://anelen.co/open-source.html)

![ANELEN](https://avatars.githubusercontent.com/u/13533307?s=400&u=a0d24a7330d55ce6db695c5572faf8f490c63898&v=4)
---

Copyright &copy; 2020~ Anelen Co., LLC
