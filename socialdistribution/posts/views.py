from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser 
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from inbox.models import Inbox
from authors.models import Author,FollowRequest
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import uuid
from authors.serializers import AuthorSerializer
# import django.db.models.signals 
from django.db.models.signals import post_save
# Create your views here.


def create_post(request, author, pid=None):
    try:
        request_copy = request.data.copy() #so we don't modify the original request
        categories = request_copy.data.getlist('categories')
        request_copy['source'] = request.get_host() + request.path
        request_copy['origin'] = request.get_host() + request.path
        if request.method == 'PUT':
            request_copy['id'] = pid

        post_ser = PostSerializer(data=request_copy)
        if post_ser.is_valid():
            post_ser.save(
                author = AuthorSerializer(author).data, 
                categories = categories
            )
            return Response(post_ser.data, status=status.HTTP_201_CREATED)
        else:
            return Response(post_ser.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class PostList(APIView):
    
    def get(self, request, id):
        author = get_object_or_404(Author, id=id)
        posts = author.posted.all() #get all posts of the authors

        page_number, size = request.GET.get('page'), request.GET.get('size')

        if page_number and size:
            paginator = Paginator(posts, size)
            try:
                posts = paginator.get_page(page_number).object_list
            except PageNotAnInteger:
                posts = paginator.get_page(1).object_list
            except EmptyPage:
                posts = paginator.get_page(paginator.num_pages).object_list
        
        serializer = PostSerializer(posts, many=True)
        return Response({"type":"posts","items":serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request, id):
        author = get_object_or_404(Author, id=id)
        if request.user.is_authenticated and request.user.id == author.user.id:
            return create_post(request, author)
        else:
            return Response({"type": "error", "message": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED)

class PostDetail(APIView):
    def get(self, request, id, pid):
        post = get_object_or_404(Post, id=pid)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, pid):
        author = get_object_or_404(Author, id=id)
        if Post.objects.filter(id=pid).exists():
            return Response({"type": "error", "message": "Post already exists"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return create_post(request, author, pid)

    def post(self, request, id, pid):
        if request.user.is_authenticated:
            author = get_object_or_404(Author, id=id)
            post = get_object_or_404(Post, id=pid)
            # update the post whose id is pid
            serializer = PostSerializer(post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"type": "error", "message": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        
    def delete(self, request, id, pid):
        author = get_object_or_404(Author, id=id)
        post = get_object_or_404(Post, id=pid)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentList(APIView):
    def get(self, request, id, pid):
        author = get_object_or_404(Author, id=id)
        post = get_object_or_404(Post, id=pid)
        comments = post.comment_set.all().order_by('-published')

        page_number, size = request.GET.get('page'), request.GET.get('size')
        if page_number and size:
            paginator = Paginator(comments, size)
            try:
                comments = paginator.get_page(page_number).object_list
            except PageNotAnInteger:
                comments = paginator.get_page(1).object_list
            except EmptyPage:
                comments = paginator.get_page(paginator.num_pages).object_list
        
        serializer = CommentSerializer(comments, many=True)
        return Response({"type":"comments","items":serializer.data}, status=status.HTTP_200_OK)

    def post(self,request,id, pid):
        author = get_object_or_404(Author, id=id)
        post = get_object_or_404(Post, id=pid)
        request_copy = request.data.copy()
        request_copy['url'] =  f"{request.build_absolute_uri('/')}/service/authors/{id}/posts/{pid}/comments/{request.data.get('id')}"

        serializer = CommentSerializer(data=request_copy)
        if serializer.is_valid():
            serializer.save(author=author, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostLikes(APIView):
    def get(self,request,id,pid):
        author = get_object_or_404(Author, id=id)
        post = get_object_or_404(Post, id=pid)
        post_url = f"{request.build_absolute_uri('/')}/service/authors/{id}/posts/{pid}"

        likes = Like.objects.all().filter(object=post_url)
        if not likes:
            return Response({"type": "error", "message": "No likes found"}, status=status.HTTP_404_NOT_FOUND)
        
        page_number, size = request.GET.get('page'), request.GET.get('size')
        if page_number and size:
            paginator = Paginator(likes, size)
            try:
                likes = paginator.get_page(page_number).object_list
            except PageNotAnInteger:
                likes = paginator.get_page(1).object_list
            except EmptyPage:
                likes = paginator.get_page(paginator.num_pages).object_list

        serializer = LikeSerializer(likes, many=True)
        return Response({"type":"likes","items":serializer.data}, status=status.HTTP_200_OK)

            
    def post(self, request, id, pid):
        author = get_object_or_404(Author, id=id)
        post = get_object_or_404(Post, id=pid)
        request_copy = request.data.copy()

        request_copy['object'] = f"{request.build_absolute_uri('/')}/service/authors/{id}/posts/{pid}"
        request_copy['summary'] = f"{author.displayName} likes your post"
        request_copy['object_type'] = "post"

        serializer = LikeSerializer(data=request_copy)
        if serializer.is_valid():
            serializer.save(author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentLikes(APIView):
    def get(self,request,id,pid,comment_id):
        author = get_object_or_404(Author, id=id)
        post = get_object_or_404(Post, id=pid)
        comment = get_object_or_404(Comment, id = comment_id)
        post_url = f"{request.build_absolute_uri('/')}/service/authors/{id}/posts/{pid}/comments/{comment_id}"

        likes = Like.objects.all().filter(object=post_url)
        if not likes:
            return Response({"type": "error", "message": "No likes found"}, status=status.HTTP_404_NOT_FOUND)
        
        page_number, size = request.GET.get('page'), request.GET.get('size')
        if page_number and size:
            paginator = Paginator(likes, size)
            try:
                likes = paginator.get_page(page_number).object_list
            except PageNotAnInteger:
                likes = paginator.get_page(1).object_list
            except EmptyPage:
                likes = paginator.get_page(paginator.num_pages).object_list

        serializer = LikeSerializer(likes, many=True)
        return Response({"type":"likes","items":serializer.data}, status=status.HTTP_200_OK)

            
    def post(self, request, id, pid):
        author = get_object_or_404(Author, id=id)
        post = get_object_or_404(Post, id=pid)
        request_copy = request.data.copy()

        request_copy['object'] = f"{request.build_absolute_uri('/')}/service/authors/{id}/posts/{pid}"
        request_copy['summary'] = f"{author.displayName} likes your comment"
        request_copy['object_type'] = "post"

        serializer = LikeSerializer(data=request_copy)
        if serializer.is_valid():
            serializer.save(author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
