from django.shortcuts import render
from onlineshop.serializers import OrderSerializer
from .models import Order

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from backend.settings import EMAIL_HOST_USER

# Create your views here.


class OrderView(APIView):
    def get(self, request):
        try:
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)

            return Response({
                'data': serializer.data,
                'message': "Orders Data Fetched Successfully"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': "Something Went Wrong Wile Fetching The Data"
            }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            data = request.data
            serializer = OrderSerializer(data=data)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': "Something Went Wrong"
                }, status=status.HTTP_400_BAD_REQUEST)

            subject = "New Order Is Placed"
            message = "Dear Customer" + " " + \
                data['customer_name'] + \
                " Your order is placed Now, Thank you for the Order!"
            email = data['customer_email']
            recipient_list = [email]
            send_mail(subject, message, EMAIL_HOST_USER,
                      recipient_list, fail_silently=True)
            serializer.save()

            return Response({
                'data': serializer.data,
                'message': "New Order is Placed Successfully"
            }, status=status.HTTP_201_CREATED)

        except:
            return Response({
                'data': {},
                'message': "Something Went Wrong in Creating Data"
            }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        try:
            data = request.data
            order1 = Order.objects.filter(id=data.get('id'))

            if not order1.exists():
                return Response({
                    'data': {},
                    'message': "This Order Not Found "
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = OrderSerializer(order1[0], data=data, partial=True)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': "Something Went Wrong"
                }, status=status.HTTP_502_BAD_GATEWAY)

            serializer.save()

            return Response({
                'data': serializer.data,
                'message': 'Order is Updated Successfully'
            }, status=status.HTTP_200_OK)

        except:
            return Response({
                'data': serializer.errors,
                'message': "Something Went Wrong"
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            data = request.data
            order1 = Order.objects.filter(id=data.get('id'))

            if not order1.exists():
                return Response({
                    'data': {},
                    'message': "This Order Not Found "
                }, status=status.HTTP_404_NOT_FOUND)

            order1[0].delete()
            return Response({
                'data': {},
                'message': 'Order is Deleted Successfully'
            }, status=status.HTTP_200_OK)

        except:
            return Response({
                'data': {},
                'message': "Something Went Wrong With Deleting Order"
            }, status=status.HTTP_400_BAD_REQUEST)
