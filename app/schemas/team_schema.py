from marshmallow import Schema, fields

class TeamSchema(Schema):
    team_id = fields.Int(required=True)
    full_name = fields.Str(allow_none=True)
    abbreviation = fields.Str(allow_none=True)
    nickname = fields.Str(allow_none=True)
    city = fields.Str(allow_none=True)
    state = fields.Str(allow_none=True)
    year_founded = fields.Int(allow_none=True)

    # Relation one-to-many avec Player
    # players = fields.Nested(PlayerSchema, allow_none=True)