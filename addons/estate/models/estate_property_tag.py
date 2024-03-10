from odoo import api, fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Model for Real Estate Property Tag"

    _sql_constraints = [
        ('name_uniq', 'UNIQUE (name)', 'You can not have two tag with the same name!')
    ]

    name = fields.Char(string='Name', required=True)
