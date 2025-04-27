from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import TreeStore
from rest_framework.viewsets import ModelViewSet

from .serializers import TreeSerializer


class TreeView(ModelViewSet):
    serializer_class = TreeSerializer
    http_method_names = ['get']

    def get_queryset(self):
        return TreeStore.objects.all()


class ChildrenView(ModelViewSet):
    serializer_class = TreeSerializer
    queryset = TreeStore.objects.all()
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        queryset = TreeStore.objects.filter(parent=id).select_related('parent')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class DrevoView(ModelViewSet):
    serializer_class = TreeSerializer
    queryset = TreeStore.objects.all()

    def list(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        obj = get_object_or_404(TreeStore, pk=id)

        parents = []
        current = obj.parent

        while current is not None:
            parents.append(current)
            current = current.parent

        serializer = self.get_serializer(parents, many=True)
        return Response(serializer.data)


class NoneView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = TreeStore.objects.filter(parent=None)
        serializer = TreeSerializer(queryset, many=True)
        return Response(serializer.data)