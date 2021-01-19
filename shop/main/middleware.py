from .models import Category


class CategoryMiddleware:
    """Middleware adds Categories to template context."""
    def __init__(self, get_response):
        self.get_response = get_response
        self.categories = Category.objects.root_nodes()

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        response.context_data["categories"] = self.categories
        return response
