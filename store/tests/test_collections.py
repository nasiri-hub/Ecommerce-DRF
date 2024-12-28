from model_bakery import baker
import pytest
from rest_framework import status
from store.models import Collection


@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/collections/', collection)
    return do_create_collection


@pytest.mark.django_db
class TestCreateCollection:

    def test_if_user_is_anonymous_returns_401(self, create_collection):

        response = create_collection({'title': 'a'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, create_collection, authenticate):

        authenticate()

        response = create_collection({'title': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, authenticate, create_collection):

        authenticate(is_staff=True)

        response = create_collection({'title': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_returns_201(self, authenticate, create_collection):

        authenticate(is_staff=True)

        response = create_collection({'title': 'a'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveCollection:

    def test_if_collection_exists_returns_200(self, api_client):
        collection = baker.make(Collection)
        response = api_client.get(f'/collections/{collection.id}/')

        assert response.status_code == status.HTTP_200_OK

        assert response.data == {
            'id': collection.id,
            'title': collection.title,
            'product_count': 0
        }

    def test_if_collection_is_not_exists_returns_404(self, api_client):

        response = api_client.get(f'/collections/0/')

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data is not None


@pytest.mark.django_db
class TestUpdateCollection:

    def test_if_user_is_anonymous_returns_401(self, api_client):
        collection = baker.make(Collection)
        response = api_client.put(
            f'/collections/{collection.id}/', data={'title': 'a'})
        # Assertion
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_return_403(self, api_client, authenticate):

        collection = baker.make(Collection)
        authenticate()
        response = api_client.put(
            f'/collections/{collection.id}/', data={'title': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_return_400(self, api_client, authenticate):

        collection = baker.make(Collection)
        authenticate(is_staff=True)
        response = api_client.put(
            f'/collections/{collection.id}/', data={'title': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_return_200(self, api_client, authenticate):

        collection = baker.make(Collection)
        authenticate(is_staff=True)
        response = api_client.put(
            f'/collections/{collection.id}/', data={'title': 'a'})

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestDeleteCollection:
    def test_if_collection_deleted_return_204(self, api_client, authenticate):
        authenticate(is_staff=True)
        collection = baker.make(Collection)

        response = api_client.delete(f'/collections/{collection.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
