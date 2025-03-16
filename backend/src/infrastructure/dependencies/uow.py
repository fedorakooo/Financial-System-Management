from dependency_injector import containers, providers

from src.infrastructure.database.uow import UnitOfWork


class UnitOfWorkContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    gateways = providers.DependenciesContainer()

    uow = providers.Factory(
        UnitOfWork,
        db_connection=gateways.database_connection,
    )
