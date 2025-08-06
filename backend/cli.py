"""
Flask CLI commands.

Este módulo define comandos CLI customizados para a aplicação Flask.
"""

import click
from flask.cli import with_appcontext

from app.extensions import db
from seed_data import init_database, seed_database


@click.command()
@with_appcontext
def init_db():
    """Inicializar banco de dados."""
    click.echo('Inicializando banco de dados...')
    init_database()
    click.echo('Banco de dados inicializado!')


@click.command()
@with_appcontext
def seed_db():
    """Fazer seed do banco de dados."""
    click.echo('Executando seed do banco de dados...')
    seed_database()
    click.echo('Seed concluído!')


@click.command()
@with_appcontext
def reset_db():
    """Resetar banco de dados."""
    click.echo('Resetando banco de dados...')
    db.drop_all()
    init_database()
    click.echo('Banco de dados resetado!')


def register_commands(app):
    """Registrar comandos CLI na aplicação."""
    app.cli.add_command(init_db)
    app.cli.add_command(seed_db)
    app.cli.add_command(reset_db)
