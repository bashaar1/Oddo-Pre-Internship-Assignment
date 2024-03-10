from odoo import api, fields, models
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError


class EstateProperties(models.Model):
    _name = "estate.property"
    _description = "Model for Real Estate Properties"

    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)", "The expected price must be positive"),
        ("check_selling_price", "CHECK(selling_price >= 0)", "The offer price must be positive"),
    ]

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Post Code')
    date_availability = fields.Date(string='Available Date',
                                    default=lambda self: datetime.now() + relativedelta(months=3), copy=False)
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer(string='Bedrooms', default="2")
    living_area = fields.Integer(string='Living Area')
    facades = fields.Integer(string='facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation = fields.Selection(string='Type',
                                          selection=[('north', 'North'), ('south', 'South'), ('east', 'East'),
                                                     ('west', 'West')])
    state = fields.Selection(string='State', selection=[('new', 'New'), ('offer_received', 'Offer Received'),
                                                        ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'),
                                                        ('cancelled', 'Cancelled')], default='new', copy=False,
                             required=True)
    property_type_id = fields.Many2one("estate.property_type", string="Property Type")
    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
    user_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Property Offer")

    total_area = fields.Float(compute="_compute_total", string="Total Area")

    best_price = fields.Float(compute="_maximum_offer", string="Maximum Offer")

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            total_area = record.living_area + record.garden_area
            record.total_area = total_area

    @api.depends("offer_ids.price")
    def _maximum_offer(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price")) if record.offer_ids else 0.0

    @api.onchange("garden")
    def _onchange_garden_field(self):
        if self.garden_area:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden = 0
            self.garden_orientation = False

    def action_cancel(self):
        if 'sold' in self.mapped('state'):
            raise UserError("Sold property cannot be canceled")
        return self.write({"state": "canceled"})

    def action_sold(self):
        if 'cancelled' in self.mapped('state'):
            raise UserError("Canceled property cannot be sold")
        return self.write({"state": "sold"})

    @api.constrains('selling_price')
    def _check_selling_price(self):
        if self.selling_price < 0.90*self.expected_price:
            raise ValidationError("The selling price cannot be less than 90% of expected price")
