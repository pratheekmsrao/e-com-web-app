from typing import Dict, List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas
from ..database import get_db
from ..models import Product

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=List[schemas.Product])
def get_all_products(
        db: Session = Depends(get_db),
        limit: int = 10,
        skip: int = 0,
        search: Optional[str] = "",
) -> List[schemas.Product]:
    """
    List all the products
    :param db: SqlAlchemy db object
    :param limit: limit number of products
    :param skip: offset/ omit a specified number of rows before the beginning of the result
    :param search: search based on product name
    :return: list of products
    """
    products = (
        db.query(models.Product)
        .group_by(models.Product.id)
        .filter(models.Product.name.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return products


@router.get("/category/all", response_model=Dict[str, List[str]])
def get_all_category(db: Session = Depends(get_db)) -> Dict[str, List[List[Product]]]:
    """
    return the list of all product categories
    :param db: SqlAlchemy db object
    :return: list of all product categories
    """
    category = db.query(models.Product).distinct(models.Product.category).all()
    category_l = [i.category for i in category]
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No products and Category"
        )

    return {"category": category_l}


@router.get("/category/{category_name}", response_model=List[schemas.Product])
def get_products_by_category(category_name: str, db: Session = Depends(get_db)) -> List[schemas.Product]:
    """
    return the list of all product for the specified category
    :return:
    :param category_name: name of the category
    :param db: SqlAlchemy db object
    :return: List of product category
    """
    category = (
        db.query(models.Product)
        .group_by(models.Product.id)
        .filter(models.Product.category == category_name)
        .all()
    )
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Products with category: {category_name} was not found",
        )

    return category



@router.get("/sub_category/{sub_category_name}", response_model=List[schemas.Product])
def get_products_by_sub_category(sub_category_name: str, db: Session = Depends(get_db)) -> List[schemas.Product]:
    """
    return all the products for a given sub-category
    :param sub_category_name: name of the sub_category_name
    :param db: SqlAlchemy db object
    :return: return list of product category
    """
    sub_category = (
        db.query(models.Product)
        .group_by(models.Product.id)
        .filter(models.Product.sub_category == sub_category_name)
        .all()
    )

    if not sub_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Products with sub_category: {sub_category} was not found",
        )

    return sub_category



@router.get("/sub_category", response_model=Dict[str, Union[str, List[str]]])
def get_sub_category_for_category(category: str = "", db: Session = Depends(get_db)) -> Dict[str, Union[str, List[str]]]:
    """
    return the list of all the sub-categories for a given category
    :param category: name of the category
    :param db: SqlAlchemy db object
    :return: list of all the sub-categories for a given category
    """
    sub_category = (
        db.query(models.Product)
        .distinct(models.Product.sub_category)
        .filter(models.Product.category == category)
        .all()
    )
    sub_category_l = [i.sub_category for i in sub_category]
    if not sub_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No sub_category for the given category :{category}",
        )
    # return {'sub_category': sub_category_l}
    return {"category": category, "sub_category": sub_category_l}



@router.get("/{id}", response_model=schemas.Product)
def get_product_by_id(id: int, db: Session = Depends(get_db)) -> schemas.Product:
    """
    return product by id
    :param id: product id of the product
    :param db: SqlAlchemy db object
    :return: Product with all the product details
    """
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"product with id: {id} was not found",
        )
    return product
