from marshmallow import Schema, fields

class TeamSchema(Schema):

    team_id = fields.Int(required=True)

    team_full_name = fields.Str(allow_none=True)
    team_tricode = fields.Str(allow_none=True)
    team_name = fields.Str(allow_none=True)

    team_city = fields.Str(allow_none=True)
    team_state = fields.Str(allow_none=True)

    year_founded = fields.Int(allow_none=True)
