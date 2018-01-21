from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',)


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'password',
                  'contact_no',
                  )


# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ('id',
#                   'name',
#                   'cost',
#                   'description',
#                   'model_no',
#                   'brand',
#                   'image'
#                   )
#
#
# class OrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = (
#                   'user',
#                   'total_amt',
#                   'product',
#                   'product_count',
#                   'shipping_address',
#                   'billing_address'
#         )
#
#
# class BuyProductSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Order
#         fields = (
#             'product',
#             'product_count',
#             'shipping_address',
#             'billing_address',
#         )
#
#
# class AddressSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Address
#         fields = (
#             'address1',
#             'address2',
#             'address3',
#             'city',
#             'state',
#             'country',
#             'postal_code',
#             'type',
#         )
#         validators = [
#             UniqueTogetherValidator(
#                 queryset=Address.objects.all(),
#                 fields=(
#                     'address1',
#                     'address2',
#                     'address3',
#                     'city',
#                     'state',
#                     'country',
#                     'postal_code',
#                     'type',
#                        )
#             )
#                     ]
#
#
# class UpdateAddressSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Address
#         fields = (
#             'address1',
#             'address2',
#             'address3',
#             'city',
#             'state',
#             'country',
#             'postal_code',
#             'type',
#         )
