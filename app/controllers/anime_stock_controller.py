from http import HTTPStatus
from flask import request
from app.models.anime_model import Anime
from psycopg2.errors import UniqueViolation
from psycopg2 import sql
from .anime_stock_keyError_controller import KeyError_controller

Anime = Anime()

def create_anime():
    Anime.table_init()

    cur = Anime.open_connection()

    data = request.get_json()

    for key in data.keys():
        if key not in Anime.fieldnames:
            return KeyError_controller(data.keys()), HTTPStatus.UNPROCESSABLE_ENTITY


    data['anime'] = data['anime'].title()

    anime_values = tuple(data.values())

    query = """
        insert into animes
            (anime, released_date, seasons)
        values
            (%s, %s, %s)
        returning *
        """

    try:
        cur.execute(query, anime_values)
    except UniqueViolation:
        return {'error': f'anime {data["anime"]} ja existe'}, HTTPStatus.CONFLICT

    returned_anime = cur.fetchone()

    Anime.commit_and_close()

    return dict(zip(Anime.fieldnames, returned_anime)), HTTPStatus.CREATED

def get_animes():
    Anime.table_init()

    cur = Anime.open_connection()

    cur.execute("SELECT * FROM animes")
    db_data = cur.fetchall()

    processed_data = [dict(zip(Anime.fieldnames, row)) for row in db_data]

    Anime.commit_and_close()

    return {"data": processed_data}, HTTPStatus.OK

def get_anime_by_id(anime_id):
    Anime.table_init()
    cur = Anime.open_connection()
    query = """
        select * from animes
        where
            id = %s;
        """
    cur.execute(query, anime_id)
    anime_data= cur.fetchone()

    Anime.commit_and_close()

    try:
        return dict(zip(Anime.fieldnames, anime_data)), HTTPStatus.OK
    except TypeError:
        return {}, HTTPStatus.NOT_FOUND

def patch_anime(anime_id):
    Anime.table_init()
    
    cur = Anime.open_connection()

    data = request.get_json()

    for key in data.keys():
        if key not in Anime.fieldnames:
            return KeyError_controller(data.keys()), HTTPStatus.UNPROCESSABLE_ENTITY

    columns = [sql.Identifier(key) for key in data.keys()]
    values = [sql.Literal(value) for value in data.values()]
    sql_anime_id = sql.Literal(anime_id)

    query = sql.SQL(
        """
        update
            animes
        set
            ({columns}) = ROW({values})
        where
            id = {id}
        returning *;
        """
    ).format(
        id = sql_anime_id,
        columns = sql.SQL(',').join(columns),
        values = sql.SQL(',').join(values)
    )

    cur.execute(query)

    patched_anime = cur.fetchone()

    Anime.commit_and_close()

    try:
        return dict(zip(Anime.fieldnames, patched_anime)), HTTPStatus.OK
    except TypeError:
        return {}, HTTPStatus.NOT_FOUND

def delete_anime(anime_id):
    Anime.table_init()

    cur = Anime.open_connection()

    query = """
    delete from animes
    where
        id = %s
    returning *;
    """

    cur.execute(query, anime_id)

    deleted_anime = cur.fetchone()

    Anime.commit_and_close()

    print(deleted_anime)

    if deleted_anime == None:
        return {}, HTTPStatus.NOT_FOUND

    return "", HTTPStatus.OK


    return {'msg': f'anime de id {anime_id} deletado'}