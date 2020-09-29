from recurly import Resource
import datetime


class MyResource(Resource):
    schema = {
        "object": str,
        "my_string": str,
        "my_int": int,
        "my_float": float,
        "my_bool": bool,
        "my_datetime": datetime,
        "my_sub_resource": "MySubResource",
        "my_sub_resources": ["MySubResource"],
    }


class MySubResource(Resource):
    schema = {"object": str, "my_string": str}


class ErrorMayHaveTransaction(Resource):
    schema = {
        "message": str,
        "params": list,
        "transaction_error": "TransactionError",
        "type": str,
    }


class Empty(Resource):
    schema = {}
