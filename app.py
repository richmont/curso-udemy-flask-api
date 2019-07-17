from flask import Flask
from flask_restful import Api
from resources.hotel import Hoteis, Hotel

app = Flask(__name__)
# definir o endereço do arquivo de banco
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'

# evitar aviso chato
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

# criar tabelas antes da primeira requisição
@app.before_first_request
def cria_banco():
    banco.create_all()


api.add_resource(Hoteis,'/hoteis')
api.add_resource(Hotel,'/hoteis/<string:hotel_id>')


if __name__ == '__main__':
    # chamar a inicialização do banco apenas quando o aplicativo for rodado
    from sql_alchemy import banco   
    banco.init_app(app) 
    app.run(debug=True)