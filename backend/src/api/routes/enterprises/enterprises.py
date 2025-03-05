from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from src.dependencies.enterprises import EnterpriseDependencies
from src.domain.schemas.enterprise import EnterpriseCreate, EnterpriseRead, EnterpriseUpdate
from src.services.enterprises.enterprise import EnterpriseService
from src.domain.exceptions.repository import (
    NotFoundError,
    UniqueConstraintError,
    NoFieldsToUpdateError
)

router = APIRouter(prefix="/enterprises", tags=["Enterprises"])


@router.get("/{enterprise_id}", response_model=EnterpriseRead, responses={
    404: {"description": "Enterprise not found"},
    500: {"description": "Unexpected server error"}
})
async def get_enterprise_by_id(
        enterprise_id: int,
        enterprise_service: EnterpriseService = Depends(EnterpriseDependencies.get_enterprise_service)
) -> EnterpriseRead:
    try:
        enterprise = await enterprise_service.get_enterprise_by_id(enterprise_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching the enterprise."
        )
    return enterprise


@router.get("/", response_model=List[EnterpriseRead], responses={
    500: {"description": "Unexpected server error"}
})
async def get_enterprises(
        enterprise_service: EnterpriseService = Depends(EnterpriseDependencies.get_enterprise_service),
) -> List[EnterpriseRead]:
    try:
        result = await enterprise_service.get_enterprises()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching the list of enterprises."
        )
    return result


@router.post("/", response_model=EnterpriseRead, responses={
    409: {"description": "Enterprise with this name already exists"},
    500: {"description": "Unexpected server error"}
})
async def create_enterprise(
        enterprise_create: EnterpriseCreate,
        enterprise_service: EnterpriseService = Depends(EnterpriseDependencies.get_enterprise_service)
) -> EnterpriseRead:
    try:
        result = await enterprise_service.create_enterprise(enterprise_create)
    except UniqueConstraintError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the enterprise."
        )
    return result


@router.patch("/{enterprise_id}", response_model=EnterpriseRead, responses={
    404: {"description": "Enterprise not found"},
    400: {"description": "No fields to update"},
    409: {"description": "Conflict due to a unique constraint violation"},
    500: {"description": "Unexpected server error"}
})
async def update_enterprise_by_id(
        enterprise_id: int,
        enterprise_update: EnterpriseUpdate,
        enterprise_service: EnterpriseService = Depends(EnterpriseDependencies.get_enterprise_service)
) -> EnterpriseRead:
    try:
        result = await enterprise_service.update_enterprise_by_id(enterprise_id, enterprise_update)
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
            detail=f"An unexpected error occurred while updating the enterprise with id {enterprise_id}."
        )

    return result


@router.delete("/{enterprise_id}", response_model=dict, status_code=status.HTTP_200_OK, responses={
    404: {"description": "Enterprise not found"},
    500: {"description": "Unexpected server error"}
})
async def delete_enterprise_by_id(
        enterprise_id: int,
        enterprise_service: EnterpriseService = Depends(EnterpriseDependencies.get_enterprise_service)
):
    try:
        await enterprise_service.delete_enterprise_by_id(enterprise_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while deleting the enterprise with id {enterprise_id}."
        )
    return {"message": "Enterprise deleted successfully"}
