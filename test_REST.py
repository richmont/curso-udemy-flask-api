import unittest, requests


class Reqs():
    @staticmethod
    def post_request(base_url, hotel_id, dados):
        '''cria um elemento no banco
        retorna a resposta em json e o código de status'''
        url = base_url + hotel_id
        resposta = requests.post(url, dados)
        return resposta.json(), resposta.status_code
    
    @staticmethod
    def put_request(base_url, dados, hotel_id):
        # cria ou atualiza um elemento no banco
        # retorna a resposta em json e o código de status
        url = base_url + hotel_id
        resposta = requests.post(url, dados)
        return resposta.json(), resposta.status_code

    @staticmethod
    def get_request(base_url, hotel_id):
        # recebe um elemento do banco
        # retorna a resposta em json e o código de status
        # preparar para hotel_id vir vazio
        resposta = requests.get(base_url + hotel_id)
        return resposta.json(), resposta.status_code

    @staticmethod
    def delete_request(base_url, hotel_id):
        # recebe um elemento do banco
        # retorna a resposta em json e o código de status
        resposta = requests.delete(base_url + hotel_id)
        return resposta.json(), resposta.status_code


class TestRequests(unittest.TestCase):
    # global base_url

    def test_basic_post(self):
        reqs = Reqs()
        dados = {"nome": 'Cabrobo Hotel', 'estrelas': 3.0, 'diaria': 150, 'cidade': 'Cabrobó'}
        hotel_id = 'cabrobo'
        base_url = 'http://localhost:5000/hoteis/'
        requisicao, status = reqs.post_request(base_url, hotel_id, dados)

        if status == 409:
            # deletar hotel_id conflitante
            requisicao, status = reqs.delete_request(base_url, hotel_id)
            # falha se o servidor retornar erro 500 
            self.assertNotEqual(status, 500)
            # falha se o servidor não encontrar o hotel
            self.assertNotEqual(status, 404)
        # se o hotel não existir no banco, conseguiu ser inserido
        # testar se o status code é OK
        self.assertEqual(status, 200)
        self.assertEqual(requisicao['nome'], 'Cabrobo Hotel')
        self.assertEqual(requisicao['estrelas'], 3.0)
        self.assertEqual(requisicao['diaria'], 150)
        self.assertEqual(requisicao['cidade'], 'Cabrobó')
        self.assertEqual(requisicao['hotel_id'], hotel_id)

        # deleta a entrada antes de terminar
        requisicao, status = reqs.delete_request(base_url, hotel_id)
        # falha se o servidor retornar erro 500
        self.assertNotEqual(status, 500)
        # falha se o servidor não encontrar o hotel
        self.assertNotEqual(status, 404)


if __name__ == '__main__':
    unittest.main()
