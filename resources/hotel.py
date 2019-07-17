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
        return {'hoteis': hoteis}


class Hotel(Resource):
    argumentos = reqparse.RequestParser()  # cria variável dos parâmetros
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    @staticmethod
    def find_hotel(hotel_id):  # verifica
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return None

    def get(self, hotel_id):

        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            return hotel
        return {'message': 'Hotel not found'}, 404

    def post(self, hotel_id):

        dados = Hotel.argumentos.parse_args()  # transfere para lista
        hotel_objeto = HotelModel(hotel_id, **dados)
        novo_hotel = hotel_objeto.json()
        hoteis.append(novo_hotel)
        return novo_hotel, 200

    def put(self, hotel_id):

        dados = Hotel.argumentos.parse_args()  # transfere lista
        hotel_objeto = HotelModel(hotel_id, **dados)
        # converte o conteúdo de dicionário para json e armazena em novo_hotel
        novo_hotel = hotel_objeto.json()
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            hotel.update(novo_hotel)
            return novo_hotel, 200

        hoteis.append(novo_hotel)  # caso o hotel não exista, cria e retorna
        return novo_hotel, 201  # código de hotel criado em resposta http

    def delete(self, hotel_id):
        global hoteis  
        # avisa ao python que estamos referenciando a variável global hotel
        # criando uma nova lista sem o hotel_id que foi rececbido
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        return {'message': 'Hotel deleted'}
