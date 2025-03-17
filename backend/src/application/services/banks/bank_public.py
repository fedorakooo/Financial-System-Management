from src.application.abstractions.banks.bank_public import AbstractBankPublicService
from src.application.dtos.bank import BankReadDTO
from src.application.mappers.bank import BankMapper
from src.domain.abstractions.database.repositories.banks import AbstractBankRepository


class BankPublicService(AbstractBankPublicService):
    def __init__(self, repository: AbstractBankRepository):
        self.repository = repository

    async def get_bank_by_id(self, bank_id: int) -> BankReadDTO:
        bank = await self.repository.get_bank_by_id(bank_id)
        bank_dto = BankMapper.map_bank_to_bank_read_dto(bank)
        return bank_dto

    async def get_banks(self) -> list[BankReadDTO]:
        banks = await self.repository.get_banks()
        banks_dto = [BankMapper.map_bank_to_bank_read_dto(bank) for bank in banks]
        return banks_dto
