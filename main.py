from flask import Flask
from flask import request
from loguru import logger
import json
from resources.functions import (create_account, delete_account, update_password, create_session, delete_session,
                                 get_session_list, get_graph_list, update_graph, delete_graph, add_graph,
                                 get_node_list, delete_node, update_node, add_node,
                                 get_link_list, delete_link, add_link, update_link)


logger.add('misc/logs/debug.log', format='{time} {level} {message}', level="DEBUG")
app = Flask('API_Notes')


#аккаунт
@app.route('/account/register', methods=['PUT'])
def registration() -> str:
    user = request.args.get('username')
    password = request.args.get('password')
    if create_account(user, password):
        return "Account has been created"
    return "Account already exists"


@app.route('/account/change-password', methods=['POST'])
def change_password() -> str:
    token = request.args.get('token')
    password = request.args.get('password')
    if update_password(token, password):
        return "Password has been successfully changed"
    return "Password has not been changed, the session token is invalid"


@app.route('/account/delete-account', methods=['DELETE'])
def remove_account() -> str:
    token = request.args.get('token')
    if delete_account(token):
        return "Account has been successfully deleted"
    return "Account was not deleted, invalid session token"


#сессии
@app.route('/account/sign-in', methods=['PUT'])
def login() -> str:
    user = request.args.get('username')
    password = request.args.get('password')
    token = create_session(user, password)
    if token != '':
        return token
    return "no account"


@app.route('/account/sign-out', methods=['DELETE'])
def log_out() -> str:
    token = request.args.get('token')
    if delete_session(token):
        return "Session was successfully deleted"
    return "Session is already closed"


@app.route('/account/session-list', methods=['GET'])
def get_sessions() -> list:
    token = request.args.get('token')
    return get_session_list(token)


#графы
@app.route('/graphs/graph-list', methods=['GET'])
def get_graphs() -> list:
    token = request.args.get('token')
    return get_graph_list(token)


@app.route('/graphs/add', methods=['PUT'])
def new_graph() -> str:
    token = request.args.get('token')
    name = request.args.get('name')
    return str(add_graph(token, name))


@app.route('/graphs/update', methods=['POST'])
def change_graph() -> str:
    token = request.args.get('token')
    name = request.args.get('name')
    id = int(request.args.get('id'))
    if update_graph(token, id, name):
        return "Graph has been successfully updated"
    return "Graph was not been updated"


@app.route('/graphs/delete', methods=['DELETE'])
def remove_graph() -> str:
    token = request.args.get('token')
    id = int(request.args.get('id'))
    if delete_graph(token, id):
        return "Graph has been successfully deleted"
    return "Graph was not deleted"


#Точки
@app.route('/nodes/node-list', methods=['GET'])
def get_nodes() -> list:
    token = request.args.get('token')
    graph_id = int(request.args.get('id'))
    return get_node_list(token, graph_id)


@app.route('/nodes/add', methods=['PUT'])
def new_node() -> str:
    token = request.args.get('token')
    graph_id = int(request.args.get('id'))
    x = float(request.args.get('x'))
    y = float(request.args.get('y'))
    name = request.args.get('name')
    return str(add_node(token, graph_id, x, y, name))


@app.route('/nodes/update', methods=['POST'])
def change_node() -> str:
    token = request.args.get('token')
    graph_id = int(request.args.get('graphid'))
    node_id = int(request.args.get('nodeid'))
    x = float(request.args.get('x'))
    y = float(request.args.get('y'))
    name = request.args.get('name')
    if update_node(token, graph_id, node_id, x, y, name):
        return "Node has been successfully updated"
    return "Node was not been updated"


@app.route('/graphs/delete', methods=['DELETE'])
def remove_node() -> str:
    token = request.args.get('token')
    id = int(request.args.get('id'))
    if delete_node(token, id):
        return "Node has been successfully deleted"
    return "Node was not deleted"


#Связи
@app.route('/links/link-list', methods=['GET'])
def get_links() -> list:
    token = request.args.get('token')
    graph_id = int(request.args.get('id'))
    return get_link_list(token, graph_id)


@app.route('/links/add', methods=['PUT'])
def new_link() -> str:
    token = request.args.get('token')
    graph_id = int(request.args.get('id'))
    source = int(request.args.get('source'))
    target = int(request.args.get('target'))
    value = float(request.args.get('value'))
    return str(add_link(token, graph_id, source, target, value))


@app.route('/links/update', methods=['POST'])
def change_link() -> str:
    token = request.args.get('token')
    graph_id = int(request.args.get('id'))
    link_id = int(request.args.get('source'))
    value = float(request.args.get('value'))
    if update_link(token, graph_id, link_id, value):
        return "Link has been successfully updated"
    return "Link was not been updated"


@app.route('/links/delete', methods=['DELETE'])
def remove_link() -> str:
    token = request.args.get('token')
    id = int(request.args.get('id'))
    if delete_link(token, id):
        return "Link has been successfully deleted"
    return "Link was not deleted"


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")