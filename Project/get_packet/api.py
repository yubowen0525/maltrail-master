from flask_restful import Resource, fields, marshal_with
from flask_restful import reqparse

from core.log import log_error
from .packet_process import _process_packet


class Statu():
    def __init__(self, statu, message=None):
        self.statu = statu
        self.message = message


# TodoList
# shows a list of all todos , and lets you POST to add new tasks
class getPacket(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('config', type=dict, required=True, help="Name cannot be blank!")
    parser.add_argument('sec', type=int, required=True, help="Name cannot be blank!")
    parser.add_argument('usec', type=int, required=True, help="Name cannot be blank!")
    parser.add_argument('ip_offset', type=int, required=True, help="Name cannot be blank!")
    parser.add_argument('packet', type=str, required=True, help="Name cannot be blank!")

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
            # try:
            #     _process_packet(packet, sec, usec, ip_offset)
            # except Exception as e:
            #     log_error("\n\n[!] %s" % (e))
            #     return Statu(-1, e), 200
            return Statu(1), 200
        else:
            return Statu(-1), 200

    @marshal_with(resource_fields, envelope='resource')
    def get(self):
        return "hello"
