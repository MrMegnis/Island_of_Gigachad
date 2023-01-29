from result_menu import ResultMenu


class Result:
    def __init__(self):
        self.inventory_size = 0
        self.inventory = None
        self.enemies_killed = 0
        self.levels_passed = -1

    def reset(self):
        self.inventory_size = 0
        self.inventory = self.inventory
        self.enemies_killed = 0
        self.levels_passed = -1

    def get_result_menu(self, height, width, ok_btn_func):
        stats = {
            "inventory_size": self.inventory.get_inventory_size(),
            "items_left": self.inventory.get_items_amount(),
            "enemies_killed": self.enemies_killed,
            "levels_passed": self.levels_passed
        }
        result_menu = ResultMenu(height, width, ok_btn_func, stats)
        return result_menu
