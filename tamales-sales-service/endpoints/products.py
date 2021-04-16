import logging

from bp.product_service import ProductService
from di import providers
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response
from fastapi import status
from pydantic import BaseModel
from typing_extensions import Final

router = APIRouter()
STATUS: Final = "status"
OK: Final = "ok"


CODE = "code"
MESSAGE = "message"
ITEMS = "items"
PAGE = "page"


class Data(BaseModel):
    productid: str


@router.post("/apis/products/predict/1.0.0", tags=["products"])
async def predict_sales(
    data: Data,
    response: Response,
    product_service: ProductService = Depends(providers.product_service_module),
):
    try:
        product_id = data.productid

        predictions = product_service.predict(product_id)

        logging.info("Predictions:::: {}".format(predictions))

        return predictions
    except Exception as e:
        logging.error("Fatal error in predict_sales", exc_info=True)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {CODE: 500, MESSAGE: str(e)}
