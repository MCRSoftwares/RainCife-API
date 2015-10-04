# -*- coding: utf-8 -*-

from rest_framework.views import APIView
from view_manager.decorators import include_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@include_view('api_root')
class APIRootView(APIView):

    def get_response_context(self, request, format):
        context = {
            'markers': reverse('apac:markers-list',
                               request=request, format=format),
        }

        return context

    def get(self, request, format=None, *args, **kwargs):
        return Response(self.get_response_context(request, format))
