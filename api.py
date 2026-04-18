from flask import Flask, request,  jsonify
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def carregar_animais():
        with open('animais.json', 'r') as f:
            return json.load(f)

def salvar_animais(animais):
    with open('animais.json', 'w') as f:
        json.dump(animais, f, indent=4)

@app.get('/animais/<int:id>') # localhost/animais/1
def get_animais_pr_id(id):
    animais = carregar_animais()

    for animal in animais:
        if animal.get('id') == id:
            return jsonify(animal), 200
    return jsonify({"mensagem": "Animal não encontrado"}), 404

def carregar_abrigos():
        with open('abrigos.json', 'r') as f:
            return json.load(f)

def salvar_abrigos(abrigos):
    with open('abrigos.json', 'w') as f:
        json.dump(abrigos, f, indent=4)

@app.get('/abrigos/<int:id>') # localhost/animais/1
def get_abrigos_pr_id(id):
    abrigos = carregar_abrigos()

    for abrigo in abrigos:
        if abrigo.get('id') == id:
            return jsonify(abrigo), 200
    return jsonify({"mensagem": "Abrigo não encontrado"}), 404

def carregar_usuarios():
        with open('usuarios.json', 'r') as f:
            return json.load(f)

def salvar_usuarios(usuarios):
    with open('usuarios.json', 'w') as f:
        json.dump(usuarios, f, indent=4)

@app.get('/usuarios/<int:id>') # localhost/animais/1
def get_usuarios_pr_id(id):
    usuarios = carregar_usuarios()

    for usuario in usuarios:
        if usuario.get('id') == id:
            return jsonify(usuario), 200

    return jsonify({"mensagem": "Usuario não encontrado"}), 404

@app.get('/animais')
def get_animais():
    animais = carregar_animais()

    nome = request.args.get('nome') #http://localhost.../animais?nome=A
    especie = request.args.get('especie')

    resultado = []

    for animal in animais:
        if nome and animal.get('nome') != nome:
            continue
        if especie and animal.get('especie') != especie:
            continue
        resultado.append(animal)
    return jsonify(resultado), 200

@app.post('/animais')
def post_animais():
    dados = request.json

    if not dados.get('nome'):
        return jsonify({"mensagem": "Campo nome é obrigatorio"}), 400
    
    nome_animal = dados.get('nome')
    if nome_animal is None:
        return jsonify({"erro": "Campo nome é obrigatório"}), 400
    if not nome_animal.isalpha():
        return jsonify({"erro": "O nome deve conter apenas letras"}), 422
    if not nome_animal.istitle():
        return jsonify({"erro": "O nome deve ter a primeira letra maiuscula"}), 422
    if not len(nome_animal) >= 2:
        return jsonify({"erro": "O nome não pode ser menor ou igual a 1 caractere"}), 422
    if not len(nome_animal) <= 20:
        return jsonify({"erro": "O nome não pode ser maior que 20 caracteres"}), 422
    
    if not dados.get('especie'):
        return jsonify({"mensagem": "Campo especie é obrigatorio"}), 400

    tipos_validos = ['cachorro', 'gato', 'passaro', 'peixe']
    if dados.get('especie') not in tipos_validos:
        return jsonify({"mensagem": "Tipo de animal inválido!"}), 422
    
    if not dados.get('idade'):
        return jsonify({"mensagem": "Campo idade é obrigatorio"}), 400
    
    idade = dados.get('idade')
    if idade is None:
        return jsonify({"erro": "Campo 'idade' é obrigatório"}), 400
    if not isinstance(idade, int):
        return jsonify({"erro": "'idade' deve ser um número inteiro"}), 422
    
    with open('animais.json', 'r') as f:
        animais = json.load(f)

    animais.append(dados)

    with open('animais.json', 'w') as f:
        json.dump(animais, f, indent=4)

    resposta = {
        "mensagem": "Animal cadastrado com sucesso!"
    }

    return jsonify(resposta), 201

@app.post('/usuario')
def post_usuario():
    dados_usuario = request.json

    if not dados_usuario.get('nome'):
        return jsonify({"mensagem": "Campo nome é obrigatorio"}), 400
    
    nome_usuario = dados_usuario.get('nome')
    if nome_usuario is None:
        return jsonify({"erro": "Campo nome é obrigatório"}), 400
    if not nome_usuario.isalpha():
        return jsonify({"erro": "Campo nome deve conter apenas letras"}), 422
    if not nome_usuario.istitle():
        return jsonify({"erro": "O nome deve ter a primeira letra maiuscula"}), 422
    if not len(nome_usuario) >= 2:
        return jsonify({"erro": "O nome não pode ser menor ou igual a 1"}), 422
    if not len(nome_usuario) <= 154:
        return jsonify({"erro": "O nome não pode ser maior que 154 caracteres"}), 422
    
    if not dados_usuario.get('cpf'):
        return jsonify({"mensagem": "Campo cpf é obrigatorio"}), 400
    
    cpf = dados_usuario.get('cpf')
    if cpf is None:
        return jsonify({"erro": "Campo cpf é obrigatório"}), 400
    if not cpf.isnumeric():
        return jsonify({"erro": "Campo cpf deve conter apenas números"}), 422
    if not len(cpf) == 11:
        return jsonify({"erro": "Campo cpf deve conter 11 digítos"}), 422
    
    if not dados_usuario.get('telefone'):
        return jsonify({"mensagem": "Campo telefone é obrigatorio"}), 400
    
    telefone = dados_usuario.get('telefone')
    if telefone is None:
        return jsonify({"erro": "Campo telefone é obrigatório"}), 400
    if not telefone.isnumeric():
        return jsonify({"erro": "Campo telefone deve conter apenas números"}), 422
    if not len(telefone) == 11:
        return jsonify({"erro": "Campo telefone deve conter 11 digítos"}), 422
    
    if not dados_usuario.get('email'):
        return jsonify({"mensagem": "Campo email é obrigatorio"}), 400
    
    email = dados_usuario.get('email')
    if email is None:
        return jsonify({"erro": "Campo email é obrigatório"}), 400
    if not len(email) <= 256:
        return jsonify({"erro": "Campo email não pode ser maior que 256 caracteres"}), 422
    
    if not dados_usuario.get('endereco'):
        return jsonify({"mensagem": "Campo endereço é obrigatorio"}), 400
    
    endereco = dados_usuario.get('endereco')
    if endereco is None:
        return jsonify({"erro": "Campo endereço é obrigatório"}), 400
    if not len(endereco) <= 60:
        return jsonify({"erro": "Campo endereço não pode ser maior que 60 caracteres"}), 422

    with open('usuario.json', 'r') as f:
        usuario = json.load(f)

    usuario.append(dados_usuario)

    with open('usuario.json', 'w') as f:
        json.dump(usuario, f, indent=4)

    resposta = {
        "mensagem": "Usuário cadastrado com sucesso!"
    }

    return jsonify(resposta), 201

def carregar_json(arquivo):
    with open(arquivo, 'r') as f:
        return json.load(f)

@app.route('/abrigos', methods=['GET'])
def get_abrigos():
    return jsonify(carregar_json('abrigos.json'))

@app.route('/categorias', methods=['GET'])
def get_categorias():
    return jsonify(["cachorro", "gato", "passaro", "peixe"])

if __name__ == '__main__':
    app.run(debug=True)