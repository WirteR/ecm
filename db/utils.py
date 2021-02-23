from rest_framework.serializers import ValidationError


def get_ids(model, fields: dict, search_fields: list):
    ids = []
    for field in fields:
        for f in search_fields:
            if f not in list(field.keys()):
                raise ValidationError(f"Search field {f} doesnt exists in passed data")
        
        filters = {k:field[k] for k in search_fields if field[k]}
        qs = model.objects.filter(**filters)
        if qs.exists():
            ids += qs.values_list("id", flat=True)
        else:
            new_instance = model.objects.create(**field)
            ids.append(new_instance.id)
    return ids