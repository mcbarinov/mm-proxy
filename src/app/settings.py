from fastapi import APIRouter
from mm_base6 import DC, CoreConfig, DynamicConfigsModel, DynamicValuesModel, ServerConfig

core_config = CoreConfig()

server_config = ServerConfig()
server_config.tags = ["source", "proxy"]
server_config.main_menu = {"/bot": "bot", "/sources": "sources", "/proxies": "proxies"}


class DynamicConfigs(DynamicConfigsModel):
    live_last_ok_minutes = DC(15, "live proxies only if they checked less than this minutes ago")
    proxies_check = DC(True, "enable periodic proxy check")
    max_proxies_check = DC(30, "max proxies to check in one iteration")
    proxy_check_timeout = DC(5.1, "timeout for proxy check")


class DynamicSettings(DynamicValuesModel):
    pass


def get_router() -> APIRouter:
    from app.server.routers import proxy_router, source_router, ui_router

    router = APIRouter()
    router.include_router(ui_router.router)
    router.include_router(source_router.router)
    router.include_router(proxy_router.router)
    return router
