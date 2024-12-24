from django.http import HttpResponse


def robots_txt(request):
    content = """
    User-agent: *
    Disallow: /admin/
    Sitemap: https://pdgaedu.com/sitemap.xml
    """
    return HttpResponse(content, content_type="text/plain")
