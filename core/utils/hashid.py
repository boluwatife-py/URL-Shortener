from hashids import Hashids
from fastapi import HTTPException
from core.config import settings 

hashids = Hashids(salt=settings.HASHID_SALT, min_length=8)

class HashID:
    @staticmethod
    def encode(id: int) -> str:
        return hashids.encode(id)

    @staticmethod
    def decode(public_id: str) -> int:
        decoded = hashids.decode(public_id)
        if not decoded:
            raise HTTPException(status_code=400, detail="Invalid public ID")
        return decoded[0]
