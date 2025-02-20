from psycopg2 import connect
from resources.config import *
from loguru import logger
import random
import string


def db_connection():
    connection = None
    try:
        connection = connect(host=host, port=port, user=user, password=password, dbname=dbname)
    except Exception as ex:
        logger.error(str(ex))
    return connection


def generate_token() -> str:
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))


def account_exist(login: str) -> tuple:
    connection = db_connection()
    cur = connection.cursor()
    query = f'''SELECT 1 FROM "users" WHERE login = '{login}';'''
    cur.execute(query)
    query_result = cur.fetchone()
    return query_result


def log_in_account(login: str, password: str) -> tuple:
    connection = db_connection()
    cur = connection.cursor()
    query = f'''SELECT userid FROM "User" WHERE userlogin = '{login}' AND userpassword = '{password}';'''
    cur.execute(query)
    query_result = cur.fetchone()
    return query_result


def token_check(token) -> tuple:
    connection = db_connection()
    cur = connection.cursor()
    query = f'''SELECT 1 FROM "Session" WHERE token = '{token}';'''
    cur.execute(query)
    query_result = cur.fetchone()
    return query_result


def graph_check(graphid: int, owner_id: int) -> tuple:
    connection = db_connection()
    cur = connection.cursor()
    query = f'''Select 1 from "graphs" WHERE graphID = {graphid} and ownerID = {owner_id};'''
    cur.execute(query)
    query_result = cur.fetchone()
    return query_result



#функции для аккаунта
@logger.catch()
def create_account(login: str, password: str) -> bool:
    connection = db_connection()
    cur = connection.cursor()
    try:
        if account_exist(login) is None:
            query = f'''INSERT INTO "users" (login, password) VALUES ('{login}','{password}');'''
            cur.execute(query)
            return True
        else:
            return False
    except Exception as ex:
        logger.error(str(ex))
    finally:
        cur.close()
        connection.commit()
        connection.close()
    return True

@logger.catch()
def update_password(token: str, new_password: str) -> bool:
    query_result = None
    connection = db_connection()
    cur = connection.cursor()
    try:
        query_result = token_check(token)
        if query_result is not None:
            query = f'''UPDATE "users" set password = '{new_password}' WHERE userID = {query_result[0]};'''
            cur.execute(query)
            return True
        else:
            return False
    except Exception as ex:
        logger.error(str(ex))
    finally:
        cur.close()
        connection.commit()
        connection.close()


@logger.catch()
def delete_account(token: str) -> bool:
    query_result = None
    connection = db_connection()
    cur = connection.cursor()
    try:
        query_result = token_check(token)
        if query_result is not None:
            query = f'''DELETE FROM "users" WHERE userid = {query_result[0]};'''
            cur.execute(query)
            return True
        else:
            return False
    except Exception as ex:
        logger.error(str(ex))
    finally:
        cur.close()
        connection.commit()
        connection.close()


#функции для сессии
@logger.catch()
def create_session(login: str, password: str) -> str:
    connection = db_connection()
    cur = connection.cursor()
    query_result = None
    try:
        query_result = log_in_account(login,password)
        if query_result is not None:
            users_token = generate_token()
            id = query_result[0]
            query = f'''INSERT INTO "session" (token, userid) VALUES ('{users_token}', {id} );'''
            cur.execute(query)
            return users_token
        else:
            return ''
    except Exception as ex:
        logger.error(str(ex))
    finally:
        cur.close()
        connection.commit()
        connection.close()


@logger.catch()
def delete_session(token: str) -> bool:
    query_result = None
    connection = db_connection()
    cur = connection.cursor()
    try:
        query_result = token_check(token)
        if query_result is not None:
            query = f'''DELETE FROM "session" WHERE token = '{token}';'''
            cur.execute(query)
            return True
        else:
            return False
    except Exception as ex:
        logger.error(str(ex))
    finally:
        cur.close()
        connection.commit()
        connection.close()


@logger.catch()
def get_session_list(token: str) -> list[tuple]:
    query_result = None
    connection = db_connection()
    cur = connection.cursor()
    try:
        query_result = token_check(token)
        if query_result is not None:
            query = f'''Select sessionID,token FROM "session" WHERE userid = {query_result[0]}'''
            cur.execute(query)
            query_result = cur.fetchall()
            return query_result
        else:
            return []
    except Exception as ex:
        logger.error(str(ex))
    finally:
        cur.close()
        connection.commit()
        connection.close()


#функции для графов
@logger.catch()
def add_graph(token: str, name:str) -> int:
    query_result = None
    connection = db_connection()
    cur = connection.cursor()
    try:
        query_result = token_check(token)
        if query_result is not None:
            query = f'''Insert Into "graphs"(graphName, ownerID) Values ('{name}',{query_result[0]})
            RETURNING graphID;'''
            cur.execute(query)
            query_result = cur.fetchone()
            return query_result[0]
        else:
            return -1
    except Exception as ex:
        logger.error(str(ex))
    finally:
        cur.close()
        connection.commit()
        connection.close()


@logger.catch()
def delete_graph(token: str, id:int) -> bool:
    query_result = None
    connection = db_connection()
    cur = connection.cursor()
    try:
        query_result = token_check(token)
        if query_result is not None:
            query = f'''DELETE FROM "graphs" WHERE graphID = {id};'''
            cur.execute(query)
            return True
        else:
            return False
    except Exception as ex:
        logger.error(str(ex))
    finally:
        cur.close()
        connection.commit()
        connection.close()


@logger.catch()
def get_graph_list(token: str) -> list[tuple]:
    query_result = None
    connection = db_connection()
    cur = connection.cursor()
    try:
        query_result = token_check(token)
        if query_result is not None:
            query = f'''Select graphID,graphName FROM "graphs" WHERE ownerID = {query_result[0]}'''
            cur.execute(query)
            query_result = cur.fetchall()
            return query_result
        else:
            return []
    except Exception as ex:
        logger.error(str(ex))
    finally:
        cur.close()
        connection.commit()
        connection.close()


@logger.catch()
def update_graph(token: str,graph_id:int, new_name: str) -> bool:
    query_result = None
    connection = db_connection()
    cur = connection.cursor()
    try:
        query_result = token_check(token)
        if query_result is not None:
            query_result = graph_check(graph_id, query_result[0])
            if query_result[0] == 1:
                query = f'''UPDATE "graphs" SET graphName = '{new_name}' where graphID = {graph_id};'''
                cur.execute(query)
                return True
            else:
                return False
        else:
            return False
    except Exception as ex:
        logger.error(str(ex))
    finally:
        cur.close()
        connection.commit()
        connection.close()


#функции для точек
@logger.catch()
def add_node(token: str, id: int, x: float, y: float, name: str) -> int:
    query_result = None
    connection = db_connection()
    cur = connection.cursor()
    try:
        query_result = token_check(token)
        if query_result is not None:
            query_result = graph_check(id, query_result[0])
            if query_result == 1:
                query = f'''Insert Into "node"(graphID, x, y, name) Values ({query_result[0]}, {x}, {y}, '{name}') 
                RETURNING graphID;'''
                cur.execute(query)
                query_result = cur.fetchone()
                return query_result[0]
            else:
                return  -1
        else:
            return -1
    except Exception as ex:
        logger.error(str(ex))
    finally:
        cur.close()
        connection.commit()
        connection.close()


@logger.catch()
def delete_node(token: str, id:int) -> bool:
    query_result = None
    connection = db_connection()
    cur = connection.cursor()
    try:
        query_result = token_check(token)
        if query_result is not None:
            query = f'''DELETE FROM "node" WHERE nodeId = {id};'''
            cur.execute(query)
            return True
        else:
            return False
    except Exception as ex:
        logger.error(str(ex))
    finally:
        cur.close()
        connection.commit()
        connection.close()


@logger.catch()
def get_node_list(token: str, graphid: int) -> list[tuple]:
    query_result = None
    connection = db_connection()
    cur = connection.cursor()
    try:
        query_result = token_check(token)
        if query_result is not None:
            query_result = graph_check(graphid, query_result[0])
            if query_result[0] == 1:
                query = f'''Select nodeid, x, y, name FROM "node" WHERE graphID = {graphid}'''
                cur.execute(query)
                query_result = cur.fetchall()
                return query_result
            else:
                return []
        else:
            return []
    except Exception as ex:
        logger.error(str(ex))
    finally:
        cur.close()
        connection.commit()
        connection.close()


@logger.catch()
def update_node(token: str, graph_id: int, note_id: int, x: int, y: int, name: str) -> bool:
    query_result = None
    connection = db_connection()
    cur = connection.cursor()
    try:
        query_result = token_check(token)
        if query_result is not None:
            query_result = graph_check(graph_id, query_result[0])
            if query_result[0] == 1:
                query = f'''Select 1 from "node" WHERE noteId = {note_id};'''
                cur.execute(query)
                query_result = cur.fetchone()
                if query_result[0] == 1:
                    query = f'''UPDATE "node" SET name = '{name}',x={x},y={y} where noteid = {note_id};'''
                    cur.execute(query)
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    except Exception as ex:
        logger.error(str(ex))
    finally:
        cur.close()
        connection.commit()
        connection.close()


#функции для связей
@logger.catch()
def add_link(token: str, graph_id: int, source: int, target: int, value: float) -> int:
    query_result = None
    connection = db_connection()
    cur = connection.cursor()
    try:
        query_result = token_check(token)
        if query_result is not None:
            query_result = graph_check(graph_id, query_result[0])
            if query_result[0] == 1:
                query = f'''Insert Into "link"(source, target, value, graphid) Values ({source}, {target},{value}, {query_result[0]}) 
                RETURNING linkid;'''
                cur.execute(query)
                query_result = cur.fetchone()
                return query_result[0]
            else:
                return -1
        else:
            return -1
    except Exception as ex:
        logger.error(str(ex))
    finally:
        cur.close()
        connection.commit()
        connection.close()


@logger.catch()
def delete_link(token: str, id:int) -> bool:
    query_result = None
    connection = db_connection()
    cur = connection.cursor()
    try:
        query_result = token_check(token)
        if query_result is not None:
            query = f'''DELETE FROM "link" WHERE linkid = {id};'''
            cur.execute(query)
            return True
        else:
            return False
    except Exception as ex:
        logger.error(str(ex))
    finally:
        cur.close()
        connection.commit()
        connection.close()


@logger.catch()
def get_link_list(token: str, graphid: int) -> list[tuple]:
    query_result = None
    connection = db_connection()
    cur = connection.cursor()
    try:
        query_result = token_check(token)
        if query_result is not None:
            query_result = graph_check(graphid, query_result[0])
            if query_result[0] == 1:
                query = f'''Select linkid, source, target, value FROM "link" WHERE graphid = {graphid}'''
                cur.execute(query)
                query_result = cur.fetchall()
                return query_result
            else:
                return []
        else:
            return []
    except Exception as ex:
        logger.error(str(ex))
    finally:
        cur.close()
        connection.commit()
        connection.close()


@logger.catch()
def update_link(token: str, graph_id: int, link_id: int, value: str) -> bool:
    query_result = None
    connection = db_connection()
    cur = connection.cursor()
    try:
        query_result = token_check(token)
        if query_result is not None:
            query_result = graph_check(graph_id, query_result[0])
            if query_result[0] == 1:
                query = f'''Select 1 from "link" WHERE linkid = {link_id};'''
                cur.execute(query)
                query_result = cur.fetchone()
                if query_result[0] == 1:
                    query = f'''UPDATE "link" SET value = '{value}' where linkid = {link_id};'''
                    cur.execute(query)
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    except Exception as ex:
        logger.error(str(ex))
    finally:
        cur.close()
        connection.commit()
        connection.close()