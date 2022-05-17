from django.shortcuts import render

# Create your views here.
def guide_home(request):

     
    
    context = {
        "user":request.user,
        
        
    }
    return render(request, 'guide/home.html', context = context)


def guide_evaluation(request):
    
    context = {
        "user":request.user,
        
        
    }
    return render(request, 'guide/evaluation.html', context = context)
    
    