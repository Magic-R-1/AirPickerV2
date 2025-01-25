from marshmallow import Schema, fields

from app.schemas.boxscore_schema import BoxscoreSchema
from app.schemas.team_schema import TeamSchema


class PlayerSchema(Schema):

    player_id = fields.Int(required=True)
    first_name = fields.Str(allow_none=True)
    last_name = fields.Str(allow_none=True)
    display_first_last = fields.Str(allow_none=True)
    display_last_comma_first = fields.Str(allow_none=True)
    display_fi_last = fields.Str(allow_none=True)
    player_slug = fields.Str(allow_none=True)

    birthdate = fields.Str(allow_none=True)
    school = fields.Str(allow_none=True)
    country = fields.Str(allow_none=True)
    last_affiliation = fields.Str(allow_none=True)
    height = fields.Str(allow_none=True)
    weight = fields.Int(allow_none=True)
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
    games_played_current_season_flag  = fields.Bool(allow_none=True)
    greatest_75_flag = fields.Bool(allow_none=True)

    draft_year = fields.Str(allow_none=True)
    draft_round = fields.Str(allow_none=True)
    draft_number = fields.Str(allow_none=True)

    # Relation avec Team
    team = fields.Nested(TeamSchema, allow_none=True)
    # boxscores = fields.Nested(BoxscoreSchema, allow_none=True)
