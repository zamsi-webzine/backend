from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token


# 장고 공식 문서 참고
class ZSUserManager(BaseUserManager):
    def create_user(self, email, nickname, password=None):
        if not email:
            raise ValueError(_('Users must have an email address'))

        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password):
        user = self.create_user(
            email,
            nickname,
            password=password,
        )
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# 인증 관련 다중 상속만 추가: PermissionsMixin
class ZSUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name=_('Email address'),
        max_length=100,
        unique=True,
    )
    nickname = models.CharField(
        verbose_name=_('Nickname'),
        max_length=30,
        unique=True,
    )
    date_joined = models.DateTimeField(
        verbose_name=_('Date joined'),
        default=timezone.now
    )
    thumbnail = models.ImageField(
        verbose_name=_('Thumbnail'),
        upload_to='thumbnail',
        blank=True,
        null=True,
    )

    objects = ZSUserManager()

    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    class Meta:
        verbose_name = _('member')
        verbose_name_plural = _('members')
        ordering = ('-date_joined',)

    def __str__(self):
        return self.nickname

    @property
    def token(self):
        return Token.objects.get_or_create(user=self)[0]

    @property
    def is_staff(self):
        return self.is_superuser
