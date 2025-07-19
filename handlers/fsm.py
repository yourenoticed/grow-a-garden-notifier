from aiogram.fsm.state import State, StatesGroup


class ConfigSetup(StatesGroup):
    config_sel = State()
    # Seeds, Gears, Eggs, Cosmetics, Weather
    seeds = State()
    eggs = State()
    cosmetics = State()
    weather = State()
