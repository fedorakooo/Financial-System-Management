from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies import get_bank_service
from src.domain.schemas.bank import BankCreate, BankRead, BankUpdate
from src.services.banks.bank import BankService
from src.domain.exceptions.repository import (
    NotFoundError,
    UniqueConstraintError,
    NoFieldsToUpdateError
)

router = APIRouter(prefix="/banks", tags=["Banks"])


@router.get("/{bank_id:int}", response_model=BankRead)
async def get_bank_by_id(
        bank_id: int,
        service: BankService = Depends(get_bank_service)
) -> BankRead:
    try:
        bank = await service.get_bank_by_id(bank_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching the bank."
        )
    if not bank:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bank not found"
        )
    print(type(bank))
    return bank


@router.post("/create")
async def create_bank(
        bank_create: BankCreate,
        service: BankService = Depends(get_bank_service)
) -> BankRead:
    try:
        result = await service.create_bank(bank_create)
    except UniqueConstraintError as e:
        error_message = str(e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=error_message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the bank."
        )
    return result


@router.get("/all", response_model=List[BankRead])
async def get_all_banks(
        service: BankService = Depends(get_bank_service)
) -> List[BankRead]:
    try:
        result = await service.get_all_banks()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching the list of bank."
        )
    return result


@router.put("/{bank_id:int}/update", response_model=BankRead)
async def update_bank(
        bank_id: int,
        bank_update: BankUpdate,
        service: BankService = Depends(get_bank_service)
) -> BankRead:
    try:
        result = await service.update_bank_by_id(bank_id, bank_update)

    except NoFieldsToUpdateError as e:
        error_message = str(e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=error_message
        )

    except NotFoundError as e:
        error_message = str(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_message
        )

    except UniqueConstraintError as e:
        error_message = str(e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=error_message
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while updating the bank with id {bank_id}."
        )

    return result


@router.delete("/{bank_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def remove_bank(
        bank_id: int,
        service: BankService = Depends(get_bank_service)
):
    try:
        await service.delete_bank(bank_id)
    except NotFoundError as e:
        error_message = str(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while deleting the bank with id {bank_id}."
        )
