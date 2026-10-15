from django.db import models

class Todo(models.Model):
    title = models.CharField("제목", max_length=200)
    content = models.TextField("세부 내용", blank=True)
    is_completed = models.BooleanField("완료 여부", default=False, db_default=False)
    created_at = models.DateTimeField("생성 일시", auto_now_add=True)

    class Meta:
        db_table = "todos_todo"
        ordering = ["-created_at", "-pk"]
        verbose_name = "할 일"
        verbose_name_plural = "할 일 목록"

    def __str__(self):
        return self.title
