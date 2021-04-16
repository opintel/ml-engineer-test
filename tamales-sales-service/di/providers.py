from bp.product_service import ProductService
from data.feature_store import FeatureStore
from fastapi import Depends

path_to_store = ""

def feature_store_module(
) -> FeatureStore:
    return FeatureStore(path_to_store)


def product_service_module(
    feature_store: FeatureStore = Depends(feature_store_module),
) -> ProductService:
    return ProductService(feature_store)