from flask import Flask
from loguru import logger
from resources.functions import (create_account, delete_account, update_password, create_session, delete_session,
                                 get_session_list, get_graph_list, update_graph, delete_graph, add_graph,
                                 get_node_list, delete_node, update_node, add_node,
                                 get_link_list, delete_link, add_link, update_link)


logger.add('misc/logs/debug.log', format='{time} {level} {message}', level="DEBUG")
app = Flask('API_Notes')


#аккаунт
@app.route('/account/register/<login>/<password>', methods=['PUT'])
def registration(login, password) -> str:
    if create_account(login, password):
        return "Account has been created"
    return "Account already exists"


@app.route('/account/change-password/<token>/<password>', methods=['POST'])
def change_password(token, password) -> str:
    if update_password(token, password):
        return "Password has been successfully changed"
    return "Password has not been changed, the session token is invalid"


@app.route('/account/delete-account/<token>', methods=['DELETE'])
def remove_account(token) -> str:
    if delete_account(token):
        return "Account has been successfully deleted"
    return "Account was not deleted, invalid session token"


#сессии
@app.route('/account/sign-in/<login>/<password>', methods=['PUT'])
def login(login, password) -> str:
    token = create_session(login, password)
    if token != '':
        return token
    return "no account"


@app.route('/account/sign-out/<token>', methods=['DELETE'])
def log_out(token) -> str:
    if delete_session(token):
        return "Session was successfully deleted"
    return "Session is already closed"


@app.route('/account/session-list/<token>', methods=['GET'])
def get_sessions(token) -> list[tuple]:
    return get_session_list(token)


#графы
@app.route('/graphs/graph-list/<token>', methods=['GET'])
def get_graphs(token) -> list[tuple]:
    return get_graph_list(token)


@app.route('/graphs/add/<token>/<name>', methods=['PUT'])
def new_graph(token, name) -> int:
    return add_graph(token, name)


@app.route('/graphs/update/<token>/<id>/<name>', methods=['POST'])
def change_graph(token, id, name) -> str:
    if update_graph(token, id, name):
        return "Graph has been successfully updated"
    return "Graph was not been updated"


@app.route('/graphs/delete/<token>/<id>', methods=['DELETE'])
def remove_graph(token, id) -> str:
    if delete_graph(token,id):
        return "Graph has been successfully deleted"
    return "Graph was not deleted"


#Точки
@app.route('/nodes/node-list/<token>/<id>', methods=['GET'])
def get_nodes(token, graph_id) -> list[tuple]:
    return get_node_list(token, graph_id)


@app.route('/nodes/add/<token>/<id>/<x>/<y>/<name>', methods=['PUT'])
def new_node(token, graph_id, x, y, name) -> int:
    return add_node(token, graph_id, x, y, name)


@app.route('/nodes/update/<token>/<graphid>/<nodeid>/<x>/<y>/<name>', methods=['POST'])
def change_node(token, graph_id, node_id, x, y, name) -> str:
    if update_node(token, graph_id, node_id, x, y, name):
        return "Node has been successfully updated"
    return "Node was not been updated"


@app.route('/graphs/delete/<token>/<id>', methods=['DELETE'])
def remove_node(token, id) -> str:
    if delete_node(token, id):
        return "Node has been successfully deleted"
    return "Node was not deleted"


#Связи
@app.route('/links/link-list/<token>/<id>', methods=['GET'])
def get_links(token, graph_id) -> list[tuple]:
    return get_link_list(token, graph_id)


@app.route('/links/add/<token>/<id>/<source>/<target>/<value>', methods=['PUT'])
def new_link(token, graph_id, source, target, value) -> int:
    return add_link(token, graph_id, source, target, value)


@app.route('/links/update/<token>/<graphid>/<linkid>/<value>', methods=['POST'])
def change_link(token, graph_id, link_id, value) -> str:
    if update_link(token, graph_id, link_id, value):
        return "Link has been successfully updated"
    return "Link was not been updated"


@app.route('/links/delete/<token>/<id>', methods=['DELETE'])
def remove_link(token, id) -> str:
    if delete_link(token, id):
        return "Link has been successfully deleted"
    return "Link was not deleted"


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")