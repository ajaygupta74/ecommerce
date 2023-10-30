from django.views import generic
from blogs.models import Blog
from django.shortcuts import render


class blogListView(generic.TemplateView):
    template_name = 'blogs/home.html'

    def get_context_data(self, keyword=None):
        all_blog_list = Blog.objects.filter(
            status=Blog.Statuschoices.PUBLISH).order_by('-created_at')
        blog_list = all_blog_list.none()
        if keyword:
            for key in keyword:
                blog_list = blog_list | all_blog_list.filter(
                    title__icontains=key)
        recent_blogs = None
        response_data = {}
        if not blog_list:
            recent_blogs = Blog.objects.filter(
                status=Blog.Statuschoices.PUBLISH).order_by('-created_at')[:10]
            blog_list = all_blog_list.order_by('-updated_at')
            response_data['no_results_message'] = (
                "No items found with the entered keyword")
        response_data['blog_list'] = blog_list.distinct()
        response_data['recent_blogs'] = recent_blogs
        return response_data

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        keyword = request.POST.get('keyword', '')
        context = self.get_context_data(keyword)
        return render(request, self.template_name, context)


class BlogDetailView(generic.DetailView):
    model = Blog
    template_name = 'blogs/blog_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = self.get_object()
        context.update({
            'blog': blog,
        })
        return context
