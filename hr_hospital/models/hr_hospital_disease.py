from odoo import models, fields


class HRHDisease(models.Model):
    _name = 'hr.hospital.disease'
    _description = 'Disease'
    _parent_store = True
    _parent_name = "parent_id"
    _order = 'parent_left'

    name = fields.Char()
    description = fields.Text()


    parent_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string="Батьківська хвороба",
        index=True, ondelete='cascade'
    )
    child_ids = fields.One2many(
        comodel_name='hr.hospital.disease',
        inverse_name='parent_id',
        string="Підлеглі хвороби"
    )
    parent_path = fields.Char(index=True)
    parent_left = fields.Integer(index=True)
    parent_right = fields.Integer(index=True)
