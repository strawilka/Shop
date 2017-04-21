class DuplicationError(Exception):
    pass


class CompatibilityError(Exception):
    pass


class ResourceError(Exception):
    def __init__(self, equip):
        Exception.__init__(self, "Player doesn't have enough resources to buy {}!".format(equip))


class Player(object):
    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)


class Shop(object):
    """Shop class providing methods to manipulate player's equipment"""

    def __init__(self, equipment):
        """
        Args:
            equipment (dict): DB of the game equipment in the following format:

                'planes': {
                    <plane_id:int>: {
                        'price': {<game_currency:str>: <amount:int>, ...},
                        'compatible_guns': {<gun_id:int>, ...}
                    },
                    ...
                },
                'guns': {
                    <gun_id:int>: {
                        'price': {<game_currency:str>: <amount:int>, ...}
                    },
                    ...
                }
        """
        self.db = equipment

    def check_resources(self, item_price, player_resources):
        resource = list(item_price.keys())[0]
        return resource if player_resources[resource] >= item_price[resource] else False

    def get_planes(self):
        return self.db['planes']

    def get_guns(self):
        return self.db['guns']

    def buy_plane(self, player, plane_id):
        """Buy plane with ID `plane_id` for player `player` and update player's
        data as necessary.

        Args:
            player(dict): player's data in the following format:

                'id': <player_id:int>,
                'resources': {<game_currency:str>: <amount:int>, ...},
                'planes': {
                    <plane_id:int>: {'gun': <gun_id:int>},
                    ...
                }

            plane_id(int): Id of plane to buy

        Returns: None
        """
        player = Player(player)
        if plane_id in player.planes:
            raise DuplicationError("The player with id {} has already have the plane {}".format(player.id, plane_id))

        # add plane to players planes
        plane_price = self.get_planes()[plane_id]['price']
        buy = self.check_resources(plane_price, player.resources)
        if buy:
            player.planes[plane_id] = {'gun': None}
            player.resources[buy] -= plane_price[buy]
        else:
            raise ResourceError("plane {}".format(plane_id))

    def buy_gun(self, player, plane_id, gun_id):
        """Buy gun with ID `gun_id` for player `player` and update player's
        data as necessary.

        Args:
            player(dict): Player's data
            plane_id(int): Id of plane to buy gun for
            gun_id(int): Id of gun to buy

        Returns: None
        """
        player = Player(player)

        # compatible planes for gun which user want to buy
        compatible_planes = [plane for plane in self.get_planes()
                             if gun_id in self.get_planes()[plane]['compatible_guns']]

        if plane_id not in player.planes:
            raise CompatibilityError("Can't buy the gun because player doesn't have compatible plane")

        if plane_id not in compatible_planes:
            raise CompatibilityError("The gun and the plane are not compatible!")

        # if the gun and the plane are compatible check if the gun already exist
        if player.planes[plane_id]['gun'] == gun_id:
            raise DuplicationError('The gun {} is already set to plane'.format(gun_id))

        # buy new gun
        gun_price = self.get_guns()[gun_id]['price']
        buy = self.check_resources(gun_price, player.resources)
        if buy:
            player.planes[plane_id]['gun'] = gun_id
            player.resources[buy] -= gun_price[buy]
        else:
            raise ResourceError("gun {}".format(gun_id))