from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from users.models import Follow

from .serializers import SubscribeCreateDestroySerializer


def post_object(serializer, request, id):
    if serializer == SubscribeCreateDestroySerializer:
        data = {'user': request.user.id, 'author': id}
    else:
        data = {'user': request.user.id, 'recipe': id}
    serializer = serializer(data=data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def delete_object(model_1, model_2, request, id):
    object = get_object_or_404(model_1, id=id)
    if model_2 == Follow:
        subscribe = model_2.objects.filter(user=request.user.id,
                                           author=object)
    else:
        subscribe = model_2.objects.filter(user=request.user.id,
                                           recipe=object)
    if subscribe.exists():
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_404_NOT_FOUND)
