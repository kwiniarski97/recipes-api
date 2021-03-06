from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.helpers.get_recipe_if_exists import get_recipe_if_exists
from api.helpers.get_user_by_username import get_user_by_username_from_headers
from api.helpers.is_authenticated import is_authenticated_headers
from api.helpers.is_recipe_owner import is_recipe_owner
from api.helpers.add_related_data_to_recipe import add_related_data_to_recipe
from domain.models import Photo
from api.serializers.photo_serializer import PhotoCreateSerializer
from api.serializers.recipe_serializer import RecipeDetailSerializer, RecipeUpdateSerializer


class RecipeDetailView(APIView):
    def get(self, req, id):
        recipe = get_recipe_if_exists(id)
        serializer = RecipeDetailSerializer(recipe)
        return Response(serializer.data)

    def put(self, req, id):
        if not is_authenticated_headers(headers=req.META):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user = get_user_by_username_from_headers(req.META)
        recipe = get_recipe_if_exists(id)

        if not is_recipe_owner(recipe, user):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # updating recipe
        serializer = RecipeUpdateSerializer(recipe, data=req.data)
        if serializer.is_valid():
            recipe = serializer.save()
            recipe_id = recipe.id
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        Photo.objects.filter(recipe_id=recipe_id).delete()
        try:
            add_related_data_to_recipe(req.data['photos'], PhotoCreateSerializer, recipe_id)
        except Exception as e:
            return Response(str(e), status.HTTP_400_BAD_REQUEST)

        return Response(recipe_id, status.HTTP_200_OK)

    def delete(self, req, id):
        if not is_authenticated_headers(headers=req.META):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        user = get_user_by_username_from_headers(req.META)
        recipe = get_recipe_if_exists(id)

        if not is_recipe_owner(recipe, user):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        recipe.delete()
        Photo.objects.filter(recipe_id=id).delete()
        return Response(status.HTTP_200_OK)
