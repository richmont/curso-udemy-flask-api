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
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def get(self, hotel_id):

        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found'}, 404

    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel_id '{}' already exists.\
".format(hotel_id)}
        dados = Hotel.argumentos.parse_args()  # transfere para lista
        hotel = HotelModel(hotel_id, **dados)
        hotel.save_hotel()
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
        hotel.save_hotel()
        return hotel.json(), 201

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            hotel.delete_hotel()
            return {'message': 'Hotel deleted'}
        # criando uma nova lista sem o hotel_id que foi rececbido
        return {'message': 'Hotel not found'}, 404
