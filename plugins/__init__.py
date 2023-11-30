from aiohttp import web 
from info import API_ID, API_HASH, BOT_TOKEN

routes = web.RouteTableDef()


@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response("Lusifilms On Tg")

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app
