from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

# from sqlalchemy.sql.functions import func
from .. import models, oauth2, schemas
from ..database import get_db

router = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.get("/", response_model=List[schemas.InventoryProduct])
def get_products(
    db: Session = Depends(get_db),
    current_user: object = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
) -> List[schemas.InventoryProduct]:
    """
    gets all products in the inventory
    :param db: SqlAlchemy db object
    :param current_user: current logged-in user
    :param limit: limit number of products
    :param skip: offset/ omit a specified number of rows before the beginning of the result
    :param search: list of products
    :return: list of products in inventory
    """
    if "invadmin" != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    products = (
        db.query(models.Product)
        .group_by(models.Product.id)
        .filter(models.Product.name.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return products


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.InventoryProduct
)
def create_product(
    product: schemas.InventoryProduct,
    db: Session = Depends(get_db),
    current_user: object = Depends(oauth2.get_current_user),
) -> schemas.InventoryProduct:
    """
    create new product in the inventory
    :param product: product details
    :param db: SqlAlchemy db object
    :param current_user: current logged-in user
    :return: returns the newly created product
    """
    if "invadmin" != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    new_product = models.Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@router.get("/{id}", response_model=schemas.InventoryProduct)
def get_product_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: object = Depends(oauth2.get_current_user),
) -> schemas.InventoryProduct:
    """
    return product by id
    :param id: product id of the product
    :param db: SqlAlchemy db object
    :param current_user: current logged-in user
    :return: returns product which matched the product id
    """
    if "invadmin" != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"product with id: {id} was not found",
        )
    return product


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    id: int,
    db: Session = Depends(get_db),
    current_user: object = Depends(oauth2.get_current_user),
) -> Response:
    """
    deletes the product by id
    :param id: product id of the product
    :param db: SqlAlchemy db object
    :param current_user: current logged-in user
    :return: status code 204
    """
    if "invadmin" != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    product_query = db.query(models.Product).filter(models.Product.id == id)

    product = product_query.first()

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"product with id: {id} does not exist",
        )

    product_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(
    "/{id}",
    response_model=schemas.InventoryProduct,
    status_code=status.HTTP_202_ACCEPTED,
)
def update_product(
    id: int,
    updated_product: schemas.InventoryProduct,
    db: Session = Depends(get_db),
    current_user: object = Depends(oauth2.get_current_user),
) -> schemas.InventoryProduct:
    """
    update the product by id
    :param id: product id of the product
    :param updated_product: updated product details
    :param db: SqlAlchemy db object
    :param current_user: current logged-in user
    :return: returns the updated product details
    """
    if "invadmin" != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    product_query = db.query(models.Product).filter(models.Product.id == id)

    product = product_query.first()

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"product with id: {id} does not exist",
        )

    product_query.update(updated_product.dict(), synchronize_session=False)

    db.commit()

    return product_query.first()
