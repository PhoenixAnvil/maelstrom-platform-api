from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from maelstrom.db import get_db
from maelstrom.models.product import Product
from maelstrom.schemas.product import ProductCreate
from maelstrom.schemas.product import ProductOut

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=list[ProductOut])
async def list_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product))
    return result.scalars().all()


@router.post("/", response_model=ProductOut)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    new_product = Product(**product.dict())
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product
