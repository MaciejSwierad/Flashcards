import sqlite3

with sqlite3.connect("FLASHCARDSAPP.db") as connection:

    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS users
      (id INTEGER PRIMARY KEY,
      username TEXT UNIQUE NOT NULL,
      password TEXT NOT NULL)
      """)

    cursor.execute("""CREATE TABLE IF NOT EXISTS flashcards(
      id INTEGER PRIMARY KEY,
      content TEXT NOT NULL,
      answer TEXT NOT NULL,
      category TEXT NOT NULL,
      level INTEGER NOT NULL,
      user_id INT NOT NULL)
      """)

    cursor.execute('INSERT INTO users VALUES(1, "admin", "admin")')
    cursor.execute('INSERT INTO flashcards VALUES (1, "kot", "cat", "AAA", 1, 1)')

# import sqlite3
#
# import click
# from flask import current_app, g
# from flask.cli import with_appcontext
#
#
# def get_db():
#     if 'db' not in g:
#         g.db = sqlite3.connect(
#             current_app.config['DATABASE'],
#             detect_types=sqlite3.PARSE_DECLTYPES
#         )
#         g.db.row_factory = sqlite3.Row
#
#     return g.db
#
#
# def close_db(e=None):
#     db = g.pop('db', None)
#
#     if db is not None:
#         db.close()
#
#
# def init_db():
#     db = get_db()
#
#     with current_app.open_resource('schema.sql') as f:
#         db.executescript(f.read().decode('utf8'))
#
#
# @click.command('init-db')
# @with_appcontext
# def init_db_command():
#     init_db()
#     click.echo('Initialized the database.')
#
#
# def init_app(app):
#     app.teardown_appcontext(close_db)
#     app.cli.add_command(init_db_command)
