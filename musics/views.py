from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Music, Artist, Comment
from .serializer import MusicSerializer, ArtistSerializer, CommentSerializer, ArtistDetailSerializer


@api_view(['GET'])
def music_list(request):

    params = {}
    artist_pk = request.GET.get('artist_pk')  # url ? 는 request.GET으로 꺼내 씀

    if artist_pk is not None:
        params['artist_id'] = artist_pk

    # 만약 artist_pk 가 Query Params 로 넘어온다면, artist_pk 로 필터링한 값만 응답.
    # 그렇지 않다면 전체 음악 응답.

    # 모든 음악에 대한 정보 받아서 json파일 형식으로 변환시켜서 응답해야 한다
    musics = Music.objects.filter(**params)  # 내가 보여주고 싶은 데이터를 DB에서 꺼낸다
    # serializing작업을 해준다 (ModelForm 작성과 비슷)
    serializer = MusicSerializer(musics, many=True)
    # (내가 받고 싶은 data, many=T/F  (default = F))
    return Response(serializer.data)  # json형태로 응답을 보낼 것


# api/vi1/musics/3/
@api_view(['GET', 'PUT', 'DELETE'])
def music_detail_update_delete(request, music_pk):
    music = get_object_or_404(Music, pk=music_pk)  # 음악 있는지 없는지 확인
    if request.method == 'GET':
        serializer = MusicSerializer(music)  # 하나의 데이터라서 many=True 안 넣음
        return Response(serializer.data)
    elif request.method == 'PUT':
        # 수정할 때 사용자가 넘긴 데이터 / 수정이므로 기존 instance 넣어줌
        serializer = MusicSerializer(data=request.data, instance=music)
        if serializer.is_valid(raise_exception=True):  # valid 하지 않을 땐 exception
            serializer.save()  # 수정하고
            return Response(serializer.data)  # 수정한 결과값 보여주기
    else:  # DELETE
        music.delete()
        return Response({'message': 'Music has been deleted!'})


@api_view(['GET'])
def artist_list(request):
    artists = Artist.objects.all()
    serializer = ArtistSerializer(artists, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def artist_detail_update_delete(request, artist_pk):
    artist = get_object_or_404(Artist, pk=artist_pk)
    if request.method == 'GET':
        serializer = ArtistDetailSerializer(artist)  # 하나의 데이터라서 many=True 안 넣음
        return Response(serializer.data)
    if request.method == 'PUT':
        serializer = ArtistSerializer(data=request.data, instance=artist)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    else:
        artist.delete()
        return Response({'message': 'Artist has been deleted!'})


@api_view(['GET'])
def comment_list(request):
    comments = Comment.objects.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def comments_create(request, music_pk):
    # 사용자가 보낸 데이터 그대로 serializer 에 담겠음
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):  # 검증에 실패하면 400 Bad Request 오류 발생
        serializer.save(music_id=music_pk)
    return Response(serializer.data)


@api_view(['PUT', 'DELETE'])
def comments_update_and_delete(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'PUT':
        serializer = CommentSerializer(data=request.data, instance=comment)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    # if request.method == 'DELETE':
    else:
        comment.delete()
        return Response({'message': 'Comment has been deleted!'})
