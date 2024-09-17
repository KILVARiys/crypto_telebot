import json

class TaskHandler:
    def __init__(self):
        self.__coins = ["BTC", "ETH", "LTC"]

    @staticmethod
    def read_task_file():
        with open("tasks.json", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def add_task_to_file(data: dict):
        last_changes = TaskHandler.read_task_file()
        last_changes[data["name"]] = data["price to alert"]
        with open("tasks.json", "w", encoding="utf-8") as file :
            json.dump(last_changes, file, indent=4)

    @staticmethod
    def delete_task_in_file(coin_name, update=True):
        last_changes = TaskHandler.read_task_file()
        try:
            del last_changes[coin_name]
            with open("tasks.json", "w", encoding="utf-8") as file:
                json.dump(last_changes, file, indent=4)

        except KeyError:
            print("Ключ отсутствует в задачах")
        if update:
            run_js("location.reload(")

    @staticmethod
    def get_task_list():
        result = []
        tasks = TaskHandler.read_task_file()

        # TODO: update