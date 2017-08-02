from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404
from .models import Post, Like, Comment
from .forms import SearchForm, CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

import re

class Search(object):    

    @staticmethod
    def sortByCountryOrCity(quary_set, complex_q):
        
        return quary_set.filter(complex_q)

    @staticmethod
    def createComplexQ(search_str, markers):
        list_to_search = re.findall(r"(\w+)", search_str)
        complex_q = Q()
        for item in list_to_search:
            for marker in markers:
                complex_q |= Q(**{marker: item})
            
        return complex_q

    

class PostActions(object):

    @staticmethod
    def likePost(request):

        post_id = int(request.POST['post_id'])
        user = request.user
        post = Post.objects.get(id=post_id)
        
        try:
            like = post.likes.get(user=user)
            print(like)
            like.delete()

        except Like.DoesNotExist:
            post.likes.add(Like.objects.create(user=user))
            post.save()

        finally:
            return post

    @staticmethod
    def commentPost(request, post_id):

        post = Post.objects.get(id=post_id)

        comment_form = CommentForm(request.POST)
        
        if comment_form.is_valid():
            
            comment_data = comment_form.cleaned_data
            comment_data["user"] = request.user
            
            comment = Comment.objects.create(**comment_data)
            
            post.comments.add(comment)
            post.save()

            return post


class LoginRequiredView(LoginRequiredMixin, View):


    login_url = settings.LOGIN_URL
    redirect_field_name = settings.LOGIN_URL

# class MainPagination(object):

#     @staticmethod
#     def make_pagination(request, some_list=None, num_items=2):

#         paginator = Paginator(some_list, num_items) 
#         request = getattr(request, request.method)
#         page = request.get('page_number')
#         pages_list = [p for p in paginator.page_range]
#         print(pages_list)

#         try:
#             pags = paginator.page(page)
#         except PageNotAnInteger:
#             # If page is not an integer, deliver first page.
#             pags = paginator.page(1)
#         except EmptyPage:
#             # If page is out of range (e.g. 9999), deliver last page of results.
#             pags = paginator.page(paginator.num_items)

#         return pags, pages_list

class Main(LoginRequiredView):

    # def get(self, request):

    #     context = {}
    #     print(request.user)

    #     search_form = SearchForm()
    #     context['search_form'] = search_form
    #     posts = Post.objects.all()
    #     page = request.GET.get('pagination_page')

    #     context['post_pags'], context['post_pages_list'] = MainPagination.make_pagination(request, list(posts), 2)
        
    #     return render(request, "main.html", context)
    def get(self, request):

        context = {}
        print(request.user)

        search_form = SearchForm()
        context['search_form'] = search_form
        posts = Post.objects.all()
        pagination_page = request.GET.get('pagination_page')

        if pagination_page:
            pagination_page = int(pagination_page)

        paginator = Paginator(posts, 2) 

        try:
            posts_page = paginator.page(pagination_page)
        except PageNotAnInteger:
            posts_page = paginator.page(1)
        except EmptyPage:
            posts_page = paginator.page(paginator.num_items)

        context['posts_page'] = posts_page
        context['page_range'] = paginator.page_range
        
        
        return render(request, "main.html", context)

    def post(self, request):
        # print(request.POST.get("submit") == "pagination_page")
        if request.POST.get("submit") == "search":
            search_form = SearchForm(request.POST)
            if search_form.is_valid():
                search_data = search_form.cleaned_data
        
            return redirect("/search/%s/"%search_data["search"].replace(",","+").replace(" ",""))

        if request.is_ajax():
            
            post = PostActions.likePost(request)

            return HttpResponse("%s like"%post.likes.count())


class SearchPage(LoginRequiredView):

    def get(self, request, search_str):

        context = {}
        # search_str = request.GET.get('search')
        # print(search_str)
        print(re.findall(r"(\w+)", search_str))
        complex_q = Search.createComplexQ(search_str, ["country", "city"])
        posts = Post.objects.all()
        posts = Search.sortByCountryOrCity(posts, complex_q)

        search_form = SearchForm()
        context['search_form'] = search_form
        # posts = Post.objects.all()
        pagination_page = request.GET.get('pagination_page')

        if pagination_page:
            pagination_page = int(pagination_page)

        paginator = Paginator(posts, 2) 

        try:
            posts_page = paginator.page(pagination_page)
        except PageNotAnInteger:
            posts_page = paginator.page(1)
        except EmptyPage:
            posts_page = paginator.page(paginator.num_items)

        context['posts_page'] = posts_page
        context['page_range'] = paginator.page_range
        context['search_str'] = search_str
        
        return render(request, "search.html", context)

    def post(self, request, search_str):

        if request.POST.get("submit") == "search":
            search_form = SearchForm(request.POST)
            if search_form.is_valid():
                search_data = search_form.cleaned_data
        
            return redirect("/search/%s/"%search_data["search"].replace(",","+").replace(" ",""))

        if request.is_ajax():
            
            post = PostActions.likePost(request)

            return HttpResponse("%s like"%post.likes.count())

class PostPage(LoginRequiredView):


    def get(self, request, post_id):
        context = {}

        comment_form = CommentForm()
        context["comment_form"] = comment_form

        post = get_object_or_404(Post, id=post_id)
        context["post"] = post

        comments = post.comments.all().order_by("-id")
        context["comments"] = comments[:3]

        if comments.count() > 3:
            context["more"] = True

        return render(request, "post_page.html", context)

    def post(self, request, post_id):

        context = {}
        if request.POST.get("submit") == "comment":
            
            post = PostActions.commentPost(request, post_id)
            context["post"] = post

            return redirect("/post_page/%s/"%post_id)

        elif request.is_ajax():
            num = int(request.POST['num'])
            num += 2
            post_id = int(request.POST['post_id'])
            print(num)
            post = get_object_or_404(Post, id=post_id)
            context["post"] = post
            comments = post.comments.all().order_by("-id")
            context["comments"] = comments[:num]

            if comments.count() > num:
                context["more"] = True
            
            return render(request, "comments_ajax.html", context)

        else:
            return Http404


        # print("dsadassaddssa",request.is_ajax())
        # if request.is_ajax() and request.POST["flag"] == "add_comment":
        #     context = {}
        #     # post_id = request.POST["post_id"]
        #     print(post_id)
        #     post = PostActions.commentPost(request, int(post_id))
        #     context["post"] = post
        #     print(post)
        #     return render(request, "comments_ajax.html", context)
            

def more_comments(request):
    if request.is_ajax():
        num = request.POST['num']
        print(num)
        reviews = Review.objects.all().order_by("-id")[:int(num)]
        return render(request, "reviews.html", {"reviews": reviews})
    else:
        return Http404