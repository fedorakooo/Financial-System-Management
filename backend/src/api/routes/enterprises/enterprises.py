from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from src.dependencies.enterprises import EnterpriseDependencies
from src.dependencies.logs import LogDependencies
from src.domain.schemas.enterprise import EnterpriseCreate, EnterpriseRead, EnterpriseUpdate
from src.services.enterprises.enterprise import EnterpriseService
from src.domain.exceptions.repository import (
    NotFoundError,
    UniqueConstraintError,
    NoFieldsToUpdateError
)
from src.services.logs.log import LogService

router = APIRouter(prefix="/enterprises", tags=["Enterprises"])


@router.get("/{enterprise_id}", response_model=EnterpriseRead, responses={
    404: {"description": "Enterprise not found"},
    500: {"description": "Unexpected server error"}
})
async def get_enterprise_by_id(
        enterprise_id: int,
        enterprise_service: EnterpriseService = Depends(EnterpriseDependencies.get_enterprise_service),
        log_service: LogService = Depends(LogDependencies.get_log_service)
) -> EnterpriseRead:
    try:
        enterprise = await enterprise_service.get_enterprise_by_id(enterprise_id)
        log_service.info(f"Successfully fetched enterprise with ID {enterprise}")
    except NotFoundError as e:
        log_service.warning(f"Enterprise with ID {enterprise_id} not found: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        log_service.error(f"Unexpected error fetching enterprise with ID {enterprise_id}: {str(e)}")
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
        log_service: LogService = Depends(LogDependencies.get_log_service)
) -> List[EnterpriseRead]:
    try:
        enterprises = await enterprise_service.get_enterprises()
        log_service.info(f"Successfully fetched {len(enterprises)} enterprises")
    except Exception as e:
        log_service.error(f"Unexpected error fetching enterprises: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching the list of enterprises."
        )
    return enterprises


@router.post("/", response_model=EnterpriseRead, responses={
    409: {"description": "Enterprise with this name already exists"},
    500: {"description": "Unexpected server error"}
})
async def create_enterprise(
        enterprise_create: EnterpriseCreate,
        enterprise_service: EnterpriseService = Depends(EnterpriseDependencies.get_enterprise_service),
        log_service: LogService = Depends(LogDependencies.get_log_service)
) -> EnterpriseRead:
    log_service.info(f"Creating bank with name {enterprise_create.name}")
    try:
        created_enterprise = await enterprise_service.create_enterprise(enterprise_create)
        log_service.info(
            f"Enterprise with name {created_enterprise.name} and ID {created_enterprise.id} successfully created"
        )
    except UniqueConstraintError as e:
        log_service.error(
            f"Unique constraint violation while creating enterprise with name {enterprise_create.name}: {str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        log_service.error(
            f"An unexpected error occurred while creating the enterprise with name {enterprise_create.name}: {str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the enterprise."
        )
    return created_enterprise


@router.patch("/{enterprise_id}", response_model=EnterpriseRead, responses={
    404: {"description": "Enterprise not found"},
    400: {"description": "No fields to update"},
    409: {"description": "Conflict due to a unique constraint violation"},
    500: {"description": "Unexpected server error"}
})
async def update_enterprise_by_id(
        enterprise_id: int,
        enterprise_update: EnterpriseUpdate,
        enterprise_service: EnterpriseService = Depends(EnterpriseDependencies.get_enterprise_service),
        log_service: LogService = Depends(LogDependencies.get_log_service)
) -> EnterpriseRead:
    log_service.info(f"Updating enterprise with ID {enterprise_id}")
    try:
        updated_enterprise = await enterprise_service.update_enterprise_by_id(enterprise_id, enterprise_update)
        log_service.info(f"Bank with ID {enterprise_id} successfully updated")
    except NotFoundError as e:
        log_service.error(f"Enterprise with ID {enterprise_id} not found for update: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except NoFieldsToUpdateError as e:
        log_service.error(f"No fields to update for enterprise with ID {enterprise_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except UniqueConstraintError as e:
        log_service.error(f"Unique constraint violation while updating enterprise with ID {enterprise_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        log_service.error(
            f"An unexpected error occurred while updating the enterprise with ID {enterprise_id}: {str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while updating the enterprise with id {enterprise_id}."
        )
    return updated_enterprise


@router.delete("/{enterprise_id}", response_model=dict, status_code=status.HTTP_200_OK, responses={
    404: {"description": "Enterprise not found"},
    500: {"description": "Unexpected server error"}
})
async def delete_enterprise_by_id(
        enterprise_id: int,
        enterprise_service: EnterpriseService = Depends(EnterpriseDependencies.get_enterprise_service),
        log_service: LogService = Depends(LogDependencies.get_log_service)
) -> dict:
    log_service.info(f"Deleting enterprise with ID {enterprise_id}")
    try:
        await enterprise_service.delete_enterprise_by_id(enterprise_id)
        log_service.info(f"Enterprise with ID {enterprise_id} deleted successfully")
    except NotFoundError as e:
        log_service.warning(f"Enterprise with ID {enterprise_id} not found for deletion: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        log_service.error(
            f"An unexpected error occurred while deleting the enterprise with ID {enterprise_id}: {str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while deleting the enterprise with id {enterprise_id}."
        )
    return {"message": "Enterprise deleted successfully"}
