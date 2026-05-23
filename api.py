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

@app.get('/animais/<int:id>')
def get_animais_pr_id(id):
    animais = carregar_animais()

    for usuario in animais:
        if usuario.get('id') == id:
            return jsonify(usuario), 200
    return jsonify({"Mensagem": "Animal não encontrado"}), 404

def carregar_abrigos():
        with open('abrigos.json', 'r') as f:
            return json.load(f)

def salvar_abrigos(abrigos):
    with open('abrigos.json', 'w') as f:
        json.dump(abrigos, f, indent=4)

@app.get('/abrigos/<int:id>')
def get_abrigos_pr_id(id):
    abrigos = carregar_abrigos()

    for abrigo in abrigos:
        if abrigo.get('id') == id:
            return jsonify(abrigo), 200
    return jsonify({"Mensagem": "Abrigo não encontrado"}), 404

def carregar_usuarios():
        with open('usuarios.json', 'r') as f:
            return json.load(f)

def salvar_usuarios(usuarios):
    with open('usuarios.json', 'w') as f:
        json.dump(usuarios, f, indent=4)

@app.get('/usuarios/<int:id>')
def get_usuarios_id(id):
    usuarios = carregar_usuarios()

    for usuario in usuarios:
        if usuario.get('id') == id:
            return jsonify(usuario), 200

    return jsonify({"Mensagem": "Usuario não encontrado"}), 404

@app.get('/animais')
def get_animais():
    animais = carregar_animais()

    nome = request.args.get('nome')
    especie = request.args.get('especie')

    resultado = []

    for animal in animais:
        if nome and animal.get('nome') != nome:
            continue
        if especie and animal.get('especie') != especie:
            continue
        resultado.append(animal)
    return jsonify(resultado), 200

@app.get('/usuarios')
def get_usuarios():
    usuarios = carregar_usuarios()

    nome = request.args.get('nome')
    cpf = request.args.get('cpf')

    resultado = []

    for usuario in usuarios:
        if nome and usuario.get('nome') != nome:
            continue
        if cpf and usuario.get('cpf') != cpf:
            continue
        resultado.append(usuario)
    return jsonify(resultado), 200

@app.post('/animais')
def post_animais():
    dados = request.json

    if not dados.get('nome'):
        return jsonify({"Mensagem": "Campo nome é obrigatorio"}), 400
    
    nome_animal = dados.get('nome')
    if not nome_animal.isalpha():
        return jsonify({"erro": "O nome deve conter apenas letras"}), 422
    if not len(nome_animal) >= 2:
        return jsonify({"erro": "O nome não pode ser menor ou igual a 1 caractere"}), 422
    if not len(nome_animal) <= 20:
        return jsonify({"erro": "O nome não pode ser maior que 20 caracteres"}), 422
    
    if not dados.get('especie'):
        return jsonify({"Mensagem": "Campo especie é obrigatorio"}), 400

    tipos_validos = ['cachorro', 'gato', 'passaro', 'peixe']
    if dados.get('especie') not in tipos_validos:
        return jsonify({"Mensagem": "Tipo de especie inválido!"}), 422

    if not dados.get('idade'):
        return jsonify({"Mensagem": "Campo idade é obrigatorio"}), 400
    
    idade = dados.get('idade')
    if not isinstance(idade, int):
        return jsonify({"erro": "'idade' deve ser um número inteiro"}), 422
    if not 0 <= idade <= 80:
        return jsonify({"erro": "Campo idade deve ser entre 0 e 80"}), 422
    
    animais = carregar_animais()


    animais.append(dados)

    salvar_animais(animais)

    resposta = {
        "Mensagem": "Animal cadastrado com sucesso!"
    }

    return jsonify(resposta), 201

@app.post('/usuarios')
def post_usuario():
    dados_usuario = request.json

    if not dados_usuario.get('nome'):
        return jsonify({"Mensagem": "Campo nome é obrigatorio"}), 400
    
    nome_usuario = dados_usuario.get('nome')
    if not nome_usuario.isalpha():
        return jsonify({"erro": "Campo nome deve conter apenas letras"}), 422
    if not len(nome_usuario) >= 2:
        return jsonify({"erro": "O nome não pode ser menor ou igual a 1"}), 422
    if not len(nome_usuario) <= 154:
        return jsonify({"erro": "O nome não pode ser maior que 154 caracteres"}), 422
    
    if not dados_usuario.get('cpf'):
        return jsonify({"Mensagem": "Campo cpf é obrigatorio"}), 400
    
    cpf = dados_usuario.get('cpf')
    if not cpf.isnumeric():
        return jsonify({"erro": "Campo cpf deve conter apenas números"}), 422
    if not len(cpf) == 11:
        return jsonify({"erro": "Campo cpf deve conter 11 digítos"}), 422
    
    if not dados_usuario.get('telefone'):
        return jsonify({"Mensagem": "Campo telefone é obrigatorio"}), 400
    
    telefone = dados_usuario.get('telefone')
    if not telefone.isnumeric():
        return jsonify({"erro": "Campo telefone deve conter apenas números"}), 422
    if not len(telefone) == 11:
        return jsonify({"erro": "Campo telefone deve conter 11 digítos"}), 422
    
    if not dados_usuario.get('email'):
        return jsonify({"Mensagem": "Campo email é obrigatorio"}), 400
    
    email = dados_usuario.get('email')
    if not len(email) <= 256:
        return jsonify({"erro": "Campo email não pode ser maior que 256 caracteres"}), 422
    if len(email) < 5:
        return jsonify({"erro": "Campo email não pode ser menor que 5 caracteres"}), 422
    
    if not dados_usuario.get('endereco'):
        return jsonify({"Mensagem": "Campo endereço é obrigatorio"}), 400
    
    endereco = dados_usuario.get('endereco')
    if not len(endereco) <= 60:
        return jsonify({"erro": "Campo endereço não pode ser maior que 60 caracteres"}), 422
    if len(endereco) < 5:
        return jsonify({"erro": "Campo endereço não pode ser menor que 5 caracteres"}), 422

    usuario = carregar_usuarios()

    usuario.append(dados_usuario)

    salvar_usuarios(usuario)

    resposta = {
        "Mensagem": "Usuário cadastrado com sucesso!"
    }

    return jsonify(resposta), 201

def carregar_json(arquivo):
    with open(arquivo, 'r') as f:
        return json.load(f)

@app.get('/abrigos')
def get_abrigos():
    return jsonify(carregar_json('abrigos.json'))

@app.get('/categorias')
def get_categorias():
    return jsonify(["cachorro", "gato", "passaro", "peixe"])

@app.put('/animais/<int:id>')
def atualizar_animal(id):
    animais = carregar_animais()
    dados = request.json
    for usuario in animais:
        if usuario.get('id') == id:
            usuario.update(dados)
            salvar_animais(animais)
            return jsonify({"Mensagem": "Ok"}), 200
    return jsonify({"Mensagem": "Não encontrado"}), 404

@app.delete('/animais/<int:id>')
def deletar_animal(id):
    animais = carregar_animais()

    for usuario in animais:
        if usuario.get('id') == id:
            animais.remove(usuario)
            salvar_animais(animais)
            return jsonify({"Mensagem": "Deletado"}), 204

    return jsonify({"Mensagem": "Não encontrado"}), 404
    
@app.put('/usuarios/<int:id>')
def atualizar_usuario(id):
    usuarios = carregar_usuarios()
    dados = request.json

    for usuario in usuarios:
        if usuario.get('id') == id:
            usuario.update(dados)
            salvar_usuarios(usuarios)
            return jsonify({"Mensagem": "Ok"}), 200

    return jsonify({"Mensagem": "Não encontrado"}), 404

@app.delete('/usuarios/<int:id>')
def deletar_usuario(id):
    usuarios = carregar_usuarios()

    for usuario in usuarios:
        if usuario.get('id') == id:
            usuarios.remove(usuario)
            salvar_usuarios(usuarios)
            return jsonify({"Mensagem": "Deletado"}), 204

    return jsonify({"Mensagem": "Não encontrado"}), 404
    
@app.put('/abrigos/<int:id>')
def atualizar_abrigo(id):
    abrigos = carregar_abrigos()
    dados = request.json

    for abrigo in abrigos:
        if abrigo.get('id') == id:
            abrigo.update(dados)
            salvar_abrigos(abrigos)
            return jsonify({"Mensagem": "Ok"}), 200

    return jsonify({"Mensagem": "Não encontrado"}), 404

@app.delete('/abrigos/<int:id>')
def deletar_abrigo(id):
    abrigos = carregar_abrigos()

    for abrigo in abrigos:
        if abrigo.get('id') == id:
            abrigos.remove(abrigo)
            salvar_abrigos(abrigos)
            return jsonify({"Mensagem": "Deletado"}), 204
        
    return jsonify({"Mensagem": "Não encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)