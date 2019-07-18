import unittest, requests


class Reqs():
    def post_request(base_url, hotel_id, dados):
        '''cria um elemento no banco
        retorna a resposta em json e o código de status'''
        resposta = requests.post(base_url + hotel_id, dados)
        return resposta.json(), resposta.status_code()

    def put_request(base_url, dados, hotel_id):
        # cria ou atualiza um elemento no banco
        # retorna a resposta em json e o código de status
        resposta = requests.put(base_url + hotel_id, dados)
        return resposta.json(), resposta.status_code()

    def get_request(base_url, hotel_id):
        # recebe um elemento do banco
        # retorna a resposta em json e o código de status
        resposta = requests.get(base_url + hotel_id)
        return resposta.json(), resposta.status_code()

    def delete_request(base_url, hotel_id):
        # recebe um elemento do banco
        # retorna a resposta em json e o código de status
        resposta = requests.delete(base_url + hotel_id)
        return resposta.json(), resposta.status_code()


class TestRequests(unittest.TestCase):
    global base_url

    def test_basic_post(self):
        reqs = Reqs()
        dados = {'nome': 'Cabrobó', 'estrelas': 3.0, 'diaria': 150, 'cidade': 'Cabrobó'}
        hotel_id = 'cabrobo'
        base_url = 'http://localhost:5000/hoteis/'
        requisicao, status = reqs.post_request(base_url, hotel_id, dados)
        self.assertEqual(status, 200)
        self.assertEqual(requisicao['nome'], 'Cabrobó')
        self.assertEqual(requisicao['estrelas'], 1.0)
        self.assertEqual(requisicao['diaria'], 1)
        self.assertEqual(requisicao['estrelas'], 1.0)
        self.assertEqual(requisicao['cidade'], 'Cabrobó')
        self.assertEqual(requisicao['hotel_id'], hotel_id)


if __name__ == '__main__':
    unittest.main()
