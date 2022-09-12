from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import func
from sqlalchemy.orm import Session

# from sqlalchemy.sql.functions import func
from .. import models, oauth2
from ..database import get_db

router = APIRouter(prefix="/checkout", tags=["Check-out"])


@router.post("/", status_code=status.HTTP_200_OK)
def get_cart_items(
    db: Session = Depends(get_db),
    current_user: object = Depends(oauth2.get_current_user),
) -> JSONResponse:
    """
    mocks the check-out, checks the item in cart for the logged in user.
    if there are products, then checks out and deletes the record from cart
    :param db: SqlAlchemy db object
    :param current_user: current logged-in user
    :return: json response with a message
    """
    item_count = (
        db.query(
            models.Cart.user_id, func.count(models.Cart.product_id).label("no_products")
        )
        .group_by(models.Cart.user_id)
        .filter(models.Cart.user_id == current_user.id)
        .first()
    )
    # delete checkedout products in cart
    # TODO reduce the inventory quantity in product table
    item_query = db.query(models.Cart).filter(models.Cart.user_id == current_user.id)

    item = item_query.first()

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No items in cart for user {current_user.username}",
        )

    if item.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    item_query.delete(synchronize_session=False)
    db.commit()

    return JSONResponse(
        content={
            "message": f"{item_count.no_products} products checked out for user {item_count.user_id}"
        },
        status_code=status.HTTP_200_OK,
    )
