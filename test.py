import requests

BASE_URL = "http://127.0.0.1:5000"

score = 0


def print_result(test_name, success):
    global score
    if success:
        print(f"[✔] {test_name}")
        score += 3
    else:
        print(f"[✘] {test_name}")


# 🧩 1. Criar equipe
def test_create_team():
    response = requests.post(f"{BASE_URL}/teams", json={
        "name": "Equipe Teste 5"
    })
    success = response.status_code == 201 or response.status_code == 200
    print_result("Criar equipe", success)

    if success:
        return response.json()["data"]["id"]
    return None


# 🧩 2. Listar equipes
def test_list_teams():
    response = requests.get(f"{BASE_URL}/teams")
    success = response.status_code == 200 and isinstance(response.json()["data"], list)
    print_result("Listar equipes", success)


# 🧩 3. Criar participante válido
def test_create_participant(team_id):
    response = requests.post(f"{BASE_URL}/users", json={
        "nome": "Pedro",
        "idade": 18,
        "email": "p@example.com",
        "senha":"1234567",
        "team_id": team_id
    })
    success = response.status_code in [200, 201]
    print_result("Criar participante válido", success)

    if success:
        return response.json()["data"]["id"]
    return None


# 🧩 4. Criar participante com equipe inválida
def test_invalid_team():
    response = requests.post(f"{BASE_URL}/participants", json={
        "nome": "Erro",
        "idade": 20,
        "team_id": 9999
    })
    success = response.status_code == 404
    print_result("Erro ao criar participante com equipe inválida", success)


# 🧩 5. Listar participantes
def test_list_participants():
    response = requests.get(f"{BASE_URL}/users")
    success = response.status_code == 200 and isinstance(response.json()["data"], list)
    print_result("Listar participantes", success)


# 🧩 6. Endpoint orientado ao domínio
def test_participants_by_team(team_id):
    response = requests.get(f"{BASE_URL}/teams/{team_id}/participants")
    success = response.status_code == 200 and isinstance(response.json()["data"], list)
    print_result("Listar participantes por equipe", success)


# 🧩 7. Validação de dados (nome ausente)
def test_validation():
    response = requests.post(f"{BASE_URL}/teams", json={})
    success = response.status_code == 400
    print_result("Validação de dados obrigatórios", success)


# 🚀 Execução dos testes

print("\n🚀 Iniciando testes...\n")

team_id = test_create_team()
test_list_teams()

if team_id:
    test_create_participant(team_id)
    test_participants_by_team(team_id)

test_invalid_team()
test_list_participants()
test_validation()

print(f"\n🎯 Pontuação final: {score}/30\n")