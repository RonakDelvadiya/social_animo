from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from users.models import Metadata_Abstract_Info
from profiles.models import prfl_profile

import logging
logger_error = logging.getLogger('content_log_file')
logger = logging.getLogger(__name__)


class cntnt_picture(Metadata_Abstract_Info):
    picture_id = models.BigAutoField(primary_key=True)
    profile = models.ForeignKey(prfl_profile, related_name='profile_uploaded_picture', on_delete=models.CASCADE)
    picture = models.ImageField(null=True, blank=True, upload_to='profile_pic/', height_field=None, width_field=None, max_length=200)
    is_current_profile_picture = models.BooleanField(default=False)
    like_count = models.BigIntegerField(null=True, blank=True, default=0)
    comments_count = models.BigIntegerField(null=True, blank=True, default=0)
    created_by = models.ForeignKey(User, related_name='picture_uploaded_by',on_delete=models.CASCADE)
    
    class Meta:
        db_table = "cntnt_picture"
        verbose_name = ('Picture')
        verbose_name_plural = ('Pictures')


class cntnt_status(Metadata_Abstract_Info):
    status_id = models.BigAutoField(primary_key=True)
    status = models.TextField("Status", blank=False, null=False)
    profile = models.ForeignKey(prfl_profile, related_name='profile_uploaded_status', on_delete=models.CASCADE)
    like_count = models.BigIntegerField(null=True, blank=True, default=0)
    comments_count = models.BigIntegerField(null=True, blank=True, default=0)
    created_by = models.ForeignKey(User, related_name='status_uploaded_by',on_delete=models.CASCADE)

    class Meta:
        db_table = "cntnt_status"
        verbose_name = ('status')
        verbose_name_plural = ('statuss')

class cntnt_comments(Metadata_Abstract_Info):
    comment_id = models.BigAutoField(primary_key=True)
    picture = models.ForeignKey(cntnt_picture, related_name='comment_picture', on_delete=models.CASCADE, blank=True, null=True)
    status = models.ForeignKey(cntnt_status, related_name='comment_status', on_delete=models.CASCADE, blank=True, null=True)
    parent_comment = models.ForeignKey('self' , related_name='inside_comment', on_delete=models.CASCADE, blank=True, null=True)
    comment = models.TextField("Comments", blank=False, null=False)
    like_count = models.BigIntegerField(null=True, blank=True, default=0)
    comments_count = models.BigIntegerField(null=True, blank=True, default=0)
    created_by = models.ForeignKey(User, related_name='comment_by',on_delete=models.CASCADE)

    class Meta:
        db_table = "cntnt_comment"
        verbose_name = ('Comment')
        verbose_name_plural = ('Comments')

    def save(self, **kwargs):
        try:
            "update like count by 1"
            if self.picture and (cntnt_comments.objects.filter(picture=self.picture.picture_id).count() == (self.picture.comments_count)) :
                cntnt_picture.objects.filter(picture_id=self.picture.picture_id).update(comments_count=F('comments_count')+1)

            if self.status and (cntnt_comments.objects.filter(status=self.status.status_id).count() == (self.status.comments_count)) :
                cntnt_status.objects.filter(status_id=self.status.status_id).update(comments_count=F('comments_count')+1)

            if self.parent_comment and (cntnt_comments.objects.filter(parent_comment=self.parent_comment.comment_id).count() == (self.parent_comment.comments_count)) :
                cntnt_comments.objects.filter(comment_id=self.parent_comment.comment_id).update(comments_count=F('comments_count')+1)

        except Exception as e:
            logger.error(str(e))
            
        super(cntnt_comments, self).save(**kwargs)


class cntnt_likes(Metadata_Abstract_Info):
    like_id = models.BigAutoField(primary_key=True)
    picture = models.ForeignKey(cntnt_picture, related_name='like_on_picture', on_delete=models.CASCADE, blank=True, null=True)
    status = models.ForeignKey(cntnt_status, related_name='like_on_status', on_delete=models.CASCADE, blank=True, null=True)
    comment = models.ForeignKey(cntnt_comments, related_name='like_on_comment', on_delete=models.CASCADE, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='like_by',on_delete=models.CASCADE)

    class Meta:
        db_table = "cntnt_like"
        verbose_name = ('Like')
        verbose_name_plural = ('Likes')

    def save(self, **kwargs):
        try:
            "update like count by 1"
            if self.picture and not cntnt_likes.objects.filter(picture=self.picture.picture_id,created_by=self.created_by) :
                cntnt_picture.objects.filter(picture_id=self.picture.picture_id).update(like_count=F('like_count')+1)

            if self.status and not cntnt_likes.objects.filter(status=self.status.status_id,created_by=self.created_by) :
                cntnt_status.objects.filter(status_id=self.status.status_id).update(like_count=F('like_count')+1)

            if self.comment and not cntnt_likes.objects.filter(comment=self.comment.comment_id,created_by=self.created_by):
                cntnt_comments.objects.filter(comment_id=self.comment.comment_id).update(like_count=F('like_count')+1)

        except Exception as e:
            logger.error(str(e))

        super(cntnt_likes, self).save(**kwargs)