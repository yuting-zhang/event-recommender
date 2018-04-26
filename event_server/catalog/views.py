from django.shortcuts import render

def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_books=1
    num_instances=2
    num_instances_available=3
    num_authors=4
    
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors},
    )