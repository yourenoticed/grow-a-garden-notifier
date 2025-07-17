from time import localtime


class Stock():
    def __init__(self, data: dict):
        self.data = data
        self.gear_shop = self.get_shop("gear_stock")
        self.egg_shop = self.get_shop("egg_stock")
        self.cosmetics_shop = self.get_shop("cosmetic_stock")
        self.seed_shop = self.get_shop("seed_stock")

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
                if item["display_name"] not in shop:
                    shop[item["display_name"]] = item["quantity"]
                else:
                    shop[item["display_name"]] += 1
            return shop
        except:
            return dict()

    def json(self):
        return {
            "seed_shop": self.seed_shop,
            "gear_shop": self.gear_shop,
            "egg_shop": self.egg_shop,
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
            "gear_stock": list(),
            "egg_stock": list(),
            "cosmetic_stock": list(),
            "seed_stock": list()
        }
        for item in diff:
            if item in self.gear_shop:
                representation["gear_stock"].append(
                    {"display_name": item, "quantity": diff[item]})
            elif item in self.egg_shop:
                representation["egg_stock"].append(
                    {"display_name": item, "quantity": diff[item]})
            elif item in self.cosmetics_shop:
                representation["cosmetic_stock"].append(
                    {"display_name": item, "quantity": diff[item]})
            elif item in self.seed_shop:
                representation["seed_stock"].append(
                    {"display_name": item, "quantity": diff[item]})
        return representation

    def check_update(self, old_stock) -> str:
        if old_stock != self:
            curr_time = localtime()
            if curr_time.tm_hour % 4 == 3:
                return "cosmetics"
            if curr_time.tm_min % 30 == 0:
                return "eggs"
            if curr_time.tm_min % 5 == 0:
                return "stock"
        return "none"

    def get_current_stock_items(self) -> dict:
        all_items = dict()
        self._add_shop_to_current_stock(all_items, self.seed_shop)
        self._add_shop_to_current_stock(all_items, self.gear_shop)
        self._add_shop_to_current_stock(all_items, self.egg_shop)
        self._add_shop_to_current_stock(all_items, self.cosmetics_shop)
        return all_items

    def _add_shop_to_current_stock(self, current_stock: dict, stock_to_add: dict) -> dict:
        for item in stock_to_add:
            current_stock[item] = stock_to_add[item]

    def __repr__(self, config=set(), include_eggs=False, include_cosmetics=False) -> dict:
        shop_items = dict()
        shop_items["Seeds"] = self.get_items(self.seed_shop, config)
        shop_items["Gears"] = self.get_items(self.gear_shop, config)
        if include_eggs == True:
            shop_items["Eggs"] = self.get_items(self.egg_shop, config)
        if include_cosmetics == True:
            shop_items["Cosmetics"] = self.get_items(
                self.cosmetics_shop, config)
        return shop_items

    def length(self):
        return len(self.get_current_stock_items())

    def __eq__(self, new_stock) -> bool:
        return self.json() == Stock.json(new_stock)

    def __str__(self, config=set(), include_eggs=False, include_cosmetics=False) -> str:
        repr_dict = self.__repr__(
            config, include_eggs, include_cosmetics)
        return "\n\n".join([f"{shop_name}:\n{repr_dict[shop_name]}" for shop_name in repr_dict if len(repr_dict[shop_name]) > 0])
