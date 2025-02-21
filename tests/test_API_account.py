import pytest
from resources.functions import *


@pytest.mark.parametrize(
    "login, password, result",
    [
        ('testUser1', 'testUser1', True),
        ('testUser1', 'testUser2', True),
        ('testUser3', 'testUser3', True),
        ('312312', '3242341', True),
        ('lox', 'loxxxxxxxxxxxxxxxx', True),
    ]
)
def test_create_account(login:str, password:str, result: bool):
    connection = db_connection()
    cur = connection.cursor()
    rows_before = 0
    rows_after = 0
    try:
        query = f'''SELECT * FROM "users"'''
        cur.execute(query)
        rows_before = len(cur.fetchall())
        create_account(login,password)
        cur.execute(query)
        rows_after = len(cur.fetchall())
    except Exception as ex:
        print(ex)
    finally:
        query = f'''DELETE FROM "users" WHERE login = '{login}' and password = '{password}' '''
        cur.execute(query)
        cur.close()
        connection.commit()
        connection.close()
    assert (rows_before < rows_after) == result


@pytest.mark.parametrize(
    "login, password, result",
    [
        ('testUser1', 'testUser1', True),
        ('testUser2', 'testUser2', True),
        ('testUser3', 'testUser3', True),
        ('312312', '3242341', True),
        ('lox', 'loxxxxxxxxxxxxxxxx', True),
    ]
)
def test_create_session(login:str, password:str, result: bool):
    connection =  db_connection()
    cur = connection.cursor()
    rows_before = 0
    rows_after = 0
    try:
        query = f'''SELECT * FROM "session"'''
        cur.execute(query)
        rows_before = len(cur.fetchall())
        create_account(login,password)
        create_session(login,password)
        cur.execute(query)
        rows_after = len(cur.fetchall())
    except Exception as ex:
        print(ex)
    finally:
        query = f'''DELETE FROM "users" WHERE login = '{login}' and password = '{password}' '''
        cur.execute(query)
        cur.close()
        connection.commit()
        connection.close()
    assert (rows_before < rows_after) == result


@pytest.mark.parametrize(
    "login, password, result",
    [
        ('testUser1', 'testUser1', True),
        ('testUser2', 'testUser2', True),
        ('testUser3', 'testUser3', True),
        ('312312', '3242341', True),
        ('lox', 'loxxxxxxxxxxxxxxxx', True),
    ]
)
def test_delete_session(login:str, password:str, result: bool):
    connection =  db_connection()
    cur = connection.cursor()
    rows_before = 0
    rows_after = 0
    try:
        query = f'''SELECT * FROM "session"'''
        cur.execute(query)
        rows_before = len(cur.fetchall())
        create_account(login,password)
        delete_session(create_session(login,password))
        cur.execute(query)
        rows_after = len(cur.fetchall())
    except Exception as ex:
        print(ex)
    finally:
        query = f'''DELETE FROM "users" WHERE login = '{login}' and password = '{password}' '''
        cur.execute(query)
        cur.close()
        connection.commit()
        connection.close()
    assert (rows_before == rows_after) == result


@pytest.mark.parametrize(
    "login, password, newpassword, result",
    [
        ('testUser1', 'testUser1','testUser1Changed', True),
        ('testUser2', 'testUser2','testUser2Changed' , True),
        ('testUser3', 'testUser3','testUser3Changed' , True),
        ('312312', '3242341','2312413Changed', True),
        ('lox', 'loxxxxxxxxxxxxxxxx','loxxxxxxxxxxxChanged', True),
    ]
)
def test_update_password(login:str, password:str,newpassword:str, result: bool):
    connection =  db_connection()
    cur = connection.cursor()
    password_after = ''
    try:
        query = f'''SELECT password FROM "users" where login = '{login}' '''
        create_account(login,password)
        update_password(create_session(login,password), newpassword)
        cur.execute(query)
        password_after = cur.fetchone()[0]
        print(password_after)
    except Exception as ex:
        print(ex)
    finally:
        query = f'''DELETE FROM "users" WHERE login = '{login}' and password = '{newpassword}' '''
        cur.execute(query)
        cur.close()
        connection.commit()
        connection.close()
    assert (password_after == newpassword) == result


@pytest.mark.parametrize(
    "login, password, result",
    [
        ('testUser1', 'testUser1', True),
        ('testUser2', 'testUser2', True),
        ('testUser3', 'testUser3', True),
        ('312312', '3242341', True),
        ('lox', 'loxxxxxxxxxxxxxxxx', True),
    ]
)
def test_delete_account(login:str, password:str, result: bool):
    connection =  db_connection()
    cur = connection.cursor()
    rows_before = 0
    rows_after = 0
    try:
        query = f'''SELECT * FROM "users"'''
        cur.execute(query)
        rows_before = len(cur.fetchall())
        create_account(login, password)
        delete_account(create_session(login, password))
        cur.execute(query)
        rows_after = len(cur.fetchall())
    except Exception as ex:
        print(ex)
    finally:
        query = f'''DELETE FROM "users" WHERE login = '{login}' and password = '{password}' '''
        cur.execute(query)
        cur.close()
        connection.commit()
        connection.close()
    assert (rows_before == rows_after) == result