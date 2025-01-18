from marshmallow import Schema, fields

from app.schemas.team_schema import TeamSchema


class PlayerSchema(Schema):
    person_id = fields.Int(required=True)
    first_name = fields.Str(allow_none=True)
    last_name = fields.Str(allow_none=True)
    display_first_last = fields.Str(allow_none=True)
    display_last_comma_first = fields.Str(allow_none=True)
    display_fi_last = fields.Str(allow_none=True)
    player_slug = fields.Str(allow_none=True)
    birthdate = fields.Date(allow_none=True)
    school = fields.Str(allow_none=True)
    country = fields.Str(allow_none=True)
    last_affiliation = fields.Str(allow_none=True)
    height = fields.Str(allow_none=True)
    weight = fields.Float(allow_none=True)
    season_exp = fields.Int(allow_none=True)
    jersey = fields.Int(allow_none=True)
    position = fields.Str(allow_none=True)
    roster_status = fields.Str(allow_none=True)
    team_id = fields.Int(allow_none=True)
    team_name = fields.Str(allow_none=True)
    team_abbreviation = fields.Str(allow_none=True)
    team_code = fields.Str(allow_none=True)
    team_city = fields.Str(allow_none=True)
    player_code = fields.Str(allow_none=True)
    from_year = fields.Int(allow_none=True)
    to_year = fields.Int(allow_none=True)
    dleague_flag = fields.Bool(allow_none=True)
    nba_flag = fields.Bool(allow_none=True)
    games_played_flag = fields.Bool(allow_none=True)
    draft_year = fields.Str(allow_none=True)    # String car peut être Undrafted
    draft_round = fields.Str(allow_none=True)   # String car peut être Undrafted
    draft_number = fields.Str(allow_none=True)  # String car peut être Undrafted

    # Relation many-to-one avec Team
    team = fields.Nested(TeamSchema, allow_none=True)
