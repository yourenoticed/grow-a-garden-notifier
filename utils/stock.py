class Stock():
    def __init__(self, data: dict):
        self.seed_shop_items: list = self.get_all_items(data, "Seeds")
        self.gear_shop_items: list = self.get_all_items(data, "Gears")
        self.seed_shop: list = data["seedsStock"]
        self.gear_shop: list = data["gearStock"]
        self.egg_shop: list = data["eggStock"]
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

    def get_item_info(self, item_name: str, shop_name: str) -> str:
        if shop_name == "Seeds":
            for item in self.seed_shop:
                if item["name"] == item_name:
                    return f"{item["name"]}\t{item["value"]}"
        elif shop_name == "Gears":
            for item in self.seed_shop:
                if item["name"] == item_name:
                    return f"{item["name"]}\t{item["value"]}"
        else:
            raise Exception("Shop doesn't exist")

    def get_items(self, shop: list, config=set()) -> str:
        items = set()
        if config:
            for item in shop:
                if item["name"] in config:
                    items.add(f"{item["name"]} — {item["value"]}")
        else:
            for item in shop:
                items.add(f"{item["name"]} — {item["value"]}")
        return "\n".join(items)

    def json(self):
        return {"seed_shop_items": self.seed_shop_items,
                "gear_shop_items": self.gear_shop_items,
                "seed_shop": self.seed_shop,
                "gear_shop": self.gear_shop,
                "egg_shop": self.egg_shop,
                "next_refresh": self.next_refresh,
                "eggs_refresh": self.eggs_refresh,
                "category_refresh_status": self.category_refresh_status}

    def __repr__(self):
        seeds = f"Seeds:\n{self.get_items(self.seed_shop)}"
        gears = f"Gears:\n{self.get_items(self.gear_shop)}"
        eggs = f"Eggs:\n{self.get_items(self.egg_shop)}"
        return "\n\n".join([seeds, gears, eggs])

    def __str__(self):
        return self.__repr__()
