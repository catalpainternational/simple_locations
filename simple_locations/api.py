from ninja import NinjaAPI

from simple_locations.router import router

api = NinjaAPI()
api.add_router("/simple_locations/", router)
