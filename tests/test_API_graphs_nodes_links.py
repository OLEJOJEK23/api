import pytest
from resources.functions import *


# graph tests
@pytest.mark.parametrize(
    "login, password, name, result",
    [
        ('testUser1', 'testUser1', 'testName1', True),
        ('testUser2', 'testUser2', 'testName2', True),
        ('testUser3', 'testUser3', 'testName3', True),
        ('423414534242342', '23423q4134141', '4324242t45', True),
        ('lox', 'losasx', 'lox_note', True)
    ]
)
def test_add_graph(login: str, password: str, name: str, result: bool):
    connection = db_connection()
    cur = connection.cursor()
    rows_before = 0
    rows_after = 0
    try:
        query = f'''SELECT * FROM "graph"'''
        cur.execute(query)
        rows_before = len(cur.fetchall())
        create_account(login, password)
        add_graph(create_session(login, password), name)
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
    "login, password, name, result",
    [
        ('testUser1', 'testUser1', 'testName1', True),
        ('testUser2', 'testUser2', 'testName2', True),
        ('testUser3', 'testUser3', 'testName3', True),
        ('423414534242342', '23423q4134141', 'testName4', True),
        ('lox', 'losasx', 'testName5', True)
    ]
)
def test_delete_graph(login: str, password: str, name: str, result: bool):
    connection = db_connection()
    cur = connection.cursor()
    rows_before = 0
    rows_after = 0
    try:
        query = f'''SELECT * FROM "graph"'''
        cur.execute(query)
        rows_before = len(cur.fetchall())
        create_account(login, password)
        token = create_session(login, password)
        delete_graph(token, add_graph(create_session(login, password), name))
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
    "login, password, graphs, result",
    [
        ('testUser1', 'testUser1', [['testText1'],
                                    ['testText2'],
                                    ['testText3'],
                                    ['testText4'],
                                    ['testText5']], True),
        ('testUser2', 'testUser2', [['1', '1'],
                                    ['2'],
                                    ['3'],
                                    ['4'],
                                    ['5']], True),
        ('testUser3', 'testUser3', [['dsklfklsdkl1'],
                                    ['lkslfkdskl2'],
                                    ['i32rkekdls3'],
                                    ['mnclaoioe4'],
                                    ['oerifkdjsljkds5']], True),
        ('423414534242342', '23423q4134141', [['TopNote1'],
                                              ['TopNote2'],
                                              ['TopNote3'],
                                              ['TopNote4'],
                                              ['TopNote5']], True),
        ('lox', 'losasx', [['dsklfklsdkl1'],
                           ['lkslfkdskl2'],
                           ['i32rkekdls3'],
                           ['mnclaoioe4'],
                           ['oerifkdjsljkds5']], True)
    ]
)
def test_get_all_graphs(login: str, password: str, graphs: list, result: bool):
    connection = db_connection()
    cur = connection.cursor()
    all_rows_actual = 0
    all_rows_exspected = 5
    try:
        create_account(login, password)
        token = create_session(login, password)
        for item in graphs:
            add_graph(token, item[0])
        all_rows_actual = len(get_graph_list(token))
    except Exception as ex:
        print(ex)
    finally:
        query = f'''DELETE FROM "users" WHERE login = '{login}' and password = '{password}' '''
        cur.execute(query)
        cur.close()
        connection.commit()
        connection.close()
    assert (all_rows_exspected == all_rows_actual) == result


@pytest.mark.parametrize(
    "login, password, name, new_name, result",
    [
        ('testUser1', 'testUser1', 'testText1', 'testText1Changed', True),
        ('testUser2', 'testUser2', 'testText2', 'testText2Changed', True),
        ('testUser3', 'testUser3', 'testText3', 'testText3Changed', True),
        ('testUser4', 'testUser4', 'testText4', 'testText4Changed', True),
        ('testUser5', 'testUser5', 'testText5', 'testText5Changed', True),

    ]
)
def test_update_graph(login: str, password: str, name: str, new_name: str, result: bool):
    connection = db_connection()
    cur = connection.cursor()
    title_after = ''
    try:
        create_account(login, password)
        token = create_session(login, password)
        id = add_graph(token, name)
        update_graph(token, id, new_name)
        query = f'''SELECT name FROM "graph" where "graphID" = '{id}' '''
        cur.execute(query)
        title_after = cur.fetchone()[0]
    except Exception as ex:
        print(ex)
    finally:
        query = f'''DELETE FROM "users" WHERE login = '{login}' and password = '{password}' '''
        cur.execute(query)
        cur.close()
        connection.commit()
        connection.close()
    assert (title_after == new_name) == result


# node tests
@pytest.mark.parametrize(
    "login, password, graph_name, x, y, node_name, result",
    [
        ('testUser1', 'testUser1', 'testGraph1', 10, 15, 'testNode1', True),
        ('testUser2', 'testUser2', 'testGraph2', 1, 5, 'testNode2', True),
        ('testUser3', 'testUser3', 'testGraph3', 1, 15.324, 'testNode3', True),
        ('testUser4', 'testUser4', 'testGraph4', 0, -10, 'testNode4', True),
        ('testUser5', 'testUser5', 'testGraph5', 34, 12, 'testNode5', True),
    ]
)
def test_add_node(login: str, password: str, graph_name: str, x: float, y: float, node_name: str, result: bool):
    connection = db_connection()
    cur = connection.cursor()
    rows_before = 0
    rows_after = 0
    try:
        query = f'''SELECT * FROM "node"'''
        cur.execute(query)
        rows_before = len(cur.fetchall())
        create_account(login, password)
        token = create_session(login, password)
        graph_id = add_graph(token, graph_name)
        add_node(token, graph_id, x, y, node_name)
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
    "login, password, graph_name, x, y, node_name, result",
    [
        ('testUser1', 'testUser1', 'testGraph1', 10, 15, 'testNode1', True),
        ('testUser2', 'testUser2', 'testGraph2', 1, 5, 'testNode2', True),
        ('testUser3', 'testUser3', 'testGraph3', 1, 15.324, 'testNode3', True),
        ('testUser4', 'testUser4', 'testGraph4', 0, -10, 'testNode4', True),
        ('testUser5', 'testUser5', 'testGraph5', 34, 12, 'testNode5', True),
    ]
)
def test_delete_node(login: str, password: str, graph_name: str, x: float, y: float, node_name: str, result: bool):
    connection = db_connection()
    cur = connection.cursor()
    rows_before = 0
    rows_after = 0
    try:
        query = f'''SELECT * FROM "node"'''
        cur.execute(query)
        rows_before = len(cur.fetchall())
        create_account(login, password)
        token = create_session(login, password)
        graph_id = add_graph(token, graph_name)
        node_id = add_node(token, graph_id, x, y, node_name)
        delete_node(token, node_id)
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
    "login, password, graph, nodes, result",
    [
        ('testUser1', 'testUser1', 'testText1',
                                    [[10, 15, 'testText1'],
                                                     [-10, 0, 'testText2'],
                                                     [124, 2345, 'testText3'],
                                                     [0, 0.124, 'testText4'],
                                                     [234, 4234, 'testText5']], True),
        ('testUser2', 'testUser2', 'testText1',
                                     [[10, 15, 'testText1'],
                                                     [-10, 0, 'testText2'],
                                                     [124, 2345, 'testText3'],
                                                     [0, 0.124, 'testText4'],
                                                     [234, 4234, 'testText5']], True),
        ('testUser3', 'testUser3', '1',
                                     [[1023124234, -32432423, '1'],
                                                     [-10, 4324, '2'],
                                                     [124321, 75673, '3'],
                                                     [0, 0.12443242343, '4'],
                                                     [22313434, 4243234, '5']], True),
        ('fsdffretf', 'dfgdfgvdfsgsfdg', 'graph1',
                                     [[10, 15, 'node1'],
                                                     [-10, 0, 'node2'],
                                                     [124, 2345, 'node3'],
                                                     [0, 0.124, 'node4'],
                                                     [234, 4234, 'node5']], True),
        ('234244123', '21423413123', 'bvnyu',
                                     [[10, 15, 'fdgdgdf'],
                                                     [-10, 0, 'dsfs2234234'],
                                                     [124, 2345, 'fdgdfgre'],
                                                     [0, 0.124, '32423'],
                                                     [234, 4234, 'fdgedfgd']], True),
    ]
)
def test_get_all_nodes(login: str, password: str, graph: str, nodes: list, result: bool):
    connection = db_connection()
    cur = connection.cursor()
    all_rows_actual = 0
    all_rows_exspected = 5
    try:
        create_account(login, password)
        token = create_session(login, password)
        graph_id = add_graph(token, graph)
        for item in nodes:
            add_node(token, graph_id, item[0], item[1], item[2])
        all_rows_actual = len(get_node_list(token,graph_id))
    except Exception as ex:
        print(ex)
    finally:
        query = f'''DELETE FROM "users" WHERE login = '{login}' and password = '{password}' '''
        cur.execute(query)
        cur.close()
        connection.commit()
        connection.close()
    assert (all_rows_exspected == all_rows_actual) == result


@pytest.mark.parametrize(
    "login, password, graph, x, y, name, new_x, new_y, new_name, result",
    [
        ('testUser1', 'testUser1', 'testGraph1', 10, 15, 'testNode1', 100, 150, 'testNode1Changed',  True),
        ('testUser2', 'testUser2', 'testGraph2', 1, 5, 'testNode2', 10, 50, 'testNode2Changed', True),
        ('testUser3', 'testUser3', 'testGraph3', 1, 15.324, 'testNode3', 10, 15.324, 'testNode3Changed', True),
        ('testUser4', 'testUser4', 'testGraph4', 0, -10, 'testNode4',  0, -100, 'testNode4Changed', True),
        ('testUser5', 'testUser5', 'testGraph5', 34, 12, 'testNode5', 340, 120, 'testNode5Changed', True),
    ]
)
def test_update_node(login: str, password: str, graph: str, x: float, y: float, name: str, new_x: float, new_y: float,
                     new_name: str, result: bool):
    connection = db_connection()
    cur = connection.cursor()
    name_after = ''
    x_after = 0.0
    y_after = 0.0
    try:
        create_account(login, password)
        token = create_session(login, password)
        graph_id = add_graph(token, graph)
        node_id = add_node(token, graph_id, x, y, name)
        update_node(token, graph_id, node_id, new_x, new_y, new_name)
        query = f'''SELECT "x","y","name" FROM "node" where "nodeid" = '{node_id}' '''
        cur.execute(query)
        data = cur.fetchone()
        name_after = data[2]
        y_after = float(data[1])
        x_after = float(data[0])
    except Exception as ex:
        print(ex)
    finally:
        query = f'''DELETE FROM "users" WHERE login = '{login}' and password = '{password}' '''
        cur.execute(query)
        cur.close()
        connection.commit()
        connection.close()
    assert (name_after == new_name and y_after == new_y and x_after == new_x) == result


# link tests
@pytest.mark.parametrize(
    "login, password, graph_name, source, target, value, result",
    [
        ('testUser1', 'testUser1', 'testGraph1', 10, 15, 324234.4324, True),
        ('testUser2', 'testUser2', 'testGraph2', 1, 5, 3241, True),
        ('testUser3', 'testUser3', 'testGraph3', 1, 15, -213412, True),
        ('testUser4', 'testUser4', 'testGraph4', 0, 1, 2345, True),
        ('testUser5', 'testUser5', 'testGraph5', 34, 12, 3241, True),
    ]
)
def test_add_link(login: str, password: str, graph_name: str, source: int, target: int, value: float, result: bool):
    connection = db_connection()
    cur = connection.cursor()
    rows_before = 0
    rows_after = 0
    try:
        query = f'''SELECT * FROM "link"'''
        cur.execute(query)
        rows_before = len(cur.fetchall())
        create_account(login, password)
        token = create_session(login, password)
        graph_id = add_graph(token, graph_name)
        add_link(token, graph_id, source, target, value)
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
    "login, password, graph_name, source, target, value, result",
    [
        ('testUser1', 'testUser1', 'testGraph1', 10, 15, 324234.4324, True),
        ('testUser2', 'testUser2', 'testGraph2', 1, 5, 3241, True),
        ('testUser3', 'testUser3', 'testGraph3', 1, 15, -213412, True),
        ('testUser4', 'testUser4', 'testGraph4', 0, 1, 2345, True),
        ('testUser5', 'testUser5', 'testGraph5', 34, 12, 3241, True),
    ]
)
def test_delete_link(login: str, password: str, graph_name: str, source: int, target: int, value: float, result: bool):
    connection = db_connection()
    cur = connection.cursor()
    rows_before = 0
    rows_after = 0
    try:
        query = f'''SELECT * FROM "link"'''
        cur.execute(query)
        rows_before = len(cur.fetchall())
        create_account(login, password)
        token = create_session(login, password)
        graph_id = add_graph(token, graph_name)
        link_id = add_link(token, graph_id, source, target, value)
        delete_link(token, link_id)
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
    "login, password, graph, links, result",
    [
        ('testUser1', 'testUser1', 'testText1',
                                    [[10, 15, 21412],
                                     [-10, 0, 124234],
                                     [124, 2345, 124.243],
                                     [0, 0.124, -12341],
                                     [234, 4234, 2141]], True),
        ('testUser2', 'testUser2', 'testText1',
                                     [[10, 15, 234],
                                      [-10, 0, 124234],
                                      [124, 2345, 124.243],
                                      [0, 0.124, -12341],
                                      [234, 4234, 2141]], True),
        ('testUser3', 'testUser3', '1',
                                     [[1023124234, -32432423, '1'],
                                      [-10, 0, 124234],
                                      [124, 2345, 124.243],
                                      [0, 0.124, -12341],
                                      [234, 4234, 2141]], True),
        ('fsdffretf', 'dfgdfgvdfsgsfdg', 'graph1',
                                     [[10, 15, 2341],
                                      [-10, 0, 124234],
                                      [124, 2345, 124.243],
                                      [0, 0.124, -12341],
                                      [234, 4234, 2141]], True),
        ('234244123', '21423413123', 'bvnyu',
                                     [[10, 15, 32423],
                                      [-10, 0, 124234],
                                      [124, 2345, 124.243],
                                      [0, 0.124, -12341],
                                      [234, 4234, 2141]], True),
    ]
)
def test_get_all_links(login: str, password: str, graph: str, links: list, result: bool):
    connection = db_connection()
    cur = connection.cursor()
    all_rows_actual = 0
    all_rows_exspected = 5
    try:
        create_account(login, password)
        token = create_session(login, password)
        graph_id = add_graph(token, graph)
        for item in links:
            add_link(token, graph_id, item[0], item[1], item[2])
        all_rows_actual = len(get_link_list(token, graph_id))
    except Exception as ex:
        print(ex)
    finally:
        query = f'''DELETE FROM "users" WHERE login = '{login}' and password = '{password}' '''
        cur.execute(query)
        cur.close()
        connection.commit()
        connection.close()
    assert (all_rows_exspected == all_rows_actual) == result


@pytest.mark.parametrize(
    "login, password, graph_name, source, target, value, new_value, result",
    [
        ('testUser1', 'testUser1', 'testGraph1', 10, 15, 324234.4324, 1, True),
        ('testUser2', 'testUser2', 'testGraph2', 1, 5, 3241, 423, True),
        ('testUser3', 'testUser3', 'testGraph3', 1, 15, -213412, -124, True),
        ('testUser4', 'testUser4', 'testGraph4', 0, 1, 2345, 4324, True),
        ('testUser5', 'testUser5', 'testGraph5', 34, 12, 3241, 4234, True),
    ]
)
def test_update_link(login: str, password: str, graph_name: str, source: int, target: int, value: float,
                     new_value: float, result: bool):
    connection = db_connection()
    cur = connection.cursor()
    value_after = 0.0
    try:
        create_account(login, password)
        token = create_session(login, password)
        graph_id = add_graph(token, graph_name)
        link_id = add_link(token, graph_id, source, target, value)
        update_link(token, graph_id, link_id, new_value)
        query = f'''SELECT "value" FROM "link" where "linkid" = '{link_id}' '''
        cur.execute(query)
        value_after = float(cur.fetchone()[0])
    except Exception as ex:
        print(ex)
    finally:
        query = f'''DELETE FROM "users" WHERE login = '{login}' and password = '{password}' '''
        cur.execute(query)
        cur.close()
        connection.commit()
        connection.close()
    assert (value_after == new_value) == result
