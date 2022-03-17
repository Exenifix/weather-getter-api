import aiohttp
import pytest


class TestAPI:
    @pytest.mark.asyncio
    async def test_api(self):
        async with aiohttp.ClientSession("http://localhost:5001") as session:
            r = await session.get("/weather", params={"city": "Moscow"})
            assert r.status == 200


if __name__ == "__main__":
    pytest.main()
