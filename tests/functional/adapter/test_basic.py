import pytest

from dbt.tests.adapter.basic.test_base import BaseSimpleMaterializations
from dbt.tests.adapter.basic.test_singular_tests import BaseSingularTests
from dbt.tests.adapter.basic.test_singular_tests_ephemeral import (
    BaseSingularTestsEphemeral
)
from dbt.tests.adapter.basic.test_empty import BaseEmpty
from dbt.tests.adapter.basic.test_ephemeral import BaseEphemeral
from dbt.tests.adapter.basic.test_incremental import BaseIncremental
from dbt.tests.adapter.basic.test_generic_tests import BaseGenericTests
from dbt.tests.adapter.basic.test_snapshot_check_cols import BaseSnapshotCheckCols
from dbt.tests.adapter.basic.test_snapshot_timestamp import BaseSnapshotTimestamp
from dbt.tests.adapter.basic.test_adapter_methods import BaseAdapterMethod


class TestSimpleMaterializationsksqlDB(BaseSimpleMaterializations):
    pass


class TestSingularTestsksqlDB(BaseSingularTests):
    pass


class TestSingularTestsEphemeralksqlDB(BaseSingularTestsEphemeral):
    pass


class TestEmptyksqlDB(BaseEmpty):
    pass


class TestEphemeralksqlDB(BaseEphemeral):
    pass


class TestIncrementalksqlDB(BaseIncremental):
    pass


class TestGenericTestsksqlDB(BaseGenericTests):
    pass


class TestSnapshotCheckColsksqlDB(BaseSnapshotCheckCols):
    pass


class TestSnapshotTimestampksqlDB(BaseSnapshotTimestamp):
    pass


class TestBaseAdapterMethodksqlDB(BaseAdapterMethod):
    pass
