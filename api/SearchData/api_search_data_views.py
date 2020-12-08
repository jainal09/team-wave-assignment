from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from services.search_stack_overflow_service import search_stack_over_flow
from services.redis_cache_helper_service import set_cache, get_cache
from services.rate_limiting import limiter
from .serializers import SearchSerializer
'''
This is GET and POST request api for the display of data according to the search result and have been implemented
by basic query searching

Endpoint for searching (GET) - http://127.0.0.1:8000/search/?q=your_question&page=1'
Endpoint for searching (POST) - http://127.0.0.1:8000/search/

'''


class Search(APIView):
    def post(self, request):
        serializer = SearchSerializer(data=request.data)
        # Check if post request params valid
        if serializer.is_valid():
            page = serializer.data["page"]
            q = serializer.data["query"]
            if limiter(request):
                # rate limiting value reached and send a 429
                return Response(data="TOO MANY REQUESTS", status=status.HTTP_429_TOO_MANY_REQUESTS)
            else:
                # check if same query exists in cache
                data = get_cache(search_query=q, page=page)
                if data is not None:
                    # data exists in cache
                    return Response(data=data, status=status.HTTP_200_OK)
                else:
                    print("in else")
                    # query from stackoverflow api as data not in cache
                    data = search_stack_over_flow(question=q, page=page)
                    # add this new data in cache
                    set_cache(search_query=q, page=page, data_to_cache=data)
                    return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response(status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        if limiter(request):
            # rate limiting value reached and send a 429
            return Response(data="TOO MANY REQUESTS", status=status.HTTP_429_TOO_MANY_REQUESTS)
        else:
            query = request.query_params.get('q')
            page = request.query_params.get('page')
            # check if same query exists in cache
            data = get_cache(search_query=query, page=page)
            if data is not None:
                # data exists in cache
                return Response(data=data, status=status.HTTP_200_OK)
            else:
                print("in else")
                # query from stackoverflow api as data not in cache
                data = search_stack_over_flow(question=query, page=page)
                # add this new data in cache
                set_cache(search_query=query, page=page, data_to_cache=data)
                return Response(data=data, status=status.HTTP_200_OK)