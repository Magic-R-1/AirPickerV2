from datetime import date

from marshmallow import Schema, fields, pre_load


class TeamGameLogSchema(Schema):
    team_id = fields.Int(required=True)

    game_id = fields.Str(required=True)
    game_date = fields.Date(required=True)
    matchup = fields.Str(required=True)

    wl = fields.Str(allow_none=True)
    w = fields.Int(allow_none=True)
    l = fields.Int(allow_none=True)
    w_pct = fields.Float(allow_none=True)

    minutes = fields.Integer(allow_none=True)

    fgm = fields.Int(allow_none=True)
    fga = fields.Int(allow_none=True)
    fg_pct = fields.Float(allow_none=True)
    fg3m = fields.Int(allow_none=True)
    fg3a = fields.Int(allow_none=True)
    fg3_pct = fields.Float(allow_none=True)
    ftm = fields.Int(allow_none=True)
    fta = fields.Int(allow_none=True)
    ft_pct = fields.Float(allow_none=True)

    o_reb = fields.Int(allow_none=True)
    d_reb = fields.Int(allow_none=True)
    reb = fields.Int(allow_none=True)

    ast = fields.Int(allow_none=True)
    stl = fields.Int(allow_none=True)
    blk = fields.Int(allow_none=True)
    tov = fields.Int(allow_none=True)
    pf = fields.Int(allow_none=True)
    pts = fields.Int(allow_none=True)

    # Ajout de cette méthode pour convertir automatiquement les dates reçues en format str acceptés par le model
    @pre_load
    def convert_date(self, data, **kwargs):
        if isinstance(data.get("game_date"), date):
            data["game_date"] = data["game_date"].isoformat()  # Convertir en 'YYYY-MM-DD'
        return data
