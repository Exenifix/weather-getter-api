from os import getenv

from aiohttp import ClientSession, web
from dotenv import load_dotenv
from exencolorlogs import Logger

load_dotenv()
APIKEY = getenv("APIKEY")
PORT = getenv("PORT")

app = web.Application()
route = web.RouteTableDef()
log = Logger()


@route.get("/weather")
async def get_weather(req: web.Request):
    log.info("Received weather request from %s", req.remote)
    try:
        city = req.rel_url.query["city"]
    except KeyError:
        log.warning("Request is mising city param")
        return web.json_response(
            {"error": '400 Invalid Form Body: missing "city" param'}, status=400
        )

    async with ClientSession() as session:
        r = await session.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": city, "appid": APIKEY, "units": "metric", "lang": "ru"},
        )
        data = await r.json()

    if r.status != 200:
        log.error("Internal server error")
        print(r.status)
        print(data)
        return web.Response(status=500)

    return web.json_response(data)


app.add_routes(route)
log.info("Running on port %s", PORT)
web.run_app(app, port=PORT)
