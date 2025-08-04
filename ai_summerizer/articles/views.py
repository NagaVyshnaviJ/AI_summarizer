from django.shortcuts import render
from django.views.decorators.csrf import  csrf_exempt
from django.http import JsonResponse
import requests
from .models import Article
# Create your views here.
HF_TOKEN=''
def home(request):
    return render(request, 'articles/home.html')

@csrf_exempt
def summarize_article(request):
    if request.method == 'POST':
        text= request.POST.get('article_text','')
        if not text:
            return JsonResponse({"error":"No text provided"},status=400)
        headers={
            'Authorization': f'Bearer  { HF_TOKEN}',
            'Content-Type': 'application/json',
        }
        payload={
            "inputs":text[:1000],
            "options":{"Wait for model":True}
        }
        resp = requests.post(
            "https://api-inference.huggingface.co/models/facebook/bart-large-cnn",
        headers = headers, json = payload
        )
        if resp.status_code != 200:
            return JsonResponse({"error": f"Summarization failed: {resp.status_code}"}, status=500)
        summary=resp.json()[0].get("summary_text","")
        words = [w.strip(".,") for w in text.lower().split()]
        stopwords = {"the", "and", "that", "this", "with", "from", "you", "have", "are", "for", "was"}
        keywords = list({w for w in words if w not in stopwords and len(w) > 4})[:5]
        tags = ", ".join(keywords)
        Article.objects.create(original_text=text, summary=summary, tags=tags)
        return JsonResponse({"summary": summary,  "tags": tags})
    return JsonResponse({"error":"Invalid request"},status=400)



