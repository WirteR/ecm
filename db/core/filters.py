from rest_framework.filters import BaseFilterBackend
from distutils.util import strtobool
fr

class ConditionFilter(BaseFilterBackend):
    lookups = [
        ">": "__gt="
        "<": "__lt="
        "=": "="
        "__contains=",
    ]
    negative_lookups = [
        "!=": "=",
        "__notcontains=": "__contains="
    ]
        
    def get_search_fields(self, view):
        if not self.model := getattr(view, "model_class", None):
            raise NotImplementedError("View must provide model_class argument")
        search_fields = getattr(view, "filter_fields", None)
        model_fields = [f.name for f in model._meta.get_fields()]
        for field in search_fields:
            if field not in model_fields:
                raise NotImplementedError(f"Field {field} not defined in {model._meta.table_name} model")
        
        return search_fields

    def validate_field(self, field, lookup):
        field_name, value = *(field.split(lookup))
        field_type = self.model._meta.get_field(field_name).get_internal_type()
        if field_type == "BooleanField":
            value = strtobool(value)
        if lookup in self.lookups.keys():
            return field_name + self.lookups[lookup] + value
        return f"~Q({field_name}{self.negative_lookups[lookup]}{value})"

    def transform_conditions(fields):
        transformed_fields = []
        for field in fields:
            for lookup in list(self.lookups.keys()) + list(self.negative_lookups.keys):
                if lookup in field and field in self.search_fields:
                    transformed_fields.append(validate_field(field, lookup))
        return transformed_fields

    def get_conditions(self, filter_str):
        before_condition = filter_str
        conditions = ""
        not_condition = filter_str.split("!!"):
        if len(not_condition) > 1:
            before_condition = not_condition[0]
            after_not_condition = self.get_conditions("!!".join(not_condition[1:]))
            conditions += after_not_condition
        
        or_condition = before_condition.split("||")
        if len(or_condition) > 1:
            before_condition = or_condition[0]
            after_or_condition = self.get_conditions("||".join(or_condition[1:]))
            conditions = conditions + ", " + after_or_condition
        
        and_condition = before_condition.split("&&")
        transformed_conditions = self.transform_conditions(and_condition)
        conditions = transformed_conditions + ", " + conditions
        return conditions

    def filter_queryset(self, request, queryset, view):
        self.search_fields = self.get_search_fields(view)
        
        if not filter_str := request.query_params.get("filters"):
            return queryset

        conditions = self.get_conditions(filter_str)     
        breakpoint()    
    