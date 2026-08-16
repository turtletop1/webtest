from django.shortcuts import render,get_object_or_404 ,redirect
from .models import Comment
from django.contrib import messages


def comment(request):

    comments = Comment.objects.order_by('-date').filter(user=request.user) 

    context = {"comments":comments}      
        
    return render(request,"comments/comment.html", context)


def delete_comment(request,comment_id):

    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()

    return redirect('comments:comment')



def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    post_id = comment.post.id

    if comment.user != request.user:
        messages.error(request, "you can not change this comment")
        return redirect('posts:post_detail', post_id=post_id)

    if request.method == "POST":
        content = request.POST['content']
        
        if content:
            comment.content = content
            comment.save()
            messages.success(request, "update success")
        else:
            messages.error(request, "comment can not blank")

        return redirect('posts:post_detail', post_id=post_id)

    return redirect('posts:post_detail', post_id=post_id)