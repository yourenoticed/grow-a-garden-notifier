from json import loads, dumps


def get_configs() -> dict:
    try:
        with open("./db/configs.json", "r") as file:
            raw = file.read()
            return loads(raw)
    except:
        return {"users": list()}


def get_user_ids() -> list[int]:
    configs = get_configs()
    return [user["id"] for user in configs["users"] if user["status"] == "member"]


def add_user(user_id: int) -> None:
    configs = get_configs()
    if not find_user(user_id):
        user = dict()
        user["id"] = user_id
        user["status"] = "member"
        user["config"] = get_default_config()
        configs["users"].append(user)
        write_file(configs)


def block_user(user_id: int) -> None:
    configs = get_configs()
    user_i, user = find_user(user_id)
    user["status"] = "blocked"
    configs["users"][user_i] = user
    write_file(configs)


def unblock_user(user_id: int) -> None:
    configs = get_configs()
    user_i, user = find_user(user_id)
    user["status"] = "member"
    configs["users"][user_i] = user
    write_file(configs)


def get_stock_config(user_id: int) -> list[str]:
    user = find_user(user_id)[1]
    return user["config"]["stock"]


def get_weather_config(user_id: int) -> list[str]:
    user = find_user(user_id)[1]
    return user["config"]["weather"]


def find_user(user_id: int) -> tuple[int, dict] | None:
    try:
        configs = get_configs()
        for i, user in enumerate(configs["users"]):
            if user["id"] == user_id:
                return (i, user)
    except KeyError:
        return None


def write_stock_config(user_id: int, new_config: list) -> None:
    configs = get_configs()
    user_i, user = find_user(user_id)
    if user:
        configs["users"][user_i]["config"]["stock"] = new_config
        write_file(configs)


def write_weather_config(user_id: int, new_config: list) -> None:
    configs = get_configs()
    user_i, user = find_user(user_id)
    if user:
        configs["users"][user_i]["config"]["weather"] = new_config
        write_file(configs)


def write_file(json_to_write: dict) -> None:
    with open("./db/configs.json", "w") as file:
        file.write(dumps(json_to_write))


def get_default_config() -> list:
    with open("./db/default_config.json", "r") as file:
        return loads(file.read())
