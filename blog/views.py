from django.shortcuts import render, HttpResponse, redirect
from blog.models import Post,BlogComment
from django.contrib import messages
# from blog.templatetags import extras


# Create your views here.
def blogHome(request):
    allPosts = Post.objects.all()
    # print(allPosts)
    context = {'allPosts' : allPosts}
    return render(request,'blog/bloghome.html',context)
    # return HttpResponse('this is blogHome. all the blog post will be here')
def blogPost(request,slug):
    post = Post.objects.filter(slug=slug).first()
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]= [reply]
        else:
            replyDict[reply.parent.sno].append(reply) 
              
    context = {'post':post, 'comments':comments,'user':request.user,'replydict': replyDict}
    return render(request,'blog/blogpost.html',context)

    # return HttpResponse(f'this is blogPost{slug}')
     
def postComment(request):
    if request.method == "POST": 
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")   
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get("parentSno")
        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request,"Your comment has been posted successfully")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post,parent=parent)

            comment.save()
            messages.success(request,"Your Reply has been posted successfully")

    return redirect(f"/blog/{post.slug}")       
 