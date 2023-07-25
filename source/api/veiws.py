from fastapi import APIRouter, status, Depends, HTTPException


from source.api.schemas import UserReadSchema, DigestSchema
from source.api.services import UserService, DigestService
from source.api.schemas import DigestSchema
from source.api.models import Digest


router = APIRouter(prefix='/api')


@router.get('/users/{user_id}', response_model=UserReadSchema, status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int) -> UserReadSchema:
    return await UserService.get_user_or_404(user_id)


@router.post('/generate_digest/{user_id}', response_model=DigestSchema, status_code=201)
async def generate_digest(user_id: int, digest_service: DigestService = Depends(DigestService)) -> DigestSchema:
    try:
        digest = await digest_service.generate_digest(user_id)
        return digest

    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)




