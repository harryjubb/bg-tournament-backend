import requests
import xmltodict


def get_bgg_data(bgg_id):

    try:
        result = requests.get(
            f"https://api.geekdo.com/xmlapi2/thing?id={bgg_id}&stats=1"
        )
    except Exception:
        return {}

    result_dict = xmltodict.parse(result.content)

    bgg_data = {
        "id": bgg_id,
        "url": f"https://boardgamegeek.com/boardgame/{id}",
        "difficulty": result_dict.get("statistics", {})
        .get("ratings", {})
        .get("averageweight", {})
        .get("_attributes", {})
        .get("value", None),
        "gameType": result_dict.get("_attributes", {}).get("type", None),
        "imageUrl": result_dict.get("image", {}).get("_text", None),
        "minimumAge": result_dict.get("minage", {})
        .get("_attributes", {})
        .get("value", None),
        "name": getName(result_dict),  # TODO: write py version
        "players": {
            "minimum": result_dict.get("minplayers", {})
            .get("_attributes", {})
            .get("value", None),
            "maximum": result_dict.get("maxplayers", {})
            .get("_attributes", {})
            .get("value", None),
        },
        "playtime": {
            "minimum": result_dict.get("minplaytime", {})
            .get("_attributes", {})
            .get("value", None),
            "maximum": result_dict.get("maxplaytime", {})
            .get("_attributes", {})
            .get("value", None),
        },
        "rating": result_dict.get("statistics", {})
        .get("ratings", {})
        .get("average", {})
        .get("_attributes", {})
        .get("value", None),
    }
