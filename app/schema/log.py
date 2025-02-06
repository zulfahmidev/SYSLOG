from app import marshmallow
from marshmallow import validate, Schema
from localoka_service.schema import CollectionSchema, fields, ParamSchema

PAYLOAD_TYPES = [
    "received", "request_to_service", "response_from_service", 
    "request_to_third_party", "response_from_third_party", "response"
]

class LogPayloadSchema(Schema):
    type = fields.String(required=True, validate=validate.OneOf(PAYLOAD_TYPES))  # Harus sesuai dengan daftar payload types
    payload = fields.String(required=True)
    note = fields.String()
    title = fields.String()

# Schema Details
class LogSchema(Schema):
    timestamp = fields.DateTime(required=True, format="%Y-%m-%dT%H:%M:%S")
    method = fields.String(required=True)
    path = fields.String(required=True)
    payloads = fields.List(fields.Nested(LogPayloadSchema))  # List of nested payload objects
    level = fields.String(required=True)
    status_code = fields.Integer(required=True)
    elapsed_time = fields.Float(required=True)
    service = fields.String(required=True)
    additional_details = fields.String()  # JSON string

    class Meta:
		# Fields to expose
        fields = [
			"service",
			"level",
			"method",
            "payloads",
			"path",
			"status_code",
			"message",
			"timestamp",
            "elapsed_time",
            "additional_details"
        ]
  
class LogCollectionSchema(Schema):
    items = marshmallow.Nested(LogSchema, many=True, data_key="data")

    class Meta:
        # Fields to expose
        fields = [
            "items",
            "_meta"
        ]

    
# class LogParamSchema(ParamSchema):
#     order_by = fields.Str(required=False, validate=validate.OneOf(valid_methods))
#     filter_uids = fields.ListOrStringField(required=False)
#     method = fields.Str(required=False)
#     path = fields.Str(required=False)
#     status = fields.Str(required=False)
#     month = fields.Integer(required=False)
#     year = fields.Integer(required=False)
#     time = fields.Str(required=False)

#     class Meta:
#         fields = (
#             *ParamSchema.opts.fields,
#         )