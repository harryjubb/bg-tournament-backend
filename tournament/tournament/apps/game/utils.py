import requests
import xmltodict

import datetime


def _cast_if_not_none(num, cast_func=int):
    if num:
        return cast_func(num)
    return None


def _mins_to_timedelta(mins):
    return datetime.timedelta(minutes=int(mins))


def get_bgg_data(bgg_id):

    try:
        result = requests.get(
            f"https://api.geekdo.com/xmlapi2/thing?id={bgg_id}&stats=1"
        )
    except Exception:
        return {}

    result_dict = xmltodict.parse(result.content)

    item = result_dict.get("items", {}).get("item", {})

    item_data = {
        "bgg_id": bgg_id,
        "url": f"https://boardgamegeek.com/boardgame/{bgg_id}",
        "complexity": _cast_if_not_none(
            item.get("statistics", {})
            .get("ratings", {})
            .get("averageweight", {})
            .get("@value", None),
            float,
        ),
        "game_type": item.get("@type", None),
        "image_url": item.get("image", None),
        "min_age": _cast_if_not_none(item.get("minage", {}).get("@value", None), int),
        "name": [
            name["@value"]
            for name in item.get("name", [])
            if name["@type"] == "primary"
        ][0]
        if type(item["name"]) == list
        else item.get("name", {}).get("@value", None),
        "min_players": _cast_if_not_none(
            item.get("minplayers", {}).get("@value", None), int
        ),
        "max_players": _cast_if_not_none(
            item.get("maxplayers", {}).get("@value", None), int
        ),
        "min_length": _cast_if_not_none(
            item.get("minplaytime", {}).get("@value", None), _mins_to_timedelta
        ),
        "max_length": _cast_if_not_none(
            item.get("maxplaytime", {}).get("@value", None), _mins_to_timedelta
        ),
        "rating": _cast_if_not_none(
            item.get("statistics", {})
            .get("ratings", {})
            .get("average", {})
            .get("@value", None),
            float,
        ),
    }

    return item_data
