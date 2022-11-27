from rest_framework.views import APIView

from core.settings import API_SECRET_KEY

from rest_framework.response import Response

from django.shortcuts import redirect

from rest_framework import status
import os

import stripe
# This is your test secret API key.
stripe.api_key = API_SECRET_KEY


class StripeCheckoutView(APIView):
    def post(self, request):
        print(request.build_absolute_uri())
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price': 'price_1M8f4BFf4PxPl0wscWiXkmGV',
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=request.build_absolute_uri() + '?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=request.build_absolute_uri() + '?canceled=true',
            )
            return redirect(checkout_session.url)
        except Exception as e:
            return Response(
                {"error": "Something went wrong when creating stripe checkout session"},status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        
