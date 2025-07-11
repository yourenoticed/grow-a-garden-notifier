from json import loads, dumps


def get_configs() -> dict:
    try:
        with open("./db/configs.json", "r") as file:
            raw = file.read()
            return loads(raw)
    except:
        return dict()


def get_user_ids() -> list[int]:
    configs = get_configs()
    return [int(user_id) for user_id in configs.keys()]


def add_user(user_id: int) -> None:
    try:
        configs = get_configs()
    except:
        configs = dict()
    with open("./db/configs.json", "w") as file:
        if str(user_id) not in configs.keys():
            configs[str(user_id)] = get_default_config()
        file.write(dumps(configs))


def get_user_config(user_id: int) -> list[str]:
    configs = get_configs()
    return configs[str(user_id)]


def write_config(user_id: int, config: list) -> None:
    configs = get_configs()
    configs[str(user_id)] = config
    with open("./db/configs.json", "w") as file:
        file.write(dumps(configs))


def get_default_config() -> list:
    with open("./db/default_config.json", "r") as file:
        return loads(file.read())
