from django.contrib.auth.models import AbstractUser


class AdminUser(AbstractUser):
    """Модель для создания администраторов."""

    class Meta:
        ordering = ("id",)
        verbose_name = "Администратор"
        verbose_name_plural = "Администраторы"

    def __str__(self):
        return self.username
