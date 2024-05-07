from fastapi.testclient import TestClient
# from datetime import date
from backend.main import app


### Users Tests ###

# test GET /users
def test_get_users():
    test_client = TestClient(app)
    response = test_client.get("/users")
    
    assert response.status_code == 200
    assert response.json()["meta"]['count'] == 10


# test POST /users
def test_post_user():
    test_client = TestClient(app)
    response = test_client.get("/users")

    assert response.json()["meta"]['count'] == 10
    assert response.status_code == 200

    test_client.post("/users", json={"id": "Captain Jack"})
    
    response2 = test_client.get("/users")
    assert response2.json()["meta"]['count'] == 11
    assert response2.status_code == 200
    
    #test for duplicate ID
    response = test_client.post("/users", json={"id": "Captain Jack"})
    assert response.status_code == 422
    assert response.json()["detail"]["type"] == "duplicate_entity"
    assert response.json()["detail"]["entity_name"] == "User"
    assert response.json()["detail"]["entity_id"] == "Captain Jack"

# test GET /users/{user_id}
def test_get_users_user_id():
    test_client = TestClient(app)
    
    #if user exists
    response = test_client.get("/users/bomb20")
    assert response.status_code == 200
    assert response.json()["user"]["id"] == "bomb20"

    #if user doesn't exist
    response = test_client.get("/users/bomb2asdfasdfsdf0")
    assert response.status_code == 404
    assert response.json()["detail"]["type"] == "entity_not_found"
    assert response.json()["detail"]["entity_name"] == "User"
    assert response.json()["detail"]["entity_id"] == "bomb2asdfasdfsdf0"


# test GET /users/{user_id}/chats
def test_get_users_chats():
    test_client = TestClient(app)
    
    #if user exists
    response = test_client.get("/users/bomb20/chats")
    assert response.status_code == 200
    assert response.json()["meta"]["count"] == 1

    #if user doesn't exist
    response = test_client.get("/users/bomb2asdfasdfsdf0/chats")
    assert response.status_code == 404
    assert response.json()["detail"]["type"] == "entity_not_found"
    assert response.json()["detail"]["entity_name"] == "User"
    assert response.json()["detail"]["entity_id"] == "bomb2asdfasdfsdf0"



### Chats Tests ###

# test GET /chats
def test_get_chats():
    test_client = TestClient(app)
    response = test_client.get("/chats")
    
    assert response.status_code == 200
    assert response.json()["meta"]['count'] == 6


# test GET /chats/{chat_id}
def test_get_chats_by_id():
    test_client = TestClient(app)

    #if chat exists
    response = test_client.get("/chats/e0ec0881a2c645de842ca5dd0fa7985b")
    assert response.status_code == 200
    assert response.json()["chat"]["id"] == 'e0ec0881a2c645de842ca5dd0fa7985b'

    #if chat doesn't exist
    response = test_client.get("/chats/asdf")
    assert response.status_code == 404
    assert response.json()["detail"]["type"] == "entity_not_found"
    assert response.json()["detail"]["entity_name"] == "Chat"
    assert response.json()["detail"]["entity_id"] == "asdf"


# test PUT /chats/{chat_id}
def test_put_chat_by_id():
    test_client = TestClient(app)

    #if chat exists
    response = test_client.get("/chats/e0ec0881a2c645de842ca5dd0fa7985b")
    assert response.status_code == 200
    assert response.json()["chat"]["name"] == 'newt'
    response = test_client.put("/chats/e0ec0881a2c645de842ca5dd0fa7985b", json={"name": "newName"})
    assert response.status_code == 200
    assert response.json()["chat"]["name"] == 'newName'

    #if chat doesn't exist
    response = test_client.get("/chats/asdf")
    assert response.status_code == 404
    assert response.json()["detail"]["type"] == "entity_not_found"
    assert response.json()["detail"]["entity_name"] == "Chat"
    assert response.json()["detail"]["entity_id"] == "asdf"


# test DELETE /chats/{chat_id}
def test_delete_chat_by_id():
    test_client = TestClient(app)

    #if chat exists
    response = test_client.get("/chats")
    assert response.status_code == 200
    assert response.json()["meta"]['count'] == 6
    test_client.delete("/chats/e0ec0881a2c645de842ca5dd0fa7985b")
    response = test_client.get("/chats")
    assert response.status_code == 200
    assert response.json()["meta"]['count'] == 5

     #if chat doesn't exist
    response = test_client.get("/chats/asdf")
    assert response.status_code == 404
    assert response.json()["detail"]["type"] == "entity_not_found"
    assert response.json()["detail"]["entity_name"] == "Chat"
    assert response.json()["detail"]["entity_id"] == "asdf"


# test GET /chats/{chat_id}/messages
def test_get_chats_messsages():
    test_client = TestClient(app)

    #if chat exists
    response = test_client.get("/chats/6215e6864e884132baa01f7f972400e2/messages")
    assert response.status_code == 200
    assert response.json()["meta"]['count'] == 35

    #lets try another
    response = test_client.get("/chats/6ad56d52b138432a9bba609533015cf3/messages")
    assert response.status_code == 200
    assert response.json()["meta"]['count'] == 41

    #if chat doesn't exist
    response = test_client.get("/chats/6af015cf3/messages")
    assert response.status_code == 404
    assert response.json()["detail"]["type"] == "entity_not_found"
    assert response.json()["detail"]["entity_name"] == "Chat"
    assert response.json()["detail"]["entity_id"] == "6af015cf3"


# test GET /chats/{chat_id}/users
def test_get_chats_users():
    test_client = TestClient(app)

    #if chat exists
    response = test_client.get("/chats/6215e6864e884132baa01f7f972400e2/users")
    assert response.status_code == 200
    assert response.json()["meta"]['count'] == 2

    #if chat doesn't exist
    response = test_client.get("/chats/6f3/users")
    assert response.status_code == 404
    assert response.json()["detail"]["type"] == "entity_not_found"
    assert response.json()["detail"]["entity_name"] == "Chat"
    assert response.json()["detail"]["entity_id"] == "6f3"
