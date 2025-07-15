from time import localtime


class Stock():
    def __init__(self, data: dict):
        self.data = data
        self.easter_shop = self.get_shop("easterStock")
        self.gear_shop = self.get_shop("gearStock")
        self.egg_shop = self.get_shop("eggStock")
        self.night_shop = self.get_shop("nightStock")
        self.honey_shop = self.get_shop("honeyStock")
        self.cosmetics_shop = self.get_shop("cosmeticsStock")
        self.seed_shop = self.get_shop("seedsStock")
        self.next_refresh = self.next_refresh_at()

    def next_refresh_at(self) -> dict[str, float]:
        try:
            curr_time = localtime()
            stock = (curr_time.tm_min - (curr_time.tm_min % 5)) % 60
            eggs = (curr_time.tm_min - (curr_time.tm_min % 30) + 30) % 60
            cosmetics = (curr_time.tm_hour - (curr_time.tm_hour % 4) + 4) % 24
            return {"stock": stock,
                    "eggs": eggs,
                    "cosmetics": cosmetics}
        except:
            return dict()

    def get_items(self, shop: dict, config=set()) -> str:
        items = list()
        if len(config) > 0:
            for item in shop:
                if item in config:
                    items.append(f"{item} — {shop[item]}")
        else:
            for item in shop:
                items.append(f"{item} — {shop[item]}")
        return "\n".join(items)

    def get_shop(self, shop_name: str) -> dict:
        try:
            shop = dict()
            for item in self.data[shop_name]:
                if item["name"] not in shop:
                    shop[item["name"]] = item["value"]
                else:
                    shop[item["name"]] += 1
            return shop
        except:
            return dict()

    def json(self):
        return {
            "seed_shop": self.seed_shop,
            "gear_shop": self.gear_shop,
            "egg_shop": self.egg_shop,
            "easter_shop": self.easter_shop,
            "night_shop": self.night_shop,
            "honey_shop": self.honey_shop,
            "cosmetics_shop": self.cosmetics_shop,
        }

    def find_diff(self, old_stock) -> dict:
        # theoretically, items can only appear in the new stock
        diff = dict()
        old_stock_items = Stock.get_current_stock_items(old_stock)
        new_stock_items = self.get_current_stock_items()
        for item in new_stock_items:
            if item not in old_stock_items:
                diff[item] = new_stock_items[item]
            else:
                if old_stock_items[item] < new_stock_items[item]:
                    diff[item] = new_stock_items[item] - old_stock_items[item]

        return self.diff_repr(diff)

    def diff_repr(self, diff: dict) -> dict:
        representation = {
            "easterStock": list(),
            "gearStock": list(),
            "eggStock": list(),
            "nightStock": list(),
            "honeyStock": list(),
            "cosmeticsStock": list(),
            "seedsStock": list()
        }
        for item in diff:
            if item in self.easter_shop:
                representation["easterStock"].append(
                    {"name": item, "value": diff[item]})
            elif item in self.gear_shop:
                representation["gearStock"].append(
                    {"name": item, "value": diff[item]})
            elif item in self.egg_shop:
                representation["eggStock"].append(
                    {"name": item, "value": diff[item]})
            elif item in self.night_shop:
                representation["nightStock"].append(
                    {"name": item, "value": diff[item]})
            elif item in self.honey_shop:
                representation["honeyStock"].append(
                    {"name": item, "value": diff[item]})
            elif item in self.cosmetics_shop:
                representation["cosmeticsStock"].append(
                    {"name": item, "value": diff[item]})
            elif item in self.seed_shop:
                representation["seedsStock"].append(
                    {"name": item, "value": diff[item]})

    def check_update(self, old_stock) -> str:
        if old_stock != self:
            curr_time = localtime()
            if curr_time.tm_hour % 4 == 1:
                return "cosmetics"
            if curr_time.tm_min % 30 == 0:
                return "eggs"
            if curr_time.tm_min % 5 == 0 and old_stock.next_refresh["stock"] != self.next_refresh["stock"]:
                return "stock"
        return "none"

    def get_current_stock_items(self) -> dict:
        all_items = dict()
        self._add_shop_to_current_stock(all_items, self.seed_shop)
        self._add_shop_to_current_stock(all_items, self.gear_shop)
        self._add_shop_to_current_stock(all_items, self.egg_shop)
        self._add_shop_to_current_stock(all_items, self.cosmetics_shop)
        self._add_shop_to_current_stock(all_items, self.easter_shop)
        self._add_shop_to_current_stock(all_items, self.night_shop)
        self._add_shop_to_current_stock(all_items, self.honey_shop)
        return all_items

    def _add_shop_to_current_stock(self, current_stock: dict, stock_to_add: dict) -> dict:
        for item in stock_to_add:
            current_stock[item] = stock_to_add[item]

    def __repr__(self, config=set(), include_eggs=False, include_cosmetics=False, include_easter=False, include_night=False, include_honey=False) -> dict:
        shop_items = dict()
        shop_items["Seeds"] = self.get_items(self.seed_shop, config)
        shop_items["Gears"] = self.get_items(self.gear_shop, config)
        if include_eggs == True:
            shop_items["Eggs"] = self.get_items(self.egg_shop, config)
        if include_cosmetics == True:
            shop_items["Cosmetics"] = self.get_items(
                self.cosmetics_shop, config)
        if include_easter == True:
            shop_items["Easter stock"] = self.get_items(
                self.easter_shop, config)
        if include_night == True:
            shop_items["Night stock"] = self.get_items(self.night_shop, config)
        if include_honey == True:
            shop_items["Honey stock"] = self.get_items(
                self.honey_shop, config)
        return shop_items

    def length(self):
        return len(self.get_current_stock_items())

    def __eq__(self, new_stock) -> bool:
        return self.json() == Stock.json(new_stock)

    def __str__(self, config=set(), include_eggs=False, include_cosmetics=False, include_easter=False, include_night=False, include_honey=False) -> str:
        repr_dict = self.__repr__(
            config, include_eggs, include_cosmetics, include_easter, include_night, include_honey)
        return "\n\n".join([f"{shop_name}:\n{repr_dict[shop_name]}" for shop_name in repr_dict if len(repr_dict[shop_name]) > 0])
