from datetime import datetime
from model_bakery import baker
import pytest
from rest_framework import status
from store.models import Collection, Product, Promotion


@pytest.fixture
def create_product(api_client):
    def do_create_product(product):
        return api_client.post('/products/', data=product)
    return do_create_product


@pytest.mark.django_db
def create_data():
    collection = baker.make(Collection)

    return {
        'title': 'a',
        'slug': 'a',
        'description': 'aaa',
        'unit_price': 20,
        'inventory': 200,
        'last_update': datetime(2023, 2, 22),
        'collection': collection.id,
    }


@pytest.mark.django_db
class TestCreateProduct:

    def test_if_user_is_anonymous_return_401(self, create_product):

        response = create_product(create_data())

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticate, create_product):

        authenticate()

        response = create_product(create_data())

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_return_400(self, authenticate, create_product):

        authenticate(is_staff=True)

        response = create_product({'title': 'a'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_return_201(self, authenticate, create_product):
        authenticate(is_staff=True)

        response = create_product(create_data())

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveProduct:

    def test_if_product_exists_return_200(self, api_client):

        product = baker.make(Product)

        response = api_client.get(f'/products/{product.id}/')

        assert response.status_code == status.HTTP_200_OK
