from odoo import api,fields,models,_

class sample(models.Model):
    _name= 'sample.sample'

    @api.multi
    def Calc_data(self):

        if self.select == 'sum':
            self.ans = self.a + self.b
            print ('\n\n',self.ans,'\n\n')
        elif self.select == 'minus':
            self.ans= self.a-self.b
            print ('\n\n', self.ans, '\n\n')
        ctx = dict(self.env.context)
        ctx.update({'default_ans': self.ans})
        print ("\n\n\n-------ctx---------->",ctx)
        return {
            'name': _('Display ans'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sample.sample',
            'view_id': self.env.ref('hotel_management.sample_form_another_view').id,
            'context':ctx,
            'type': 'ir.actions.act_window',
            'target': 'new'
        }


    a = fields.Float('A')
    b = fields.Float('B')
    select = fields.Selection([('sum','Sum'),('minus','Subtraction')])
    ans = fields.Float('Ans',readonly=True)

