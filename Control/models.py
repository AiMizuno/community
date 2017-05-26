from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import datetime
import django
from django.urls import reverse

# Create your models here.
class Account(models.Model):

    SEX_CHOICES = {
        1: '男',
        2: '女',
    }

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sex = models.SmallIntegerField(default=1, choices=SEX_CHOICES.items())
    avatar = models.ImageField(upload_to="Image/", blank=True, null=True)
    grade = models.IntegerField(blank=True, null=True)
    college = models.CharField(max_length=20, blank=True, null=True)
    major = models.CharField(max_length=20, blank=True, null=True)
    realname = models.CharField(max_length=20, blank=True, null=True)
    IDnum = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'Account'

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                p = Account.objects.get(user=self.user)
                self.pk = p.pk
            except Account.DoesNotExist:
                pass

        super(Account, self).save(*args, **kwargs)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Account()
        profile.user = instance
        profile.save()


post_save.connect(create_user_profile, sender=User)

#社团相关

class Community(models.Model):
    name = models.CharField(u'社团缩写', max_length=20, primary_key=True)
    community_name = models.CharField(u'社团名字', max_length=20, null=True, blank=True)
    establish_date = models.DateField(u"创建时间", default=django.utils.timezone.now)
    introduction = models.CharField(u'简介', max_length=100, default="", blank=True, null=True)
    icon = models.ImageField(upload_to="Image/", blank=True, null=True)
    #member = models.ManyToManyField(u'成员', Person)
    def __str__(self):
        return self.name

class Activity(models.Model):
    # hoster = models.ForeignKey(Association, on_delete=models.CASCADE)
    # community = models.ForeignKey(Community)
    community = models.ForeignKey(Community, related_name='community_activity', on_delete=models.CASCADE, null=True, blank=True)
    #author = models.ManyToManyField(Account)
    name = models.CharField(u'名字', null= True, blank=True, max_length = 200)
    # time = 2017.4.3 10:00 AM-11：30AM
    datetime = models.CharField(u'日期', null=True, blank=True, max_length=200)
    address = models.CharField(u'地址', null=True, blank=True, max_length = 200)
    introduction = models.TextField(u'介绍',null=True, blank=True)
    def __str__(self):
        return self.name

class Private_Message(models.Model):
    sender = models.ForeignKey(User, default="")
    acceptor = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    create_time = models.DateField(null=True, blank=True)
    # sendtime = models.
    def __str__(self):
        return self.content

class Community_Message(models.Model):
    title = models.CharField(null=True, blank=True, max_length=200)
    community = models.OneToOneField(Community)
    author = models.ManyToManyField(User, related_name="publish_notice")
    content = models.TextField(null=True, blank=True)
    create_time = models.DateField(null=True, blank = True)
    def __str__(self):
        return self.content

# class Category(models.Model):
#     name = models.CharField(max_length=100)
#     def __str__(self):
#         return self.name
#
#
# class Tag(models.Model):
#     name = models.CharField(max_length=100)
#     def __str__(self):
#         return self.name

class Blog(models.Model):
    TYPE_CHOICES = {
        1: '普通',
        2: '通知',
    }
    title = models.CharField(max_length=70)
    body = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    type = models.SmallIntegerField(default=1, choices=TYPE_CHOICES.items())
    excerpt = models.CharField(max_length=200, blank=True)  # 摘要
    # category = models.ForeignKey(Category)  # 分类
    # tag = models.ManyToManyField(Tag, blank=True)  # 标签
    author = models.ForeignKey(Community, blank=True)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-created_time']

class Twit(models.Model):
    author = models.ForeignKey(Community, blank=True)
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return str(str(self.author) + "-" + str(self.id))

    class Meta:
        ordering = ['-created_time']

#联系集
class Account_Community(models.Model):
    account = models.ForeignKey(User, default=None, related_name='account_detail')
    community = models.ForeignKey(Community, default=None)
    class Meta:
        ordering = ['community']
    def __str__(self):
        return str(str(self.community) + "-" + str(self.account))

class Account_Activity(models.Model):
    account = models.ForeignKey(User, default=None)
    activity = models.ForeignKey(Activity, default=None)


#Saas部分
class MT_Tables(models.Model):
    name = models.CharField(max_length=20, null=True,)
    Tenant = models.ForeignKey(Community)

class MT_Fields(models.Model):
    dataTYPE_CHOICES = {
        1: 'char',
        2: 'int',
        3: 'bool',
    }
    dataType = models.SmallIntegerField(max_length=20, choices=dataTYPE_CHOICES.items(), default=1)
    name = models.CharField(max_length=20, null=True)
    table_ID = models.ForeignKey(MT_Tables)
    Tenant = models.ForeignKey(Community)
    field_Num = models.IntegerField()

class MT_Data(models.Model):
    Table = models.ForeignKey(MT_Tables)
    Tenant = models.ForeignKey(Community)
    value0 = models.CharField(max_length=20, null=True, blank=True)
    value1 = models.CharField(max_length=20, null=True, blank=True)
    value2 = models.CharField(max_length=20, null=True, blank=True)
    value13 = models.CharField(max_length=20, null=True, blank=True)
    value14 = models.CharField(max_length=20, null=True, blank=True)
    value15 = models.CharField(max_length=20, null=True, blank=True)
    value16 = models.CharField(max_length=20, null=True, blank=True)
    value17 = models.CharField(max_length=20, null=True, blank=True)
    value18 = models.CharField(max_length=20, null=True, blank=True)
    value19 = models.CharField(max_length=20, null=True, blank=True)
    value20 = models.CharField(max_length=20, null=True, blank=True)
    value21 = models.CharField(max_length=20, null=True, blank=True)
    value22 = models.CharField(max_length=20, null=True, blank=True)
    value23 = models.CharField(max_length=20, null=True, blank=True)
    value24 = models.CharField(max_length=20, null=True, blank=True)
    value25 = models.CharField(max_length=20, null=True, blank=True)
    value26 = models.CharField(max_length=20, null=True, blank=True)
    value27 = models.CharField(max_length=20, null=True, blank=True)
    value28 = models.CharField(max_length=20, null=True, blank=True)
    value29 = models.CharField(max_length=20, null=True, blank=True)
    value30 = models.CharField(max_length=20, null=True, blank=True)