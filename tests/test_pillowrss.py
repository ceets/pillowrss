from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status


async def test_real_endpoint(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Checks the health endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    url = fastapi_app.url_path_for("get_rss", community_name="Gaming")
    response = await client.get(url)
    response_text = response.content.decode("utf8")
    assert response.status_code == status.HTTP_200_OK
