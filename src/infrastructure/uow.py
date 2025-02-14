from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.uow import AbstractUnitOfWork


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repositories = {}

    async def commit(self):
        try:
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise e

    async def rollback(self):
        await self.session.rollback()
