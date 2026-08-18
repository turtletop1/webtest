import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import StreamingHttpResponse
from posts.models import Post
from stuffs.models import Stuff
from django.contrib import messages
from django.contrib.auth.models import User

def generation(request):
    table_type = request.GET.get('tables', '').strip()

    if table_type == 'Stuff':
        gen = Stuff.objects.order_by('-missing_date')
    elif table_type == 'User':
        gen = User.objects.order_by('-first_name')
    else:
        gen = Post.objects.order_by('-issue_date')

    paginator = Paginator(gen, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {"gens": page_obj, "table_type": table_type,"values": request.GET}

    return render(request, 'generations/generation.html', context)


class Echo:
    def write(self, value):
        return value


def export_large_csv(request):
    table_type = request.GET.get('tables', '').strip()
    
    if table_type == 'Stuff':
        gen = Stuff.objects.order_by('-missing_date').select_related('user') #select_related = 1次SQL JOIN查詢 
    elif table_type == 'User':
        gen = User.objects.order_by('-first_name')  
    else:
        gen = Post.objects.order_by('-issue_date').select_related('user', 'stuff') 

    filename = f"{table_type.lower() if table_type else 'posts'}_export.csv"

    def stream_rows():
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)

        if table_type == 'Stuff':
            yield writer.writerow(["ID", "Name", "Missing Date", "User", "Type"])
            for s in gen.iterator(chunk_size=1000):
                missing_date = s.missing_date.strftime('%Y-%m-%d %H:%M') if getattr(s, 'missing_date', None) else ''
                username = s.user.username if s.user else ''
                
                yield writer.writerow([
                    s.id,
                    s.name,
                    missing_date,
                    username,
                    getattr(s, 'type', '')#安全獲取物件obj嘅attri屬性 (obj, attr , defalut)
                ])

        elif table_type == 'User':
            yield writer.writerow(["ID", "User Name", "First Name", "Last Name", "Email"])
            for a in gen.iterator(chunk_size=1000):
                yield writer.writerow([
                    a.id,
                    a.username,
                    a.first_name,
                    a.last_name,
                    a.email
                ])

        else:    
            yield writer.writerow(["ID", "User", "Stuff", "Title", "Issue Date", "Status", "Type", "Due Date", "Reward", "Content"])

            for p in gen.iterator(chunk_size=1000):
                issue_date = p.issue_date.strftime('%Y-%m-%d %H:%M') if p.issue_date else ''
                due_date = p.due_date.strftime('%Y-%m-%d') if getattr(p, 'due_date', None) else ''
                username = p.user.username if p.user else ''
                stuff_name = p.stuff.name if p.stuff else ''

                yield writer.writerow([
                    p.id,
                    username,
                    stuff_name,
                    p.title,
                    issue_date,
                    p.status,
                    p.type,
                    due_date,
                    p.reward,
                    p.content
                ])

    response = StreamingHttpResponse(
        stream_rows(),
        content_type="text/csv; charset=utf-8-sig",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
    return response