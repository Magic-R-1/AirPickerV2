from marshmallow import Schema, fields


class BoxscoreSchema(Schema):

    game_id = fields.String(required=True)

    team_id = fields.Integer(required=False)
    team_city = fields.String(required=False)
    team_name = fields.String(required=False)
    team_tricode = fields.String(required=False)
    team_slug = fields.String(required=False)

    player_id = fields.Integer(required=True)
    first_name = fields.String(required=False)
    family_name = fields.String(required=False)
    display_fi_last = fields.String(required=False)
    player_slug = fields.String(required=False)
    position = fields.String(required=False, allow_none=True)
    comment = fields.String(required=False, allow_none=True)
    jersey_num = fields.String(required=False, allow_none=True)
    minutes = fields.String(required=False, allow_none=True)

    fgm = fields.Integer(required=False)
    fga = fields.Integer(required=False)
    fg_pct = fields.Float(required=False)
    fg3m = fields.Integer(required=False)
    fg3a = fields.Integer(required=False)
    fg3_pct = fields.Float(required=False)
    ftm = fields.Integer(required=False)
    fta = fields.Integer(required=False)
    ft_pct = fields.Float(required=False)
    o_reb = fields.Integer(required=False)
    d_reb = fields.Integer(required=False)
    reb = fields.Integer(required=False)
    ast = fields.Integer(required=False)
    stl = fields.Integer(required=False)
    blk = fields.Integer(required=False)
    tov = fields.Integer(required=False)
    pf = fields.Integer(required=False)
    pts = fields.Integer(required=False)
    plus_minus_points = fields.Float(required=False)
