import pytest
from resources.functions import *


@pytest.mark.parametrize(
    "login, password, name, result",
    [
        ('testUser1', 'testUser1','testName1', True),
        ('testUser2', 'testUser2','testName2', True),
        ('testUser3', 'testUser3','testName3', True),
        ('423414534242342', '23423q4134141','4324242t45', True),
        ('lox', 'losasx','lox_note', True)
    ]
)
def test_add_graph(login:str, password:str, result: bool, title:str, text:str):
    connection =  db_connection()
    cur = connection.cursor()
    rows_before = 0
    rows_after = 0
    try:
        query = f'''SELECT * FROM "Note"'''
        cur.execute(query)
        rows_before = len(cur.fetchall())
        create_account(login,password)
        add_note(create_session(login,password),title,text)
        cur.execute(query)
        rows_after = len(cur.fetchall())
        print(rows_after)
    except Exception as ex:
        print(ex)
    finally:
        query = f'''DELETE FROM "User" WHERE userlogin = '{login}' and userpassword = '{password}' '''
        cur.execute(query)
        cur.close()
        connection.commit()
        connection.close()
    assert (rows_before < rows_after) == result


@pytest.mark.parametrize(
    "login, password, title, text, result",
    [
        ('testUser1', 'testUser1','testTitle1','testText1', True),
        ('testUser2', 'testUser2','testTitle2','testText2', True),
        ('testUser3', 'testUser3','testTitle3','testText3', True),
        ('423414534242342', '23423q4134141','4324242t45','234231q', True),
        ('lox', 'losasx','lox_note','note_lox', True)
    ]
)
def test_delete_notes(login:str, password:str, result: bool, title:str, text:str):
    connection =  db_connection()
    cur = connection.cursor()
    rows_before = 0
    rows_after = 0
    try:
        query = f'''SELECT * FROM "Note"'''
        cur.execute(query)
        rows_before = len(cur.fetchall())
        create_account(login,password)
        token = create_session(login, password)
        delete_note(token,add_note(token,title,text))
        cur.execute(query)
        rows_after = len(cur.fetchall())
    except Exception as ex:
        print(ex)
    finally:
        query = f'''DELETE FROM "User" WHERE userlogin = '{login}' and userpassword = '{password}' '''
        cur.execute(query)
        cur.close()
        connection.commit()
        connection.close()
    assert (rows_before == rows_after) == result


@pytest.mark.parametrize(
    "login, password, notes, result",
    [
        ('testUser1', 'testUser1',[['testTitle1','testText1'],
                                   ['testTitle2','testText2'],
                                   ['testTitle3','testText3'],
                                   ['testTitle4','testText4'],
                                   ['testTitle5','testText5']], True),
        ('testUser2', 'testUser2',[['1','1'],
                                   ['2','2'],
                                   ['3','3'],
                                   ['4','4'],
                                   ['5','5']], True),
        ('testUser3', 'testUser3',[['kmsdlfmsd1','dsklfklsdkl1'],
                                   ['oreworpw2','lkslfkdskl2'],
                                   ['ljdsfkkl3','i32rkekdls3'],
                                   ['oiewpoirpiow4','mnclaoioe4'],
                                   ['njhdskfhshd5','oerifkdjsljkds5']], True),
        ('423414534242342', '23423q4134141',[['TopNote1','TopNote1'],
                                   ['TopNote2','TopNote2'],
                                   ['TopNote3','TopNote3'],
                                   ['TopNote4','TopNote4'],
                                   ['TopNote5','TopNote5']], True),
        ('lox', 'losasx',[['kmsdlfmsd1','dsklfklsdkl1'],
                                   ['oreworpw2','lkslfkdskl2'],
                                   ['ljdsfkkl3','i32rkekdls3'],
                                   ['oiewpoirpiow4','mnclaoioe4'],
                                   ['njhdskfhshd5','oerifkdjsljkds5']], True)
    ]
)
def test_get_all_notes(login:str, password:str, result: bool, notes:list):
    connection =  db_connection()
    cur = connection.cursor()
    all_rows_actual = 0
    all_rows_exspected = 5
    try:
        create_account(login,password)
        token = create_session(login, password)
        for item in notes:
            add_note(token,item[0],item[1])
        all_rows_actual = len(get_notes(token))
    except Exception as ex:
        print(ex)
    finally:
        query = f'''DELETE FROM "User" WHERE userlogin = '{login}' and userpassword = '{password}' '''
        cur.execute(query)
        cur.close()
        connection.commit()
        connection.close()
    assert (all_rows_exspected == all_rows_actual) == result


@pytest.mark.parametrize(
    "login, password, title,text,new_title,new_text,result",
    [
        ('testUser1', 'testUser1', 'testTitle1', 'testText1', 'testTitle1Changed', 'testText1Changed', True),
        ('testUser2', 'testUser2', 'testTitle2', 'testText2', 'testTitle2Changed', 'testText2Changed', True),
        ('testUser3', 'testUser3', 'testTitle3', 'testText3', 'testTitle3Changed', 'testText3Changed', True),
        ('testUser4', 'testUser4', 'testTitle4', 'testText4', 'testTitle4Changed', 'testText4Changed', True),
        ('testUser5', 'testUser5', 'testTitle5', 'testText5', 'testTitle5Changed', 'testText5Changed', True),

    ]
)
def test_update_note(login:str, password:str,title:str,text:str,new_title:str,new_text:str , result: bool):
    connection =  db_connection()
    cur = connection.cursor()
    title_after = ''
    try:
        create_account(login, password)
        token = create_session(login, password)
        id = add_note(token,title,text)
        update_note(token,id,new_title,new_text)
        query = f'''SELECT notetitle FROM "Note" where noteid = '{id}' '''
        cur.execute(query)
        title_after = cur.fetchone()[0]
    except Exception as ex:
        print(ex)
    finally:
        query = f'''DELETE FROM "User" WHERE userlogin = '{login}' and userpassword = '{password}' '''
        cur.execute(query)
        cur.close()
        connection.commit()
        connection.close()
    assert (title_after == new_title) == result


@pytest.mark.parametrize(
    "login, password, title, text, result",
    [
        ('testUser1', 'testUser1','testTitle1','testText1', True),
        ('testUser2', 'testUser2','testTitle2','testText2', True),
        ('testUser3', 'testUser3','testTitle3','testText3', True),
        ('423414534242342', '23423q4134141','4324242t45','234231q', True),
        ('lox', 'losasx','lox_note','note_lox', True)
    ]
)
def test_get_note_content(login:str, password:str,title:str, text:str, result: bool):
    connection =  db_connection()
    cur = connection.cursor()
    result_text = ''
    try:
        create_account(login, password)
        token = create_session(login, password)
        id = add_note(token, title, text)
        result_text = get_note_content(token,id)
    except Exception as ex:
        print(ex)
    finally:
        query = f'''DELETE FROM "User" WHERE userlogin = '{login}' and userpassword = '{password}' '''
        cur.execute(query)
        cur.close()
        connection.commit()
        connection.close()
    assert (result_text == text) == result