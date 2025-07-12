class Stock():
    def __init__(self, data: dict):
        self.seed_shop_items: list = self.get_all_items(data, "Seeds")
        self.gear_shop_items: list = self.get_all_items(data, "Gears")
        self.seed_shop: list = data["seedsStock"]
        self.gear_shop: list = data["gearStock"]
        self.egg_shop: list = data["eggStock"]
        self.event_shop: list = data["eventStock"]
        self.easter_shop: list = data["easterStock"]
        self.night_shop: list = data["nightStock"]
        self.merchants_shop: list = data["merchantsStock"]
        self.cosmetics_shop: list = data["cosmeticsStock"]
        self.next_refresh = data["restockTimers"]["seeds"]
        self.eggs_refresh = data["restockTimers"]["eggs"]
        self.category_refresh_status = data["categoryRefreshStatus"]

    def get_all_items(self, stock, shop_name: str):
        all_items = list()
        for item in stock["lastSeen"][shop_name]:
            try:
                curr_item = {"name": item["name"],
                             "emoji": item["emoji"],
                             "pictureUrl": stock["imageData"][item["name"]]}
            except:
                curr_item = {"name": item["name"],
                             "emoji": item["emoji"],
                             "pictureUrl": None}
            all_items.append(curr_item)
        return all_items

    def get_items(self, shop: list, config=set()) -> str:
        items = list()
        if config:
            for item in shop:
                if item["name"] in config:
                    items.append(f"{item["name"]} — {item["value"]}")
        else:
            for item in shop:
                items.append(f"{item["name"]} — {item["value"]}")
        return "\n".join(items)

    def json(self):
        return {"seed_shop_items": self.seed_shop_items,
                "gear_shop_items": self.gear_shop_items,
                "seed_shop": self.seed_shop,
                "gear_shop": self.gear_shop,
                "egg_shop": self.egg_shop,
                "event_shop": self.event_shop,
                "easter_shop": self.easter_shop,
                "night_shop": self.night_shop,
                "merchants_shop": self.merchants_shop,
                "cosmetics_shop": self.cosmetics_shop,
                "next_refresh": self.next_refresh,
                "eggs_refresh": self.eggs_refresh,
                "category_refresh_status": self.category_refresh_status}

    def __repr__(self):
        string_builder = list()
        string_builder.append(f"Seeds:\n{self.get_items(self.seed_shop)}")
        string_builder.append(f"Gears:\n{self.get_items(self.gear_shop)}")
        string_builder.append(f"Eggs:\n{self.get_items(self.egg_shop)}")
        string_builder.append(
            f"Cosmetics:\n{self.get_items(self.cosmetics_shop)}")
        if self.event_shop:
            string_builder.append(
                f"Event shop:\n{self.get_items(self.event_shop)}")
        if self.easter_shop:
            string_builder.append(
                f"Easter shop:\n{self.get_items(self.easter_shop)}")
        if self.night_shop:
            string_builder.append(
                f"Night shop:\n{self.get_items(self.night_shop)}")
        if self.merchants_shop:
            string_builder.append(
                f"Merchant shop:\n{self.get_items(self.merchants_shop)}")
        return "\n\n".join(string_builder)

    def __str__(self):
        return self.__repr__()
