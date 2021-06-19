from flask import Flask, request, jsonify
app = Flask(__name__)

queues        = []     # relacao de filas
idx_queues    = {}     # idx das filas cadastradas
peoplesGrades = []     # armazenar nota das pessoas que saíram da fila.

 
# Questionário de avaliação
# 1 - Qual nota vc apresenta pelo tempo de espera na fila?
# 2 - Qual nota vc apresenta pelo seu atendimento?


# FILAS 
@app.route('/queues', methods=['POST'])
def add_queue():
    requisicao = request.json
    for queue in queues:
        for item in requisicao:
            if(queue['name'] == item['name']):
                return jsonify({"Atenção! Fila já cadastrada:": item['name']})
            else:
                # inserção pelos elementos e idx nos names para as posições inseridas na fila. 
                idx_queues[item['name']] = len(queues)
                queues.append(item)

    for item in requisicao:
        #inserção pelos elementos e idx nos names para as posições inseridas na fila.    
        idx_queues[item['name']] = len(queues)
        queues.append(item)

    return jsonify("Informações adicionadas com sucesso!", queues)


@app.route('/queues')
def get_all_queues():
    return jsonify("Exibição de Filas Cadastradas!", {
        "idx_queues": idx_queues,
        "queues": queues
    })


@app.route('/queues/delete', methods=['POST'])
def delete_queue():
    requisicao = request.json
    for queue in queues:
        if(queue['name'] == requisicao['name']):
            idx_queues.pop(requisicao['name'])
            queues.remove(queue)
            return jsonify({"Fila removida com sucesso:": requisicao['name']})
    
    return jsonify({"Atenção! Fila inexistente:": requisicao['name']})   


# PESSOAS NA FILA
@app.route('/queues/people', methods=['POST'])
def add_queue_people():
    requisicao = request.json
    for index, item in enumerate(queues):
        if item['name'] == requisicao['name']:
            queue = item
    
    for index, people in enumerate(requisicao['Queue']):
        if(queue['qtd'] >= queue['max']):
            return jsonify("Limite máximo de pessoas na fila!")
        queue["Queue"].append(people)

    queue["qtd"] = len(queue["Queue"])
    queue["total"] += len(requisicao["Queue"])  
    
    return jsonify(queue)


@app.route('/queues/people')
def get_all_queues_people():

    requisicao = request.json

    for item in queues:
        if(requisicao['name'] == item['name']):
            return jsonify("Exibição Clientes na Fila!", {
                "fila": item['name'],
                "client": item['Queue']
            })
    return jsonify({"Atenção! Fila inexistente:": requisicao['name']})   


@app.route('/queues/people/delete', methods=['POST'])
def delete_queue_people():
    requisicao = request.json

    for queue in queues:
        if (requisicao['name'] == queue['name']):
            if(len(queue['Queue']) > 0):
                removedPerson = queue['Queue'].pop(0)
                removedPersonQueue = {
                queue["name"]: {
                      removedPerson: {
                          "Nota em relação ao tempo de espera na fila": requisicao['grade1'],
                          "Nota em relação ao atendimento": requisicao['grade2']
                      }
                    }
                }
                peoplesGrades.append(removedPersonQueue)
                queue['qtd'] = len(queue['Queue'])
                return jsonify({"Cliente removido da fila:": removedPerson, "Notas": removedPersonQueue})
            return jsonify("Não há clientes para serem removidos!")
            
    return jsonify("Fila não encontrada!")

# exibição dos dados.
@app.route('/queues/client/grade', methods=['GET'])
def add_client_grade():

    return jsonify("Relatório geral de atendimento:", peoplesGrades)
