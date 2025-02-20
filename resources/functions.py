from psycopg2 import connect
from resources.config import *
from loguru import  logger
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
            query = f'''Select 1 from "graphs" WHERE graphID = {graph_id} and ownerID = {query_result[0]};'''
            cur.execute(query)
            query_result = cur.fetchone()
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
            query = f'''Select 1 from "graphs" WHERE graphID = {graph_id} and ownerID = {query_result[0]};'''
            cur.execute(query)
            query_result = cur.fetchone()
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