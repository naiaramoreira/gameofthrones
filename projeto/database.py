import sqlite3
from projeto.models import Lord, Casa, PlayedBy, TvSeries, PovBook, Allegiance, Alias, Book, Title

def conectar():
    return sqlite3.connect('casas.db')

def criar_tabelas():
    try:
        conn = sqlite3.connect('casas.db')
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS houses
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           name TEXT,
                           region TEXT,                       
                           founding_year INTEGER,
                           lord_id INTEGER,
                           FOREIGN KEY (lord_id) REFERENCES lords(id))''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS lords
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           name TEXT,
                           gender TEXT,
                           culture TEXT,
                           born TEXT,
                           died TEXT,
                           father TEXT,
                           mother TEXT,
                           spouse TEXT)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS aliases
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           lord_id INTEGER,
                           alias TEXT,
                           FOREIGN KEY (lord_id) REFERENCES lords(id))''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS books
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           lord_id INTEGER,
                           book_url TEXT,
                           FOREIGN KEY (lord_id) REFERENCES lords(id))''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS allegiances
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           lord_id INTEGER,
                           house_url TEXT,
                           FOREIGN KEY (lord_id) REFERENCES lords(id))''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS pov_books
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           lord_id INTEGER,
                           book_url TEXT,
                           FOREIGN KEY (lord_id) REFERENCES lords(id))''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS tv_series
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           lord_id INTEGER,
                           serie_name TEXT,
                           FOREIGN KEY (lord_id) REFERENCES lords(id))''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS playeds_by
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           lord_id INTEGER,
                           actor_name TEXT,
                           FOREIGN KEY (lord_id) REFERENCES lords(id))''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS titles
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           lord_id INTEGER,
                           title TEXT,
                           FOREIGN KEY (lord_id) REFERENCES lords(id))''')

        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def adicionar_casa(casa):
    try:
        conn = sqlite3.connect('casas.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO houses (name, region, founding_year, lord_id)
                          VALUES (?, ?, ?, ?)''', (casa.name, casa.region, casa.founding_year, casa.lord_id))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def adicionar_lord(lord):
    try:
        conn = sqlite3.connect('casas.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO lords (name, gender, culture, born, died, father, mother, spouse)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                       (lord.name, lord.gender, lord.culture, lord.born, lord.died, lord.father, lord.mother, lord.spouse))
        conn.commit()
        conn.close()
        lord.id = buscar_ultimo_registro_lord()

        return lord
    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def adicionar_alias(alias):
    try:
        conn = sqlite3.connect('casas.db')
        cursor = conn.cursor()
        cursor.executemany('''INSERT INTO aliases (lord_id, alias)
                          VALUES (?, ?)''', [(int(al.lord_id), al.alias) for al in alias])
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def adicionar_book(books):
    try:
        conn = sqlite3.connect('casas.db')
        cursor = conn.cursor()
        cursor.executemany('''INSERT INTO books (lord_id, book_url)
                          VALUES (?, ?)''', [(int(boo.lord_id), boo.book_url) for boo in books])
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def adicionar_allegiance(allegiances):
    try:
        conn = sqlite3.connect('casas.db')
        cursor = conn.cursor()
        cursor.executemany('''INSERT INTO allegiances (lord_id, house_url)
                          VALUES (?, ?)''', [(int(alle.lord_id), alle.house_url) for alle in allegiances])
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def adicionar_pov_book(pov_books):
    try:
        conn = sqlite3.connect('casas.db')
        cursor = conn.cursor()
        cursor.executemany('''INSERT INTO pov_books (lord_id, book_url)
                          VALUES (?, ?)''', [(int(pv.lord_id), pv.book_url) for pv in pov_books])
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def adicionar_played_by(playeds_by):
    try:
        conn = sqlite3.connect('casas.db')
        cursor = conn.cursor()
        cursor.executemany('''INSERT INTO playeds_by (lord_id, actor_name)
                          VALUES (?, ?)''', [(int(pb.lord_id), pb.actor_name) for pb in playeds_by])
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def adicionar_tv_series(tv_series):
    try:
        conn = sqlite3.connect('casas.db')
        cursor = conn.cursor()
        cursor.executemany('''INSERT INTO tv_series (lord_id, serie_name)
                          VALUES (?, ?)''', [(int(tv.lord_id), tv.serie_name) for tv in tv_series])
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def adicionar_titles(titles):
    try:
        conn = sqlite3.connect('casas.db')
        cursor = conn.cursor()
        cursor.executemany('''INSERT INTO titles (lord_id, title)
                          VALUES (?, ?)''', [(int(ti.lord_id), ti.title) for ti in titles])
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def listar_casas():
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('''
                        SELECT c.id, c.name, c.region, c.founding_year,
                               l.name, l.gender, l.born, l.culture, 
                               l.died, l.father, l.mother, l.spouse, l.id
                          FROM houses c INNER JOIN lords l ON c.lord_id = l.id;
        ''')
        casas = []
        resultado = cursor.fetchall()
        if resultado:
            for linha in resultado:
                lord = Lord(linha[4], linha[5], linha[6], linha[7], linha[8], linha[9], linha[10], linha[11], linha[12])
                casa = Casa(linha[1], lord, linha[2], linha[3], linha[0])
                dicionario = {'lord': lord, 'casa': casa}
                casas.append(dicionario)
            conexao.close()
            return casas
        conexao.close()
        return "Sem informações de casas!!!"

    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def buscar_casa_por_nome(nome):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('''
                        SELECT c.id, c.name, c.region, c.founding_year,
                               l.name, l.gender, l.born, l.culture, 
                               l.died, l.father, l.mother, l.spouse, l.id
                          FROM houses c INNER JOIN lords l ON c.lord_id = l.id
                         WHERE c.name like ?''', (str('%'+nome+'%'),)
        )
        casas = []
        resultado = cursor.fetchall()
        if resultado:
            for linha in resultado:
                lord = Lord(linha[4], linha[5], linha[6], linha[7], linha[8], linha[9], linha[10], linha[11], linha[12])
                casa = Casa(linha[1], lord, linha[2], linha[3], linha[0])
                dicionario = {'lord': lord, 'casa': casa}
                casas.append(dicionario)
            conexao.close()
            return casas
        conexao.close()
        return
    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def buscar_casa_por_id(id):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('''
                        SELECT c.id, c.name, c.region, c.founding_year,
                               l.name, l.gender, l.born, l.culture, 
                               l.died, l.father, l.mother, l.spouse, l.id
                          FROM houses c INNER JOIN lords l ON c.lord_id = l.id
                         WHERE c.id = ?''', (id,))
        casas = []
        resultado = cursor.fetchall()
        if resultado:
            for linha in resultado:
                lord = Lord(linha[4], linha[5], linha[6], linha[7], linha[8], linha[9], linha[10], linha[11], linha[12])
                casa = Casa(linha[1], lord, linha[2], linha[3], linha[0])
                dicionario = {'lord': lord, 'casa': casa}
                casas.append(dicionario)
            conexao.close()
            return casas
        conexao.close()
        return
    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def buscar_lord_por_id(lord_id):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM lords WHERE id = ?', (lord_id,))
        linha = cursor.fetchone()
        if linha is not None:
            lord = Lord(linha[1], linha[2], linha[3], linha[4], linha[5], linha[6], linha[7], linha[8], linha[0])
            conexao.close()
            return lord
        conexao.close()
        return None
    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def buscar_ultimo_registro_lord():
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('SELECT max(id) as id FROM lords;')
        linha = cursor.fetchone()
        if linha is not None:
            conexao.close()
            return linha[0]

        conexao.close()
        return None
    except sqlite3.Error as e:
        print(f"Erro: {e}")

def buscar_aliases_por_lord_id(lord_id):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM aliases WHERE lord_id = ?', (lord_id,))
        aliases = []
        resultado = cursor.fetchall()
        if resultado:
            for linha in resultado:
                alias = Alias(lord_id, linha[2], linha[0])
                aliases.append(alias)
            conexao.close()
            return aliases
        conexao.close()
        return ""
    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def buscar_books_por_lord_id(lord_id):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM books WHERE lord_id = ?', (lord_id,))
        books = []
        resultado = cursor.fetchall()
        if resultado:
            for linha in resultado:
                book = Book(lord_id, linha[2], linha[0])
                books.append(book)
            conexao.close()
            return books
        conexao.close()
        return ""
    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def buscar_allegiances_por_lord_id(lord_id):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM allegiances WHERE lord_id = ?', (lord_id,))
        allegiances = []
        resultado = cursor.fetchall()
        if resultado:
            for linha in resultado:
                allegiance = Allegiance(lord_id, linha[2], linha[0])
                allegiances.append(allegiance)
            conexao.close()
            return allegiances

        conexao.close()
        return ""
    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def buscar_pov_books_por_lord_id(lord_id):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM pov_books WHERE lord_id = ?', (lord_id,))
        pov_books = []
        resultado = cursor.fetchall()
        if resultado:
            for linha in resultado:
                pov_book = PovBook(lord_id, linha[2], linha[0])
                pov_books.append(pov_book)
            conexao.close()
            return pov_books

        conexao.close()
        return ""

    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def buscar_tv_series_by_por_lord_id(lord_id):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM tv_series WHERE lord_id = ?', (lord_id,))
        series_name = []
        resultado = cursor.fetchall()
        if resultado:
            for linha in resultado:
                serie_name = TvSeries(lord_id, linha[2], linha[0])
                series_name.append(serie_name)
            conexao.close()
            return series_name

        conexao.close()
        return ""

    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def buscar_played_by_por_lord_id(lord_id):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM playeds_by WHERE lord_id = ?', (lord_id,))
        played_by = []
        resultado = cursor.fetchall()
        if resultado:
            for linha in resultado:
                played_by_actor = PlayedBy(lord_id, linha[2], linha[0])
                played_by.append(played_by_actor)
            conexao.close()
            return played_by

        conexao.close()
        return ""
    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def buscar_title_por_lord_id(lord_id):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM titles WHERE lord_id = ?', (lord_id,))
        titles = []
        resultado = cursor.fetchall()
        if resultado:
            for linha in resultado:
                title = Title(lord_id, linha[2], linha[0])
                titles.append(title)
            conexao.close()
            return titles

        conexao.close()
        return ""
    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def alterar_casa(casa, casa_alteracao):
    try:
        conn = sqlite3.connect('casas.db')
        cursor = conn.cursor()
        cursor.execute('''UPDATE houses SET name = ?, region = ?, founding_year = ?, lord_id = ? WHERE id = ?''', (casa_alteracao.name, casa_alteracao.region, casa_alteracao.founding_year, casa_alteracao.lord_id, int(casa.id)))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def alterar_lord(id, lord):
    try:
        conn = sqlite3.connect('casas.db')
        cursor = conn.cursor()
        cursor.execute('''UPDATE lords SET name = ?, gender = ?, culture = ?, born = ?, died = ?, father = ?, mother = ?, spouse = ? WHERE id = ?''',
                       (lord.name, lord.gender, lord.culture, lord.born, lord.died, lord.father, lord.mother, lord.spouse, id))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def alterar_alias(lord_id, alias_alteracao):
    try:
        conn = sqlite3.connect('casas.db')
        cursor = conn.cursor()
        cursor.executemany('''UPDATE aliases SET alias = ? where lord_id = ?''', [(al.alias, int(lord_id)) for al in alias_alteracao])
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def alterar_book(lord_id, books):
    try:
        conn = sqlite3.connect('casas.db')
        cursor = conn.cursor()
        cursor.executemany('''UPDATE books SET book_url = ? where lord_id = ?''', [(boo.book_url, int(lord_id)) for boo in books])
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def alterar_allegiance(lord_id, allegiances):
    try:
        conn = sqlite3.connect('casas.db')
        cursor = conn.cursor()
        cursor.executemany('''UPDATE allegiances SET house_url = ? where lord_id = ?''', [(alle.house_url, lord_id) for alle in allegiances])
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def alterar_pov_book(lord_id, pov_books):
    try:
        conn = sqlite3.connect('casas.db')
        cursor = conn.cursor()
        cursor.executemany('''UPDATE pov_books SET book_url = ? where lord_id = ?''', [(pv.book_url, lord_id) for pv in pov_books])
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def alterar_played_by(lord_id, playeds_by):
    try:
        conn = sqlite3.connect('casas.db')
        cursor = conn.cursor()
        cursor.executemany('''UPDATE playeds_by SET actor_name = ? where lord_id''', [(pb.actor_name, lord_id) for pb in playeds_by])
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def alterar_tv_series(lord_id, tv_series):
    try:
        conn = sqlite3.connect('casas.db')
        cursor = conn.cursor()
        cursor.executemany('''UPDATE tv_series SET serie_name = ? where lord_id = ?''', [(tv.serie_name, lord_id) for tv in tv_series])
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def alterar_titles(lord_id, titles):
    try:
        conn = sqlite3.connect('casas.db')
        cursor = conn.cursor()
        cursor.executemany('''UPDATE titles SET titles = ? where lord_id = ?''', [(ti.title, lord_id) for ti in titles])
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def remover_casa(id):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('DELETE FROM houses WHERE id = ?', (id,))
        conexao.commit()
        conexao.close()
    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def remover_lord(id):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('DELETE FROM lords WHERE id = ?', (id,))
        conexao.commit()
        conexao.close()
    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def remover_aliases(lord_id):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('DELETE FROM aliases WHERE lord_id = ?', (lord_id,))
        conexao.commit()
        conexao.close()
    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def remover_allegiances(lord_id):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('DELETE FROM allegiances WHERE lord_id = ?', (lord_id,))
        conexao.commit()
        conexao.close()
    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def remover_pov_books(lord_id):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('DELETE FROM pov_books WHERE lord_id = ?', (lord_id,))
        conexao.commit()
        conexao.close()
    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def remover_playeds_by(lord_id):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('DELETE FROM playeds_by WHERE lord_id = ?', (lord_id,))
        conexao.commit()
        conexao.close()
    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def remover_tv_series(lord_id):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('DELETE FROM tv_series WHERE lord_id = ?', (lord_id,))
        conexao.commit()
        conexao.close()
    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None

def remover_titles(lord_id):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('DELETE FROM titles WHERE lord_id = ?', (lord_id,))
        conexao.commit()
        conexao.close()
    except sqlite3.Error as e:
        print(f"Erro: {e}")
        return None
