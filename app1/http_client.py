import httpx
from typing import Any, Generator
from contextlib import contextmanager

from data_models import Item, ItemPartial


class Client:
    @contextmanager
    def request(self) -> Generator[httpx.Client, Any, None]:
        with httpx.Client(
                base_url="https://api.restful-api.dev/objects",
        ) as client:
            yield client

    def create(self, item: Item) -> httpx.Response:
        with self.request() as request:
            return request.post(
                url='',
                json=item.model_dump()
            )

    def get(self, _id: int) -> httpx.Response:
        with self.request() as request:
            return request.get(
                url=f"{_id}",
            )

    def put(self, _id: int, item: Item) -> httpx.Response:
        with self.request() as request:
            return request.put(
                url=f"{_id}",
                json=item.model_dump(),
            )

    def patch(self, _id: int, item: ItemPartial):
        with self.request() as request:
            return request.put(
                url=f"{_id}",
                json=item.model_dump(exclude_none=True, exclude_unset=True),
            )

    def delete(self, _id: int) -> httpx.Response:
        with self.request() as request:
            return request.delete(
                url=f"{_id}",
            )
