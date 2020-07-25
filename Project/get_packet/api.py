from flask_restful import Resource, fields, marshal_with
from flask_restful import reqparse


class Statu():
    def __init__(self, statu):
        self.statu = statu


# TodoList
# shows a list of all todos , and lets you POST to add new tasks
class getPacket(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('config', type=dict, required=True, help="Name cannot be blank!")
    parser.add_argument('sec', type=int, required=True, help="Name cannot be blank!")
    parser.add_argument('usec', type=int, required=True, help="Name cannot be blank!")
    parser.add_argument('ip_offset', type=int, required=True, help="Name cannot be blank!")
    parser.add_argument('packet', type=bytes, required=True, help="Name cannot be blank!")

    resource_fields = {
        'statu': fields.Integer
    }

    @marshal_with(resource_fields, envelope='resource')
    def post(self):

        args = self.parser.parse_args()
        if 'type' in args['config'] and args['config']['type'] == 'np':
            packet = args['packet']
            sec = args['sec']
            usec = args['usec']
            ip_offset = args['ip_offset']
            print('---------------------------------------------------------------------------')
            print("sec:%d, usec:%d, ip_offset:%d" % (sec, usec, ip_offset))
            print("get packet: ", packet)
            print('----------------------------------------------------------------------------')
            return Statu(1), 200
        else:
            return Statu(-1), 200

    @marshal_with(resource_fields, envelope='resource')
    def get(self):
        return "hello"
