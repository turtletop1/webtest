import csv
import base64
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import StreamingHttpResponse, HttpResponse
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.views.decorators.clickjacking import xframe_options_exempt

from posts.models import Post
from stuffs.models import Stuff
from weasyprint import HTML



def get_queryset_by_type(table_type):
    if table_type == 'Stuff':
        return Stuff.objects.order_by('-missing_date')
    elif table_type == 'User':
        return User.objects.order_by('-first_name')
    else:
        return Post.objects.order_by('-issue_date')


def get_csv_headers(table_type):
    headers = {'Stuff': ["ID", "Name", "Missing Date", "User", "Type"],'User': ["ID", "User Name", "First Name", "Last Name", "Email"], }
    return headers.get(table_type,["ID", "User", "Stuff", "Title", "Issue Date", "Status", "Type", "Due Date", "Reward", "Content"] )


def get_csv_row(obj, table_type):
    if table_type == 'Stuff':
        missing_date = obj.missing_date.strftime('%Y-%m-%d %H:%M') if obj.missing_date else ''
        return [obj.id, obj.name, missing_date, obj.user.username if obj.user else '', getattr(obj, 'type', '')]
    
    elif table_type == 'User':
        return [obj.id, obj.username, obj.first_name, obj.last_name, obj.email]
    
    else:  # Post
        issue_date = obj.issue_date.strftime('%Y-%m-%d %H:%M') if obj.issue_date else ''
        due_date = obj.due_date.strftime('%Y-%m-%d') if obj.due_date else ''
        return [
            obj.id,
            obj.user.username if obj.user else '',
            obj.stuff.name if obj.stuff else '',
            obj.title, issue_date, obj.status, obj.type, due_date, obj.reward, obj.content
        ]


def get_photo_base64(photo_file=None, post=None):
    if photo_file:
        file_bytes = photo_file.read()
        if file_bytes:
            encoded = base64.b64encode(file_bytes).decode('utf-8')
            content_type = photo_file.content_type or 'image/jpeg'
            return f"data:{content_type};base64,{encoded}"
    
    elif post and post.stuff and post.stuff.photo_main:
        with post.stuff.photo_main.open('rb') as f:
            encoded = base64.b64encode(f.read()).decode('utf-8')
        return f"data:image/jpeg;base64,{encoded}"
    
    return None


def generation(request):
    table_type = request.GET.get('tables', '').strip()
    queryset = get_queryset_by_type(table_type)
    
    paginator = Paginator(queryset, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    return render(request, 'generations/generation.html', {
        "gens": page_obj,
        "table_type": table_type,
        "values": request.GET
    })


def poster(request, post_id=None):
    post = get_object_or_404(Post, pk=post_id) if post_id else None
    return render(request, "generations/poster.html", {"post": post})

class Echo:
    def write(self, value):
        return value


def export_large_csv(request):

    table_type = request.GET.get('tables', '').strip()
    queryset = get_queryset_by_type(table_type)
    
    filename = f"{table_type.lower() if table_type else 'posts'}_export.csv"
    
    def stream_rows():
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)
        
        yield writer.writerow(get_csv_headers(table_type))
        
        chunk_size = 1000
        for obj in queryset.iterator(chunk_size=chunk_size):
            yield writer.writerow(get_csv_row(obj, table_type))
    
    return StreamingHttpResponse(
        stream_rows(),
        content_type="text/csv; charset=utf-8-sig",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},)


@xframe_options_exempt
def some_view(request, post_id=None):

    post = get_object_or_404(Post, pk=post_id) if post_id else None

    post_data = {
        'title': request.POST.get('title', '').strip() if request.method == 'POST' else '',
        'name': request.POST.get('name', '').strip() if request.method == 'POST' else '',
        'missing_date': request.POST.get('missing_date', '').strip() if request.method == 'POST' else '',
        'type': request.POST.get('type', '').strip() if request.method == 'POST' else '',
        'email': request.POST.get('email', '').strip() if request.method == 'POST' else '',
        'location': request.POST.get('location', '').strip() if request.method == 'POST' else '',
        'description': request.POST.get('description', '').strip() if request.method == 'POST' else '',
    }

    context = {
        'title': post_data['title'] or (post.title if post else ''),
        'name': post_data['name'] or (post.stuff.name if post and post.stuff else ''),
        'location': post_data['location'] or (post.stuff.location if post and post.stuff else ''),
        'missing_date': post_data['missing_date'] or (
            post.stuff.missing_date.strftime('%Y-%m-%d') if post and post.stuff and post.stuff.missing_date else ''
        ),
        'type': post_data['type'] or (post.type if post else ''),
        'email': post_data['email'] or (post.user.email if post and post.user else ''),
        'description': post_data['description'] or (post.stuff.description if post and post.stuff else ''),
        'photo': get_photo_base64(request.FILES.get('photo'), post),
    }

    html_string = render_to_string('generations/poster_pdf.html', context)
    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf()
    
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="poster.pdf"'
    
    return response