from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from src.dependencies.banks import BankDependencies
from src.domain.schemas.bank import BankCreate, BankRead, BankUpdate
from src.services.banks.bank import BankService
from src.domain.exceptions.repository import (
    NotFoundError,
    UniqueConstraintError,
    NoFieldsToUpdateError
)

router = APIRouter(prefix="/banks", tags=["Banks"])


@router.get("/{bank_id}", response_model=BankRead, responses={
    404: {"description": "Bank not found"},
    500: {"description": "Unexpected server error"}
})
async def get_bank_by_id(
        bank_id: int,
        bank_service: BankService = Depends(BankDependencies.get_bank_service)
) -> BankRead:
    try:
        bank = await bank_service.get_bank_by_id(bank_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
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
) -> List[BankRead]:
    try:
        result = await bank_service.get_banks()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching the list of banks."
        )
    return result


@router.post("/", response_model=BankRead, responses={
    409: {"description": "Bank with this name already exists"},
    500: {"description": "Unexpected server error"}
})
async def create_bank(
        bank_create: BankCreate,
        bank_service: BankService = Depends(BankDependencies.get_bank_service)
) -> BankRead:
    try:
        result = await bank_service.create_bank(bank_create)
    except UniqueConstraintError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the bank."
        )
    return result


@router.patch("/{bank_id}", response_model=BankRead, responses={
    404: {"description": "Bank not found"},
    400: {"description": "No fields to update"},
    409: {"description": "Conflict due to a unique constraint violation"},
    500: {"description": "Unexpected server error"}
})
async def update_bank_by_id(
        bank_id: int,
        bank_update: BankUpdate,
        bank_service: BankService = Depends(BankDependencies.get_bank_service)
) -> BankRead:
    try:
        result = await bank_service.update_bank_by_id(bank_id, bank_update)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except NoFieldsToUpdateError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except UniqueConstraintError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while updating the bank with id {bank_id}."
        )

    return result


@router.delete("/{bank_id}", response_model=dict, status_code=status.HTTP_200_OK, responses={
    404: {"description": "Bank not found"},
    500: {"description": "Unexpected server error"}
})
async def delete_bank_by_id(
        bank_id: int,
        bank_service: BankService = Depends(BankDependencies.get_bank_service)
):
    try:
        await bank_service.delete_bank_by_id(bank_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while deleting the bank with id {bank_id}."
        )
    return {"message": "Bank deleted successfully"}
