from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    title = models.CharField(max_length=100)
    mamo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# models.CASCADE = если пользователь будет удалён, то удаляются всего его задачи
# models.PROTECT = если у пользователя существует хотя бы 1 задача, то его нельзя удалить
# models.SET_NULL = если удалится родительский объект - пользователь, то поле примет значение NULL
# models.SET_DEFAULT = то же, что и SET_NULL, только вместо Null указатель смещается на default значения