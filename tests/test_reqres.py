import json
import requests
from jsonschema import validate

from utils.schemas_path import load_schema


def test_get_user():
    first_name = "Lindsay"
    last_name = "Ferguson"
    response = requests.get("https://reqres.in/api/users", data={"name": first_name, "last_name": last_name})

    assert response.status_code == 200


def test_update_user():
    name = "Sergey"
    job = "Teacher"
    response = requests.put("https://reqres.in/api/users/2", data={"name": name, "job": job})

    assert response.status_code == 200
    assert response.json()["name"] == name
    assert response.json()["job"] == job
    assert response.json()["job"] != ["name"]


def test_user_not_found():
    response = requests.get('https://reqres.in/api/users/23')

    assert response.status_code == 404


def test_delete_user():
    response = requests.delete("https://reqres.in/api/users/2")

    assert response.status_code == 204


def test_user_login_success():
    email = "eve.holt@reqres.in"
    password = "cityslicka"
    response = requests.post("https://reqres.in/api/login", data={"email": email, "password": password})
    body = response.json()

    assert body["token"] == "QpwL5tke4Pnpja7X4"
    schema = load_schema("user_login.json")
    with open(schema) as file:
        schema = json.load(file)
    validate(body, schema=schema)


def test_create_user():
    name = "morpheus"
    job = "leader"

    response = requests.post("https://reqres.in/api/users", data={"name": name, "job": job})
    body = response.json()

    assert response.status_code == 201

    schema = load_schema("create_user.json")
    with open(schema) as file:
        schema = json.load(file)
    validate(body, schema=schema)

    assert body["name"] == name
    assert body["job"] == job


def test_user_list():
    first_name = "Janet"
    last_name = "Weaver"

    response = requests.get('https://reqres.in/api/users/2', data={"first_name": first_name, "last_name": last_name})
    body = response.json()

    assert response.json()["data"]["first_name"] == first_name
    assert response.status_code == 200
    schema = load_schema("list_users.json")
    with open(schema) as file:
        schema = json.load(file)
    validate(body, schema=schema)
    assert body["data"]["last_name"] == last_name


def test_user_update():
    name = "morpheus"
    job = "zion resident"

    response = requests.patch('https://reqres.in/api/users/2', data={"name": name, "job": job})
    body = response.json()

    assert response.json()["name"] == name
    assert response.status_code == 200

    schema = load_schema("update_user.json")
    with open(schema) as file:
        schema = json.load(file)
    validate(body, schema=schema)
    assert body["job"] == job


def test_user_registration_not_success():
    response = requests.post("https://reqres.in/api//api/register", data={"email": "sydney@fife"})

    assert response.status_code == 404


def test_user_login_not_success():
    response = requests.post("https://reqres.in/api/login", data={"email": "peter@klaven"})

    assert response.status_code == 400

