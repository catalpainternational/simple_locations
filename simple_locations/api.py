from ninja import NinjaAPI

from simple_locations.router import router

api = NinjaAPI(csrf=True)
api.add_router("/simple_locations/", router)
