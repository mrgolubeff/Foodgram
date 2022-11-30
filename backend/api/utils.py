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
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def delete_object(model_1, model_2, request, id):
    obj = get_object_or_404(model_1, id=id)
    if model_2 == Follow:
        subscribe = model_2.objects.filter(user=request.user.id,
                                           author=obj)
    else:
        subscribe = model_2.objects.filter(user=request.user.id,
                                           recipe=obj)
    if subscribe.exists():
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_404_NOT_FOUND)
