from flask_restful import Resource, reqparse
from models.HotelModel import HotelModel
hoteis = [
    {
        'hotel_id': 'alpha',
        'nome': 'Alpha Hotel',
        'estrelas': 4.3,
        'diaria': 420.3,
        'cidade': 'Rio de Janeiro'
    },
    {
        'hotel_id': 'bravo',
        'nome': 'Bravo Hotel',
        'estrelas': 4.4,
        'diaria': 380.90,
        'cidade': 'Santa Catarina'
    },
    {
        'hotel_id': 'charlie',
        'nome': 'Charlie Hotel',
        'estrelas': 3.9,
        'diaria': 320.20,
        'cidade': 'Santa Catarina'
    }]


class Hoteis(Resource):
    def get(self):
        # SELECT * FROM hoteis
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}


class Hotel(Resource):
    argumentos = reqparse.RequestParser()  # cria variável dos parâmetros
    argumentos.add_argument('nome', type=str, required=True, help="The field \
        'nome' cannot be left blank")
    argumentos.add_argument('estrelas', type=float, required=True, help="The field \
        'nome' cannot be left blank")
    argumentos.add_argument('diaria', type=float, required=True, help="The field \
        'nome' cannot be left blank")
    argumentos.add_argument('cidade')

    def get(self, hotel_id):

        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found'}, 404

    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            # retorna 409 (Conflict) caso já haja hotel_id no banco
            return {"message": "Hotel_id '{}' already exists.\
".format(hotel_id)},409
        dados = Hotel.argumentos.parse_args()  # transfere para lista
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            #  internal server error
            return {'message': '\
                An internal error ocurred trying to save hotel.'}, 500
        return hotel.json()

    def put(self, hotel_id):

        dados = Hotel.argumentos.parse_args()  # transfere lista
        # verifica se o hotel existe no banco
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            # então atualiza os dados do hotel existente
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200
        # caso não encontre, crie e salve no banco
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            #  internal server error
            return {'message': '\
                An internal error ocurred trying to save hotel.'}, 500
        return hotel.json(), 201

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': '\
                An internal error ocurred trying to save hotel.'}, 500
            return {'message': 'Hotel deleted'},200
        return {'message': 'Hotel not found'}, 404
