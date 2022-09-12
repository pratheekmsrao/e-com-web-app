from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

# from sqlalchemy.sql.functions import func
from .. import models, oauth2, schemas
from ..database import get_db

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get("/", response_model=List[schemas.CartProductOut])
def get_cart_items(
    db: Session = Depends(get_db),
    current_user: object = Depends(oauth2.get_current_user),
) -> List[schemas.CartProductOut]:
    """
    get list of cart items
    :param db: SqlAlchemy db object
    :param current_user: current logged-in user
    :return: list of cart items for a logged in user
    """
    cart_item = (
        db.query(models.Cart).filter(models.Cart.user_id == current_user.id).all()
    )
    return cart_item


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.CartProductOut
)
def add_item_to_cart(
    item: schemas.AddToCart,
    db: Session = Depends(get_db),
    current_user: object = Depends(oauth2.get_current_user),
) -> schemas.CartProductOut:
    """
    add new product to the cart.
    check if the product is available in inventory and check if the quantity is less than available product quantity.
    if the product is not already in the cart, then product is added to the cart
    :param item: items details: product_id, quantity
    :param db: SqlAlchemy db object
    :param current_user: current logged-in user
    :return: returns the added product
    """
    product = (
        db.query(models.Product)
        .filter(
            models.Product.id == item.product_id, models.Product.inventory_count > 0
        )
        .first()
    )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"product with id: {item.product_id} does not exist",
        )

    item_query = db.query(models.Cart).filter(
        models.Cart.product_id == item.product_id,
        models.Cart.user_id == current_user.id,
    )

    found_item = item_query.first()
    if found_item:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"user {current_user.username} has alredy added on product {item.product_id} to cart",
        )

    if product.inventory_count < item.quantity:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ordered quantity is greater than inventory quantity, Enter quantity below {product.inventory_count+1}",
        )

    else:
        new_item = models.Cart(user_id=current_user.id, **item.dict())
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        # return {"message": "Item added to Cart"}
        return new_item


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: object = Depends(oauth2.get_current_user),
) -> Response:
    """
    delete product from the cart by product id
    :param product_id: product id
    :param db: SqlAlchemy db object
    :param current_user: current logged-in user
    :return: status code
    """
    item_query = db.query(models.Cart).filter(models.Cart.product_id == product_id)

    item = item_query.first()

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"product with id: {product_id} does not exist",
        )

    if item.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    item_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(
    "/{product_id}",
    response_model=schemas.CartProductOut,
    status_code=status.HTTP_202_ACCEPTED,
)
def update_cart(
    product_id: int,
    updated_item: schemas.UpdateCart,
    db: Session = Depends(get_db),
    current_user: object = Depends(oauth2.get_current_user),
) -> schemas.CartProductOut:
    """
    update product in the cart.
    check if the product is available in inventory and check if the quantity is less than available product quantity.
    if the product is not already in the cart, then product is updated in the cart
    :param product_id: product id
    :param updated_item: product quantity to be updated
    :param db: SqlAlchemy db object
    :param current_user: current logged-in user
    :return: updated product
    """
    product = (
        db.query(models.Product)
        .filter(models.Product.id == product_id, models.Product.inventory_count > 0)
        .first()
    )

    item_query = db.query(models.Cart).filter(
        models.Cart.product_id == product_id, models.Cart.user_id == current_user.id
    )

    item = item_query.first()

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"product with id: {product_id} does not exist",
        )
    if item.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    if product.inventory_count < updated_item.quantity:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Update quantity is greater than inventory quantity, Enter quantity below {product.inventory_count+1}",
        )

    item_query.update(updated_item.dict(), synchronize_session=False)

    db.commit()

    return item_query.first()
