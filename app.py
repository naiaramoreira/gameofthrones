from flask import Flask, jsonify, request
from projeto.models import Casa, Lord, Alias, Book, Allegiance, PovBook, PlayedBy, TvSeries, Title
import projeto.database as database

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Game Of Thrones!'

@app.route('/casas', methods=['POST'])
def adicionar_casa():
    dados = request.get_json()

    lord = Lord(
        dados['lord_name'],
        dados['gender'],
        dados['culture'],
        dados['born'],
        dados['died'],
        dados['father'],
        dados['mother'],
        dados['spouse'],
    )
    lord_ = database.adicionar_lord(lord)

    aliases = []
    for item in dados['aliases']:
        alias = Alias(lord_.id, item)
        aliases.append(alias)
    database.adicionar_alias(aliases)

    books = []
    for item in dados['books']:
        book = Book(lord_.id, item)
        books.append(book)
    database.adicionar_book(books)

    allegiances = []
    for item in dados['allegiances']:
        allegiance = Allegiance(lord_.id, item)
        allegiances.append(allegiance)
    database.adicionar_allegiance(allegiances)

    pov_books = []
    for item in dados['povBooks']:
        pov_book = PovBook(lord_.id, item)
        pov_books.append(pov_book)
    database.adicionar_pov_book(pov_books)

    tv_series = []
    for item in dados['tvSeries']:
        tv_serie = TvSeries(lord_.id, item)
        tv_series.append(tv_serie)
    database.adicionar_tv_series(tv_series)

    playeds_by = []
    for item in dados['playedBy']:
        played_by = PlayedBy(lord_.id, item)
        playeds_by.append(played_by)
    database.adicionar_played_by(playeds_by)

    titles = []
    for item in dados['titles']:
        title = Title(lord_.id, item)
        titles.append(title)
    database.adicionar_titles(titles)

    casa = Casa(dados['house_name'], lord_.id, dados['region'], dados['founding_year'])
    database.adicionar_casa(casa)
    return jsonify({'mensagem': 'Casa adicionada com sucesso'})

@app.route('/casas/<nome>', methods=['GET'])
def buscar_casa_por_nome(nome):
    casas = database.buscar_casa_por_nome(nome)
    casas_json = []
    if casas is not None:
        for item in casas:
            casas_json.append({
                "house_name": item['casa'].name,
                "name": item['lord'].name,
                "gender": item['lord'].gender,
                "culture": item['lord'].culture,
                "born": item['lord'].born,
                "died": item['lord'].died,
                "titles": [ti.title for ti in database.buscar_title_por_lord_id(item['lord'].id)],
                "aliases": [al.alias for al in database.buscar_aliases_por_lord_id(item['lord'].id)],
                "father": item['lord'].father,
                "mother": item['lord'].mother,
                "spouse": item['lord'].spouse,
                "allegiances": [al.house_url for al in database.buscar_allegiances_por_lord_id(item['lord'].id)],
                "books": [al.book_url for al in database.buscar_books_por_lord_id(item['lord'].id)],
                "povBooks": [al.book_url for al in database.buscar_pov_books_por_lord_id(item['lord'].id)],
                "tvSeries": [ts.serie_name for ts in database.buscar_tv_series_by_por_lord_id(item['lord'].id)],
                "playedBy": [pb.actor_name for pb in database.buscar_played_by_por_lord_id(item['lord'].id)]
            })
        return jsonify(casas_json)
    return jsonify({'mensagem': 'Casa(s) não encontrada(s)'})

@app.route('/casas/<int:id>', methods=['GET'])
def buscar_casa_por_id(id):
    casas = database.buscar_casa_por_id(id)
    resposta = {}
    if casas is not None:
        for casa in casas:
            resposta ={
                "house_name": casa['casa'].name,
                "name": casa['lord'].name,
                "gender": casa['lord'].gender,
                "culture": casa['lord'].culture,
                "born": casa['lord'].born,
                "died": casa['lord'].died,
                "titles": [ti.title for ti in database.buscar_title_por_lord_id(casa['lord'].id)],
                "aliases": [al.alias for al in database.buscar_aliases_por_lord_id(casa['lord'].id)],
                "father": casa['lord'].father,
                "mother": casa['lord'].mother,
                "spouse": casa['lord'].spouse,
                "allegiances": [al.house_url for al in database.buscar_allegiances_por_lord_id(casa['lord'].id)],
                "books": [al.book_url for al in database.buscar_books_por_lord_id(casa['lord'].id)],
                "povBooks": [al.book_url for al in database.buscar_pov_books_por_lord_id(casa['lord'].id)],
                "tvSeries": [ts.serie_name for ts in database.buscar_tv_series_by_por_lord_id(casa['lord'].id)],
                "playedBy": [pb.actor_name for pb in database.buscar_played_by_por_lord_id(casa['lord'].id)]
            }
        return jsonify(resposta)
    return jsonify({'mensagem': 'Casa não encontrada'})

@app.route('/casas/<int:id>', methods=['PUT'])
def alterar_casa_id(id):
    dados = request.get_json()

    casa = database.buscar_casa_por_id(id)
    casa_alteracao = Casa(dados['house_name'], casa[0]['lord'].id, dados['region'], dados['founding_year'])
    database.alterar_casa(casa[0]['casa'], casa_alteracao)

    lord_alteracao = Lord(dados['lord_name'], dados['gender'], dados['culture'], dados['born'], dados['died'], dados['father'], dados['mother'], dados['spouse'])
    database.alterar_lord(casa[0]['lord'].id, lord_alteracao)

    alias_alteracao = []
    for item in dados['aliases']:
        alias = Alias(casa[0]['lord'].id, item)
        alias_alteracao.append(alias)
    database.alterar_alias(casa[0]['lord'].id, alias_alteracao)

    allegiances = []
    for item in dados['allegiances']:
        allegiance = Allegiance(casa[0]['lord'].id, item)
        allegiances.append(allegiance)
    database.alterar_allegiance(casa[0]['lord'].id, allegiances)

    books = []
    for item in dados['books']:
        book = Book(casa[0]['lord'].id, item)
        books.append(book)
    database.alterar_book(casa[0]['lord'].id, books)

    playeds_by = []
    for item in dados['playedBy']:
        played_by = PlayedBy(casa[0]['lord'].id, item)
        playeds_by.append(played_by)
    database.alterar_played_by(casa[0]['lord'].id, playeds_by)

    pov_books = []
    for item in dados['povBooks']:
        pov_book = PovBook(casa[0]['lord'].id, item)
        pov_books.append(pov_book)
    database.alterar_pov_book(casa[0]['lord'].id, pov_books)

    titles = []
    for item in dados['titles']:
        title = Title(casa[0]['lord'].id, item)
        titles.append(title)
    database.alterar_titles(casa[0]['lord'].id, titles)

    tv_series = []
    for item in dados['tvSeries']:
        tv_serie = TvSeries(casa[0]['lord'].id, item)
        tv_series.append(tv_serie)
    database.alterar_tv_series(casa[0]['lord'].id, tv_series)

    return 'Alteração realizada com sucesso!'

@app.route('/casas', methods=['GET'])
def listar_casas():
    casas = database.listar_casas()
    casas_json = []
    if casas is not None:
        for item in casas:
            casas_json.append({
                "house_name": item['casa'].name,
                "name": item['lord'].name,
                "gender": item['lord'].gender,
                "culture": item['lord'].culture,
                "born": item['lord'].born,
                "died": item['lord'].died,
                "titles": [ti.title for ti in database.buscar_title_por_lord_id(item['lord'].id)],
                "aliases": [al.alias for al in database.buscar_aliases_por_lord_id(item['lord'].id)],
                "father": item['lord'].father,
                "mother": item['lord'].mother,
                "spouse": item['lord'].spouse,
                "allegiances": [al.house_url for al in database.buscar_allegiances_por_lord_id(item['lord'].id)],
                "books": [al.book_url for al in database.buscar_books_por_lord_id(item['lord'].id)],
                "povBooks": [al.book_url for al in database.buscar_pov_books_por_lord_id(item['lord'].id)],
                "tvSeries": [ts.serie_name for ts in database.buscar_tv_series_by_por_lord_id(item['lord'].id)],
                "playedBy": [pb.actor_name for pb in database.buscar_played_by_por_lord_id(item['lord'].id)]
            })
        return jsonify(casas_json)
    return jsonify({'mensagem': 'Não existe informações na base!'})

@app.route('/casas/<int:id>', methods=['DELETE'])
def remover_casa(id):

    database.remover_casa(id)

    return jsonify({'mensagem': 'Casa removida com sucesso'})


@app.route('/lord/<int:id>', methods=['DELETE'])
def remover_lord(id):

    lord = database.buscar_lord_por_id(id)

    database.remover_aliases(lord.id)
    database.remover_allegiances(lord.id)
    database.remover_tv_series(lord.id)
    database.remover_playeds_by(lord.id)
    database.remover_pov_books(lord.id)
    database.remover_titles(lord.id)
    database.remover_lord(id)

    return jsonify({'mensagem': 'Lord removido com sucesso'})

if __name__ == '__main__':
    database.criar_tabelas()
    app.run(host="0.0.0.0", port=5000)
