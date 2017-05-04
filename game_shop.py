class DuplicationError(Exception):
    pass


class CompatibilityError(Exception):
    pass


class ResourceError(Exception):
    def __init__(self, equip):
        Exception.__init__(self, "Player doesn't have enough resources to buy {}!".format(equip))


class Shop(object):
    """Shop class providing methods to manipulate player's equipment"""

    def __init__(self, equipment):
        self.db = equipment

    def check_resources(self, player, item_price):
        for res, value in item_price.items():
            return not (player['resources'].get(res, 0) <= item_price[res])
        return True

    def write_off(self, player, item_price):
        for k, v in item_price.items():
            player['resources'][k] -= item_price[k]

    def get_planes(self):
        return self.db['planes']

    def get_guns(self):
        return self.db['guns']

    def buy_plane(self, player, plane_id):

        if plane_id in player['planes']:
            raise DuplicationError("The player with id {} has already have the plane {}".format(player, plane_id))

        # add plane to players planes
        plane_price = self.get_planes()[plane_id]['price']
        if self.check_resources(player, plane_price):
            player['planes'][plane_id] = {'gun': None}
            self.write_off(player, plane_price)
        else:
            raise ResourceError("plane {}".format(plane_id))

    def buy_gun(self, player, plane_id, gun_id):

        if plane_id not in player['planes']:
            raise CompatibilityError("Can't buy the gun because player doesn't have compatible plane")

        if gun_id not in self.get_planes()[plane_id]['compatible_guns']:
            raise CompatibilityError("The gun and the plane are not compatible!")

        if player['planes'][plane_id]['gun'] == gun_id:
            raise DuplicationError('The gun {} is already set to plane'.format(gun_id))

        gun_price = self.get_guns()[gun_id]['price']
        if self.check_resources(player, gun_price):
            player['planes'][plane_id]['gun'] = gun_id
            self.write_off(player, gun_price)
        else:
            raise ResourceError("gun {}".format(gun_id))