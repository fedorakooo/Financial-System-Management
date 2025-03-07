from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from src.dependencies.banks import BankDependencies
from src.dependencies.logs import LogDependencies
from src.domain.schemas.bank import BankCreate, BankRead, BankUpdate
from src.services.banks.bank import BankService
from src.domain.exceptions.repository import (
    NotFoundError,
    UniqueConstraintError,
    NoFieldsToUpdateError
)
from src.services.logs.log import LogService

router = APIRouter(prefix="/banks", tags=["Banks"])


@router.get("/{bank_id}", response_model=BankRead, responses={
    404: {"description": "Bank not found"},
    500: {"description": "Unexpected server error"}
})
async def get_bank_by_id(
        bank_id: int,
        bank_service: BankService = Depends(BankDependencies.get_bank_service),
        log_service: LogService = Depends(LogDependencies.get_log_service)
) -> BankRead:
    try:
        bank = await bank_service.get_bank_by_id(bank_id)
        log_service.info(f"Successfully fetched bank with ID {bank_id}")
    except NotFoundError as e:
        log_service.warning(f"Bank with ID {bank_id} not found: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        log_service.error(f"An unexpected error occurred while fetching the bank with ID {bank_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching the bank."
        )
    return bank


@router.get("/", response_model=List[BankRead], responses={
    500: {"description": "Unexpected server error"}
})
async def get_banks(
        bank_service: BankService = Depends(BankDependencies.get_bank_service),
        log_service: LogService = Depends(LogDependencies.get_log_service)
) -> List[BankRead]:
    try:
        banks = await bank_service.get_banks()
        log_service.info(f"Successfully fetched {len(banks)} banks")
    except Exception as e:
        log_service.error(f"An unexpected error occurred while fetching the list of banks: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching the list of banks."
        )
    return banks


@router.post("/", response_model=BankRead, responses={
    409: {"description": "Bank with this name already exists"},
    500: {"description": "Unexpected server error"}
})
async def create_bank(
        bank_create: BankCreate,
        bank_service: BankService = Depends(BankDependencies.get_bank_service),
        log_service: LogService = Depends(LogDependencies.get_log_service)
) -> BankRead:
    log_service.info(f"Creating bank with name {bank_create.name}")
    try:
        created_bank = await bank_service.create_bank(bank_create)
        log_service.info(f"Bank with name {created_bank.name} and ID {created_bank.id} successfully created")
    except UniqueConstraintError as e:
        log_service.error(
            f"Unique constraint violation while creating bank with name {bank_create.name}: {str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        log_service.error(
            f"An unexpected error occurred while creating the bank with name {bank_create.name}: {str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the bank."
        )
    return created_bank


@router.patch("/{bank_id}", response_model=BankRead, responses={
    404: {"description": "Bank not found"},
    400: {"description": "No fields to update"},
    409: {"description": "Conflict due to a unique constraint violation"},
    500: {"description": "Unexpected server error"}
})
async def update_bank_by_id(
        bank_id: int,
        bank_update: BankUpdate,
        bank_service: BankService = Depends(BankDependencies.get_bank_service),
        log_service: LogService = Depends(LogDependencies.get_log_service)
) -> BankRead:
    log_service.info(f"Updating bank with ID {bank_id}")
    try:
        updated_bank = await bank_service.update_bank_by_id(bank_id, bank_update)
        log_service.info(f"Bank with ID {bank_id} successfully updated")
    except NotFoundError as e:
        log_service.error(f"Bank with ID {bank_id} not found for update: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except NoFieldsToUpdateError as e:
        log_service.error(f"No fields to update for bank with ID {bank_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except UniqueConstraintError as e:
        log_service.error(f"Unique constraint violation while updating bank with ID {bank_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        log_service.error(f"An unexpected error while updating the bank with ID {bank_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while updating the bank with id {bank_id}."
        )
    return updated_bank


@router.delete("/{bank_id}", response_model=dict, status_code=status.HTTP_200_OK, responses={
    404: {"description": "Bank not found"},
    500: {"description": "Unexpected server error"}
})
async def delete_bank_by_id(
        bank_id: int,
        bank_service: BankService = Depends(BankDependencies.get_bank_service),
        log_service: LogService = Depends(LogDependencies.get_log_service)
) -> dict:
    log_service.info(f"Deleting bank with ID {bank_id}")
    try:
        await bank_service.delete_bank_by_id(bank_id)
        log_service.info(f"Bank with ID {bank_id} deleted successfully")
    except NotFoundError as e:
        log_service.warning(f"Bank with ID {bank_id} not found for deletion: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        log_service.error(f"An unexpected error while deleting the bank with ID {bank_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while deleting the bank with id {bank_id}."
        )
    return {"message": "Bank deleted successfully"}
