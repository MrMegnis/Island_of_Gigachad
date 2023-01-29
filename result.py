from result_menu import ResultMenu


class Result:
    def __init__(self):
        self.inventory_size = 0
        self.enemies_killed = 0
        self.levels_passed = 0

    def reset(self):
        self.inventory_size = 0
        self.enemies_killed = 0
        self.levels_passed = 0

    def get_result_menu(self, height, width, ok_btn_func):
        stats = {
            "inventory_size": self.inventory_size,
            "enemies_killed": self.enemies_killed,
            "levels_passed": self.levels_passed
        }
        result_menu = ResultMenu(height, width, ok_btn_func, stats)
        return result_menu
