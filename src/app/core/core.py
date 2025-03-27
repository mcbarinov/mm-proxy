from typing import Self

from mm_base6 import BaseCore, CoreConfig

from app.core.db import Db
from app.core.services.proxy_service import ProxyService
from app.core.services.source_service import SourceService
from app.settings import DConfigSettings, DValueSettings


class Core(BaseCore[DConfigSettings, DValueSettings, Db]):
    proxy_service: ProxyService
    source_service: SourceService

    @classmethod
    async def init(cls, core_config: CoreConfig) -> Self:
        res = await super().base_init(core_config, DConfigSettings, DValueSettings, Db)
        res.proxy_service = ProxyService(res.base_service_params)
        res.source_service = SourceService(res.base_service_params)
        return res

    def configure_scheduler(self) -> None:
        self.scheduler.add_task("proxy_check", 1, self.proxy_service.check_next)
        self.scheduler.add_task("source_check", 60, self.source_service.check_next)
