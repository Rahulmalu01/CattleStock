from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from prediction.models import DiseasePrediction


@login_required
def prediction_dashboard(request):
    predictions = DiseasePrediction.objects.select_related('cattle')
    return render(request,'prediction/dashboard.html',{'predictions': predictions})