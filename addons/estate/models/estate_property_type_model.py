from odoo import api, fields, models


class EstatePropertiesTypes(models.Model):
    _name = "estate.property_type"
    _description = "Real Estate Property Type"

    name = fields.Char(string='Name')
