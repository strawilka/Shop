import game_shop
import pytest

equipment = {
    'planes': {
        1001: {
            'price': {'credits': 100},
            'compatible_guns': {201}
        },
        1002: {
            'price': {'credits': 500},
            'compatible_guns': {202}
        },
        1003: {
            'price': {'gold': 50},
            'compatible_guns': {201, 202, 203, 204}
        },
        1004: {
            'price': {'credits': 150},
            'compatible_guns': {201, 202, 203, 204}
        },
        1005: {
            'price': {'credits': 10},
            'compatible_guns': {204}
        }
    },
    'guns': {
        201: {
            'price': {'credits': 10},
        },
        202: {
            'price': {'credits': 50},
        },
        203: {
            'price': {'gold': 5},
        },
        204: {
            'price': {'credits': 15},
        }
    }
}

player = {
    'id': 0,
    'resources': {
        'credits': 200,
        'gold': 2
    },
    'planes': {
        1001: {'gun': 201},
        1003: {'gun': 202}
    }
}

player2 = {
    'id': 0,
    'resources': {
        'credits': 200,
        'gold': 150
    },
    'planes': {
    }
}
shopping = game_shop.Shop(equipment)


def test_dupl_plane_error():
    with pytest.raises(game_shop.DuplicationError):
        shopping.buy_plane(player, 1001) is True


def test_buy_plane():
    shopping.buy_plane(player, 1004)
    assert player['planes'][1004]['gun'] is None


def test_buy_plane_resource_error():
    with pytest.raises(game_shop.ResourceError):
        shopping.buy_plane(player, 1002)


def test_buy_gun_resource_error():
    with pytest.raises(game_shop.ResourceError):
        shopping.buy_gun(player, 1003, 203)


#buy gun for not existed plane
def test_buy_gun_for_not_exist_plane():
    with pytest.raises(game_shop.CompatibilityError):
        shopping.buy_gun(player, 1002, 203)


#can't buy gun for plane which already has it
def test_buy_gun_existed():
    with pytest.raises(game_shop.DuplicationError):
        shopping.buy_gun(player, 1003, 202)


#buy_gun pass
def test_buy_gun():
    shopping.buy_gun(player, 1003, 204)
    assert player['planes'][1003]['gun'] == 204


def test_buy_gun_not_comp_to_plane():
    with pytest.raises(game_shop.CompatibilityError):
        shopping.buy_gun(player, 1001, 202)


def test_buy_gun_update_resources():
    res_in = player['resources']['credits']
    gun_price = equipment['guns'][201]['price']['credits']
    shopping.buy_gun(player, 1003, 201)
    assert player['resources']['credits'] == res_in - gun_price


def test_buy_plane_update_resources():
    res_in = player['resources']['credits']
    plane_price = equipment['planes'][1005]['price']['credits']
    shopping.buy_plane(player, 1005)
    assert player['resources']['credits'] == res_in - plane_price
