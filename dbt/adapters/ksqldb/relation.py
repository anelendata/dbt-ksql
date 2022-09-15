from dataclasses import dataclass
from typing import Optional, Type

from itertools import chain, islice

from dbt.adapters.base.relation import BaseRelation, ComponentName, InformationSchema
from dbt.dataclass_schema import StrEnum
from dbt.exceptions import raise_compiler_error
from dbt.utils import classproperty, filter_null_values
from typing import TypeVar


Self = TypeVar("Self", bound="ksqlDBRelation")


class ksqlDBRelationType(StrEnum):
    # Built-in materialization types.
    Table = "table"
    View = "view"
    CTE = "cte"
    External = "external"

    # ksqldb-specific materialization types.
    # Source = "source"
    Stream = "stream"


@dataclass(frozen=True, eq=False, repr=False)
class ksqlDBRelation(BaseRelation):
    quote_character: str = ""
    location: Optional[str] = None
    ns_delimit: Optional[str] = "_"

    type: Optional[ksqlDBRelationType] = None

    @classproperty
    def get_relation_type(cls) -> Type[ksqlDBRelationType]:
        return ksqlDBRelationType

    def render(self):
        dl = self.ns_delimit
        path = list()
        if self.include_policy.database and self.database:
            path.append(self.database)
        if self.include_policy.schema and self.schema:
            path.append(self.schema)
        if self.name:
            path.append(self.name)

        try:
            ret = dl.join(path)
        except Exception as e:
            raise Exception(str(path))
        return ret

    def matches(
        self,
        database: Optional[str] = None,
        schema: Optional[str] = None,
        identifier: Optional[str] = None,
    ) -> bool:
        search = filter_null_values(
            {
                ComponentName.Database: database,
                ComponentName.Schema: schema,
                ComponentName.Identifier: identifier,
            }
        )

        if not search:
            # nothing was passed in
            pass

        for k, v in search.items():
            if not self._is_exactish_match(k, v):
                return False

        return True

    def information_schema(self, identifier: Optional[str] = None) -> "ksqlDBInformationSchema":
        return ksqlDBInformationSchema.from_relation(self, identifier)


@dataclass(frozen=True, eq=False, repr=False)
class ksqlDBInformationSchema(InformationSchema):
    quote_character: str = ""
    location: Optional[str] = None

    @classmethod
    def get_include_policy(cls, relation, information_schema_view):
        schema = True
        if information_schema_view in ("SCHEMATA", "SCHEMATA_OPTIONS", None):
            schema = False

        identifier = True
        if information_schema_view == "__TABLES__":
            identifier = False

        # In the future, let's refactor so that location/region can also be a
        # ComponentName, so that we can have logic like:
        #
        # region = False
        # if information_schema_view == "OBJECT_PRIVILEGES":
        #     region = True

        return relation.include_policy.replace(
            schema=schema,
            identifier=identifier,
        )

    def get_region_identifier(self) -> str:
        region_id = f"region-{self.location}"
        return self.quoted(region_id)

    @classmethod
    def from_relation(cls, relation, information_schema_view):
        info_schema = super().from_relation(relation, information_schema_view)
        if information_schema_view == "OBJECT_PRIVILEGES":
            # OBJECT_PRIVILEGES require a location.  If the location is blank there is nothing
            # the user can do about it.
            if not relation.location:
                msg = (
                    f'No location/region found when trying to retrieve "{information_schema_view}"'
                )
                raise raise_compiler_error(msg)
            info_schema = info_schema.incorporate(location=relation.location)
        return info_schema

    # override this method to interpolate the region identifier,
    # if a location is required for this information schema view
    def _render_iterator(self):
        iterator = super()._render_iterator()
        if self.location:
            return chain(
                islice(iterator, 1),  # project,
                [(None, self.get_region_identifier())],  # region id,
                islice(iterator, 1, None),  # remaining components
            )
        else:
            return iterator

    def replace(self, **kwargs):
        if "information_schema_view" in kwargs:
            view = kwargs["information_schema_view"]
            # we also need to update the include policy, unless the caller did
            # in which case it's their problem
            if "include_policy" not in kwargs:
                kwargs["include_policy"] = self.get_include_policy(self, view)
        return super().replace(**kwargs)
