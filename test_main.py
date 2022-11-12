from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def post_api():
    response = client.post("/api/product_type",
                           json={
                            "type_token":"TYPE221112213540eb0c",
                            "type_name":"二手書籍"
                            })
    assert response.status_code == 200
    assert response.text == "1|OK"


post_api()