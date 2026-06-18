from flask import request
from functools import wraps
from pydantic import ValidationError


def transform_validation_error(e) -> dict:
    errors = {}
    for error in e.errors():
        field = error["loc"][0]
        errors[field] = error["msg"]

    return errors


def validate_body(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                validated_data = schema(**request.json)

                return func(validated_data, *args, **kwargs)

            except ValidationError as e:
                return {
                    "message": "Validation failed",
                    "errors": transform_validation_error(e)
                }, 400

        return wrapper

    return decorator
