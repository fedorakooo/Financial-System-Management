from abc import abstractmethod, ABC


class AbstractUnitOfWork(ABC):
    @abstractmethod
    async def commit(self) -> None:
        pass

    @abstractmethod
    async def rollback(self) -> None:
        pass
