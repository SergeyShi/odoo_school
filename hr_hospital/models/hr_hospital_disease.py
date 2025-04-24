from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HRHDisease(models.Model):
    """
    Disease model. Allows creating a hierarchical disease classifier for a medical institution.
    """
    _name = 'hr.hospital.disease'
    _description = 'Disease'
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = 'complete_name'
    _order = 'complete_name'

    name = fields.Char(index='trigram',
                       required=True)
    description = fields.Text()

    parent_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='Parent Disease',
        index=True, ondelete='cascade')

    child_ids = fields.One2many(
        comodel_name='hr.hospital.disease',
        inverse_name='parent_id',
        string='Sub Diseases')

    complete_name = fields.Char(
        compute='_compute_complete_name',
        recursive=True, store=True)

    parent_path = fields.Char(index=True, unaccent=False)

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        """
        Computes the full hierarchical name of the disease.
        """
        for record in self:
            if record.parent_id:
                record.complete_name = '%s / %s' % (
                    record.parent_id.complete_name, record.name)
            else:
                record.complete_name = record.name

    @api.constrains('parent_id')
    def _check_category_recursion(self):
        """
        Prevents creation of recursive disease categories.
        """
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive categories.'))

    @api.model
    def name_create(self, name):
        """
        Creates a new disease record with the specified name.
        """
        record = self.create({'name': name})
        return record.id, record.display_name

    @api.depends_context('hierarchical_naming')
    def _compute_display_name(self):
        """
        Computes the display name depending on the hierarchical naming context.
        """
        if self.env.context.get('hierarchical_naming', True):
            super()._compute_display_name()
            return
        for record in self:
            record.display_name = record.name
