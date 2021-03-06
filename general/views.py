import MySQLdb
import json
from decouple import config
from rest_framework import viewsets, status
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, authentication_classes, permission_classes, action
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import HttpResponse
from .models import *
from .serializers import *



class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )


    def create(self, request, *args, **kwargs):
        response = {'message': 'You can\'t use POST method like this'}
        return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)

    def retrieve(self, request, *args, **kwargs):
        response = {'message': 'You can\'t use GET method like this'}
        return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)

    def update(self, request, *args, **kwargs):
        response = {'message': 'You can\'t use PUT method like this'}
        return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)

    def destroy(self, request, *args, **kwargs):
        response = {'message': 'You can\'t use DELETE method like this'}
        return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)




class FamilyViewSet(viewsets.ModelViewSet):
    queryset = Family.objects.all().order_by('batch')
    serializer_class = FamilySerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    def create(self, request, *args, **kwargs):
        response = {'message': 'You can\'t use POST method like this'}
        return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)

    def retrieve(self, request, *args, **kwargs):
        response = {'message': 'You can\'t use GET method like this'}
        return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)

    def update(self, request, *args, **kwargs):
        response = {'message': 'You can\'t use PUT method like this'}
        return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)

    def destroy(self, request, *args, **kwargs):
        response = {'message': 'You can\'t use DELETE method like this'}
        return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)




class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )
    authentication_classes = (TokenAuthentication,)
    def list(self, request, *args, **kwargs):
            user = User.objects.all().order_by('-userextension__batch', 'first_name')
            serializer = UserSerializer(user, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class ForumPostViewSet(viewsets.ModelViewSet):
    queryset = ForumPost.objects.all()
    serializer_class = ForumPostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        forum_post = ForumPost()
        forum_post.heading = request.data['heading']
        forum_post.body = request.data['body']
        forum_post.author = request.user
        forum_post.author_name = request.user.first_name + ' ' + request.user.last_name
        forum_post.save()
        serializer = ForumPostSerializer(forum_post, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        if 'id' in request.GET:
            forum_post = ForumPost.objects.all().filter(author=request.GET['id'])
            serializer = ForumPostSerializer(forum_post, many = True)
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            forum_post = ForumPost.objects.all().order_by('-id')
            serializer = ForumPostSerializer(forum_post, many = True)
            return Response(serializer.data, status = status.HTTP_200_OK)


class ForumCommentViewSet(viewsets.ModelViewSet):
    queryset = ForumComment.objects.all()
    serializer_class = ForumCommentSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        forum_comment = ForumComment()
        forum_comment.comment = request.data['comment']
        par_post = ForumPost.objects.all().filter(id=request.data['post_id'])
        forum_comment.parent_post = par_post[0]
        forum_comment.author = request.user
        forum_comment.author_name = request.user.first_name + ' ' + request.user.last_name
        forum_comment.save()
        serializer = ForumCommentSerializer(forum_comment, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        if 'post_id' in request.GET:
            forum_comment = ForumComment.objects.all().filter(parent_post = request.GET['post_id']).order_by('-id')
            serializer = ForumCommentSerializer(forum_comment, many = True)
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            forum_comment = ForumComment.objects.all().filter(author = request.GET['user_id']).order_by('-id')
            serializer = ForumCommentSerializer(forum_comment, many = True)
            return Response(serializer.data, status = status.HTTP_200_OK)



class ForumReplyViewSet(viewsets.ModelViewSet):
    queryset = ForumReply.objects.all()
    serializer_class = ForumReplySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        forum_reply = ForumReply()
        forum_reply.author = request.user
        forum_reply.parent_comment = request.data['comment_id']
        forum_reply.reply = request.data['reply']
        forum_reply.save()
        serializer = ForumReplySerializer(forum_reply, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        forum_reply = ForumReply.objects.all().filter(parent_comment = request.GET['comment_id'])
        serializer = ForumReplySerializer(forum_reply, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)


class UserFromTokenViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        user = Token.objects.get(key=request.data['token']).user
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EventsViewSet(viewsets.ModelViewSet):
    queryset = Events.objects.all().order_by('-id')
    serializer_class = EventsSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )


class UserExtensionViewSet(viewsets.ModelViewSet):
    queryset = UserExtension.objects.all()
    serializer_class = UserExtensionSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        user_details = UserExtension.objects.all().filter(user = request.GET['id'])
        serializer = UserExtensionSerializer(user_details, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def full_list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def commentCount(request):
    all_comment = ForumComment.objects.all()
    user = request.user
    count = 0
    for comment in all_comment:
        parent_post = comment.parent_post
        if str(parent_post.author) == str(user):
            count = count + 1
    return HttpResponse({count}, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_family(request):
    data = []
    family = []
    db = MySQLdb.connect(user=config('DB_USER'),
                         db=config('DB_NAME'),
                         passwd=config('DB_PASSWORD'),
                         host='localhost')
    cursor = db.cursor()
    sql = "SELECT batch, group_concat(user_id ORDER BY auth_user.first_name, auth_user.last_name separator ',') FROM general_userextension, auth_user WHERE auth_user.id=general_userextension.user_id GROUP BY batch;"
    cursor.execute(sql)
    data = cursor.fetchall()
    db.close()
    for x in data:
        obj = {}
        obj["batch"] = x[0]
        my_list = x[1].split(",")
        final = json.dumps(my_list)
        obj["user_id"] = final
        family.append(obj)
    return Response(family, status=status.HTTP_200_OK)



@api_view(['GET'])
def conf(request):
    return Response({"maintenance":False,"update":False,"app_version":"1.0"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def onboarding(request):
    return Response(
        [
            {
                "title": "Title1",
                "desc": "Desc1",
                "img": "https://sochem.org/static/media/sochemlogo.93a3f8aa.png"
            },
            {
                "title": "Title2",
                "desc": "Desc2",
                "img": "https://sochem.org/static/media/sochemlogo.93a3f8aa.png"
            },
            {
                "title": "Title3",
                "desc": "Desc3",
                "img": "https://sochem.org/static/media/sochemlogo.93a3f8aa.png"
            }
        ],
        status=status.HTTP_200_OK)


@api_view(['GET'])
def home_carousel(request):
    return Response(
        [
            {
                "title": "Title1",
                "img": "https://sochem.org/static/media/sochemlogo.93a3f8aa.png"
            },
            {
                "title": "Title2",
                "img": "https://sochem.org/static/media/sochemlogo.93a3f8aa.png"
            },
            {
                "title": "Title3",
                "img": "https://sochem.org/static/media/sochemlogo.93a3f8aa.png"
            },
            {
                "title": "Title4",
                "img": "https://sochem.org/static/media/sochemlogo.93a3f8aa.png"
            },
            {
                "title": "Title5",
                "img": "https://sochem.org/static/media/sochemlogo.93a3f8aa.png"
            },
            {
                "title": "Title6",
                "img": "https://sochem.org/static/media/sochemlogo.93a3f8aa.png"
            }
        ],
        status=status.HTTP_200_OK)
