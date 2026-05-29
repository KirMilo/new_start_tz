from data_models import Item, ItemPartial
from http_client import Client

from random import randint


def main():
    item = Item(**{
        "name": "Item's name",
        "data": {
            "field_int": 1,
            "field_str": "Something here...",
        }
    })

    client = Client()
    response = client.create(item)  # 1
    response.raise_for_status()
    _id = response.json().get("id")

    try:
        response = client.get(_id)  # 2
        print(f"status code: {response.status_code}. result: {response.json()}")
    except:  # noqa
        pass

    try:
        if randint(0, 1):  # Рандомно выбираем каким методом обновляем item, через put или через patch.
            item.name = "Changed Item's name. Changed with put method."
            response = client.put(_id, item)
        else:
            response = client.patch(_id, ItemPartial(
                name="Changed Item's name. Changed with patch method."
            ))
        print(f"status code: {response.status_code}. {response.json()}")
    finally:
        client.delete(_id)   # 4
        response = client.get(_id)    # 5
        print(f"status code: {response.status_code}. {response.json()}")


if __name__ == "__main__":
    main()
