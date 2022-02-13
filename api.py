from os import getenv

from aiohttp import ClientSession, web
from dotenv import load_dotenv

load_dotenv()
APIKEY = getenv("APIKEY")
PORT = getenv("PORT")

app = web.Application()
route = web.RouteTableDef()


@route.get("/weather")
async def get_weather(req: web.Request):
    try:
        city = req.rel_url.query["city"]
    except KeyError:
        return web.Response(status=400)

    async with ClientSession() as session:
        r = await session.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": city, "appid": APIKEY, "units": "metric", "lang": "ru"},
        )
        data = await r.json()

    if r.status != 200:
        print(r.status)
        print(data)
        return web.Response(status=500)

    return web.json_response(data)


app.add_routes(route)
web.run_app(app, port=PORT)
