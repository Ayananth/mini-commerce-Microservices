import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from .serializers import OrderCreateSerializer, OrderSerializer

USER_SERVICE_URL = "http://user-service:8002/api/me/"
PRODUCT_SERVICE_URL = "http://product-service:8003/api/products/"


class OrderCreateView(APIView):
    def post(self, request):
        # 1. Validate input
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. Validate JWT via User Service
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return Response({"error": "Authorization header missing"}, status=401)

        user_response = requests.get(
            USER_SERVICE_URL,
            headers={"Authorization": auth_header},
            timeout=5
        )

        if user_response.status_code != 200:
            return Response({"error": "Invalid user"}, status=401)

        user_data = user_response.json()
        user_id = user_data["id"]

        # 3. Fetch product from Product Service
        product_id = serializer.validated_data["product_id"]
        quantity = serializer.validated_data["quantity"]

        product_response = requests.get(
            f"{PRODUCT_SERVICE_URL}{product_id}/",
            timeout=5
        )

        if product_response.status_code != 200:
            return Response({"error": "Invalid product"}, status=400)

        product_data = product_response.json()
        price = product_data["price"]

        total_price = float(price) * quantity

        # 4. Create order
        order = Order.objects.create(
            user_id=user_id,
            product_id=product_id,
            product_price=price,
            quantity=quantity,
            total_price=total_price
        )

        return Response(OrderSerializer(order).data, status=201)
