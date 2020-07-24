from flask_restful import Resource, fields, marshal_with
from flask_restful import reqparse


class Statu():
    def __init__(self,statu):
        self.statu = statu

# TodoList
# shows a list of all todos , and lets you POST to add new tasks
class getPacket(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('type',type=str,required=True,help="Name cannot be blank!")
    parser.add_argument('message',type=str,required=True,help="Name cannot be blank!")

    resource_fields = {
        'statu':fields.Integer
    }

    @marshal_with(resource_fields, envelope='resource')
    def post(self):

        args = self.parser.parse_args()
        if args['type'] == "np":
            packet = args['message']
            print(packet)
            # print(packet)
            return Statu(1), 200
        else:
            return Statu(-1), 200


