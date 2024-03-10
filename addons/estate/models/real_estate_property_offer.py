from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float(string="Price", required=True)
    state = fields.Selection(string="Status", selection=[('accepted','Accepted'),('refused','Refused')], copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(string ='Deal Line Date',compute="_compute_date_deadline", inverse="_inverse_date_deadline")



    #Check
    @api.depends('create_date','validity')
    def _compute_date_deadline(self):
        for offer_record in self:
            date = offer_record.create_date.date() if offer_record.create_date else fields.Date.today()
            offer_record.date_deadline = date + relativedelta(days=offer_record.validity)

    def _inverse_date_deadline(self):
        for offer_record in self:
            date = offer_record.create_date.date() if offer_record.create_date else fields.Date.today()
            offer_record.validity = (offer_record.date_deadline - date).days


    def action_accept(self):
        if "accepted" in self.mapped("property_id.offer_ids.state"):
            raise UserError("Another offer already been accepted")
        self.write(
            {
                "state": "accepted",
            }
        )
        return self.mapped("property_id").write(
            {
                "state": "offer_accepted",
                "selling_price": self.price,
                "buyer": self.partner_id.id,
            }
        )

    def action_refuse(self):
        return self.write(
            {
                "state": "refused",
            }
        )