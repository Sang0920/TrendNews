# extractor/views.py
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from news_keyword_extractor import news_keyword_extractor 
from rest_framework.response import Response


@api_view(['GET', 'POST'])
def get_keywords(request):
    if request.method == 'POST':
        data = request.data
    else:
        data = request.query_params

    algo = data.get('algo', 'TF-IDF')
    lang = data.get('lang', 'vi')
    region = data.get('region', 'VN')
    topic = data.get('topic', 'CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB')
    period = int(data.get('period', 1))
    min_ngram = int(data.get('min_ngram', 5))
    max_ngram = int(data.get('max_ngram', 5))

    try:
        result = news_keyword_extractor(
            algo=algo,
            lang=lang,
            region=region,
            topic=topic,
            period=period,
            min_ngram=min_ngram,
            max_ngram=max_ngram
        )
        result_json = result
        # return JsonResponse(result_json, safe=False)
        return Response(result_json)
    except Exception as e:
        # return JsonResponse({'error': str(e)}, status=500)
        return Response({'error': str(e)}, status=500)


def landing_page(request):
    return render(request, 'extractor/landing_page.html')
