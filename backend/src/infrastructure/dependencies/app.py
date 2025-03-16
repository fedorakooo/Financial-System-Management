from dependency_injector import containers, providers

from src.infrastructure.dependencies.core import Core
from src.infrastructure.dependencies.gateways import Gateways
from src.infrastructure.dependencies.repository import Repositories
from src.infrastructure.dependencies.services import Services
from src.infrastructure.dependencies.uow import UnitOfWorkContainer


class Application(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=["config.yml"])

    wiring_config = containers.WiringConfiguration(
        packages=["src.api"]
    )

    core = providers.Container(
        Core,
        config=config.core,
    )

    gateways = providers.Container(
        Gateways,
        config=config.gateways,
        core=core,
    )

    repositories = providers.Container(
        Repositories,
        config=config.repository,
        gateways=gateways,
    )

    uow = providers.Container(
        UnitOfWorkContainer,
        config=config.uow,
        gateways=gateways,
    )

    services = providers.Container(
        Services,
        config=config.services,
        repositories=repositories,
        core=core,
        uow=uow,
        gateways=gateways,
    )
