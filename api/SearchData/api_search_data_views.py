from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from services.search_stack_overflow_service import search_stack_over_flow
from services.redis_cache_helper_service import set_cache, get_cache
'''
This is GET request api for the display of data according to the search result and have been implemented
by basic query searching

Endpoint for searching - http://127.0.0.1:8000/search/?q=your_question&page=1'

'''


class Search(APIView):
    def get(self, request):
        query = request.query_params.get('q')
        page = request.query_params.get('page')
        data = get_cache(search_query=query, page=page)
        print(data)
        if data is not None:
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            print("in else")
            data = search_stack_over_flow(question=query, page=page)
            set_cache(search_query=query, page=page, data_to_cache=data)
            return Response(data=data, status=status.HTTP_200_OK)