from odoo import api,fields,models

class sample(models.Model):
    _name= 'sample.sample'

    @api.multi
    def Calc_data(self):
        ans = 0
        if self.select == 'sum':
            ans = self.a + self.b
            print ('\n\n',ans,'\n\n')
        elif self.select == 'minus':
            ans= self.a-self.b
            print ('\n\n', ans, '\n\n')

    a = fields.Float('A')
    b = fields.Float('B')
    select = fields.Selection([('sum','Sum'),('minus','Subtraction')])


