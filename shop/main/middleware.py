from .models import Category


class CategoryMiddleware:
    """A middleware provides root categories to templates.

    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.categories = Category.objects.root_nodes()

    def __call__(self, request):
        return self.get_response(request)

    def process_template_response(self, request, response):
        response.context_data['categories'] = self.categories
        return response
