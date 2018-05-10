from odoo import api,fields,models
from datetime import datetime,date,timedelta

class room_type(models.Model):
    _name='room.type'

    name=fields.Char('Type_Name')
    subtype=fields.Char('Sub_type')
    facility_ids=fields.One2many('room.facility','type_id','Facilities')

class room_details(models.Model):
    _name='room.details'


    @api.model
    def create(self,vals):
        product_vals = {}
        print ('\n\n\n-----------Vals---->',vals,'\n\n')

        # seq= self.env['ir.sequence'].next_by_code('room.details.seq')
        # print ('\n\nsequence---------->',seq)
        # vals.update({'name':seq})

        product_rec=self.env['product.template']

        res = super(room_details, self).create(vals)
        product_vals.update({
            'name': vals.get('name'),
            'list_price': vals.get('terrif'),
            'type': 'service',
            'purchase_method': 'purchase',
            'purchase_ok': False,
            'room_details_id':res.id,
        })
        create_pro = product_rec.create(product_vals)
        print ('\n\n------------------create_pro------->', create_pro)

        print ('\n\n\n-----------RES---->', res, '\n\n')
        return res

    # @api.multi
    # def write(self,vals):
    #     product_vals = {}
    #     print ('\n\n\n-----------Vals---->', vals, '\n\n')
    #
    #     product_rec = self.env['product.template'].search([('room_details_id','=',self.id)])
    #     print ('\n\n----------product_rec=---->',product_rec)
    #     print ('\n\nidssssss-----', self.id, product_rec.id)
    #     product_vals.update({
    #             'name': vals.get('name'),
    #             'list_price': vals.get('terrif'),
    #             'type': 'service',
    #             'purchase_method': 'purchase',
    #             'purchase_ok': False
    #
    #         })
    #     write_pro = product_rec.write(product_vals)
    #     print ('\n\n------------------write_pro------->', write_pro)
    #
    #     res = super(room_details, self).write(vals)
    #     print ('\n\n\n-----------RES---->', res, '\n\n')
    #     return res

    @api.onchange('name','terrif')
    def _onchange_name(self):
        print('\n--------------self', self._origin)
        product_rec = self.env['product.template'].search([('room_details_id', '=', self._origin.id)])
        print ('\n\n--------product_rec------>', product_rec.name, self.name,product_rec.list_price,self.terrif)
        if product_rec:
            product_rec.write({'name': self.name,'list_price':self.terrif})
            print("\n\n\n rec--",product_rec, product_rec.name)


    @api.onchange('type_id')
    def _get_facility(self):
        # list1 = []
        # print ("-------------------------------------------seld-->",self)
        val=self.env['room.facility'].search([('type_id','=',self.type_id.id),('mode','=','free')])
        # print ('\n\n\n%%%T',val)
        # for line in val:
        #     list1.append((0,0,{'name':line.name,'mode':line.mode}))
        print ('\n\n----------Val.ids--->',val.ids,'\n\n')
        self.facility_ids = val.ids
        # print ('\n\n\njasd',self.facility_ids.name)
        # diffrent method
        # for rec in self:
        #     print ('---------------------->',rec.type_id.facility_ids)
        #     for line in rec.type_id.facility_ids:
        #         print ('\n\n\nline---=====',line.mode)
        #         list1.append((0,0,{'name':line.name,'mode':line.mode}))
        #     print ('\n\n\n\nkjgf--->',list1)
        #     self.facility_ids=list1
        #     print ('\n\n\n\n========ids',self.facility_ids)

    @api.multi
    def action_clean(self):
        self.state='clean'

    @api.multi
    def action_cancel(self):
        self.state='cancel'

    @api.multi
    def action_inspect(self):
        self.state = 'inspect'

    @api.multi
    def action_done(self):
        self.state = 'done'

    @api.multi
    def action_dirty(self):
        self.state = 'dirty'

    name=fields.Char('Room_name/No.',required=True)
    type_id=fields.Many2one('room.type','Room Type')
    state=fields.Selection([('dirty','Dirty'),('clean','Clean'),('inspect','Inspect'),('done','Done'),
                            ('cancel','Cancelled')],default='dirty')
    specification=fields.Text('Specification')
    occupancy=fields.Integer('Occupancy')
    terrif=fields.Float('Terrif')
    facility_ids=fields.One2many('room.facility','details_id','Facilities')
    product_id = fields.Many2one('product.template')
    hotel_folio_id = fields.Many2one('hotel.folio')

class room_facility(models.Model):
    _name='room.facility'

    name=fields.Char('Facility_name')
    type_id = fields.Many2one('room.type','Room')
    mode=fields.Selection([('free','Free'),('charge','Chargable')],'Mode')
    charge=fields.Float('Charge')
    details_id=fields.Many2one('room.details','Room Details')

class hotel_folio(models.Model):
    _name='hotel.folio'

    @api.model
    def create(self,vals):
        seq = self.env['ir.sequence'].next_by_code('hotel.folio.seq')
        vals.update({'name':seq})
        res = super(hotel_folio, self).create(vals)
        return res


    @api.onchange('check_in','duration')
    def _onchange_checkout(self):
        val = self.check_in
        print ('\n\n------------------date----------\n',val,self.duration)
        self.check_out = datetime.strptime(val,"%Y-%m-%d") + timedelta(days=self.duration)
        print ('----------------check_out--------------',self.check_out)

    @api.onchange('guest_id')
    def _onchange_guest(self):
        val = self.guest_id
        print ('\n\n-----------------guest----------\n', val)
        self.email = val.email
        self.mobile = val.phone
        print ('\n----------------emial--------------', self.email,self.mobile)


    name = fields.Char('name',readonly=True)
    date = fields.Datetime('Date',default=datetime.today())
    room_details_ids = fields.One2many('room.details','hotel_folio_id','Room Details')
    total = fields.Float('Total')
    folio_bool = fields.Boolean('Folio')
    member_bool = fields.Boolean('Member')
    guest_id = fields.Many2one('res.partner')
    email = fields.Char('Email')
    mobile = fields.Char('Phone Number')
    duration = fields.Integer('Days')
    check_in = fields.Date(string ='Check_in', default=datetime.today())
    check_out = fields.Date('Check_out')


class hotel_folio_line(models.Model):
    _name= 'hotel.folio.line'


    @api.onchange('name')
    def _onchange_name(self):
        self.rent = self.name.terrif

    name = fields.Many2one('room.details','Room')
    description = fields.Char('Description')
    rent = fields.Float('Rent')

class product_template(models.Model):
    _inherit='product.template'

    room_details_id = fields.Many2one('room.details','Room Details id')


