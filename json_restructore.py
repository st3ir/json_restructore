import requests
import json


def read_config(config):
    """ Читаем файл и возвращаем """
    with open(config, 'r') as file:
        read_configuration = json.load(file)
    return read_configuration


def write_config(filename, data):
    """ Записываем данные в локальный файл """
    with open(filename, 'w') as file:
        json.dump(data, file)


def get_data_from_server(url, username, password):
    """ Отправляем GET-запрос на сервер """
    response = requests.get(url, auth=(username, password))
    return response.json()


def restructure_data(data):
    """ Пересобираем данные """
    restructured_data = {}
    for employee in data["employees"]:
        department_id = employee["department"]["id"]
        department_name = employee["department"]["department_name"]
        if department_id not in restructured_data:
            restructured_data[department_id] = {
                "department_name": department_name, "employees": []}
        restructured_data[department_id]["employees"].append(
            {"name": employee["name"], "age": employee["age"]})
    return restructured_data


def send_data_to_server(url, username, password, data):
    """ Отправляем данные на сервер """
    response = requests.post(url, auth=(username, password), json=data)
    return response.status_code


def main(config):
    """ Основной метод для реализации механики пересборки """
    config = read_config(config)
    url = config["server_url"]
    username = config["username"]
    password = config["password"]

    # Получаем данные с сервера
    main_data = get_data_from_server(url, username, password)

    # Пересобираем данные
    restructured_data = restructure_data(main_data)

    # Отправляем данные обратно на сервер
    status_code = send_data_to_server(
        url, username, password, restructured_data
    )

    # Сохраняем данные локально
    if status_code == 200:
        write_config(config["local_filename"], restructured_data)
        print("Данные успешно сохранены.")
    else:
        print(
            f"Ошибка при отправке данных. "
            f"Статус-код: {status_code}"
        )


if __name__ == "__main__":
    main("config.json")
