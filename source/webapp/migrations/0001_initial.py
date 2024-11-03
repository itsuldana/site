from django.conf import settings
import django.contrib.postgres.fields

from django.db import migrations, models
import django.db.models.deletion
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Name')),
                ('description', models.TextField(max_length=3000, verbose_name='Description')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price')),
                ('image', models.ImageField(blank=True, null=True, upload_to='course_images/', verbose_name='Image')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated at')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestModule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='New titile', max_length=255, verbose_name='Name')),
                ('description', django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='Описание')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('position', models.PositiveIntegerField(default=1)),
                ('time_limit', models.PositiveIntegerField(default=30, verbose_name='Лимит времени (минуты)')),
                ('cours', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_modules', to='webapp.course', verbose_name='Тестовый модуль')),
            ],
        ),
        migrations.CreateModel(
            name='TestCaseDescriptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Default Title', max_length=255, verbose_name='Name')),
                ('description', django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='Описание')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('сourse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_case_descriptions', to='webapp.course', verbose_name='Тестовый модуль')),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Вопрос')),
                ('test_module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests', to='webapp.testmodule', verbose_name='Тестовый модуль')),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_date', models.DateTimeField(auto_now_add=True)),
                ('payment_status', models.CharField(choices=[('PENDING', 'В ожидании'), ('DONE', 'Оплачено')], default='PENDING', max_length=20)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to='webapp.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('description', models.TextField(blank=True, max_length=2000, null=True, verbose_name='Описание')),
                ('position', models.PositiveIntegerField(verbose_name='Position')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated at')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='webapp.course', verbose_name='Модуль')),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('small_description', models.TextField(max_length=255, verbose_name='Краткое описание')),
                ('content', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Content')),
                ('video_url', models.URLField(blank=True, max_length=1000, null=True, verbose_name='Видео URL')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated at')),
                ('thumbnail_url', models.URLField(blank=True, max_length=1000, null=True, verbose_name='URL превью')),
                ('duration', models.IntegerField(blank=True, null=True, verbose_name='Длительность видео')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator', to=settings.AUTH_USER_MODEL, verbose_name='Создатель')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='webapp.module', verbose_name='Модуль')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='tag',
            field=models.ManyToManyField(blank=True, related_name='tags', to='webapp.tag'),
        ),
        migrations.CreateModel(
            name='AnswerOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Ответ')),
                ('is_correct', models.BooleanField(default=False, verbose_name='Правильный ответ')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_options', to='webapp.test', verbose_name='Тест')),
            ],
        ),
        migrations.CreateModel(
            name='TestHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct_answer_ids', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, size=None, verbose_name='ID правильных ответов')),
                ('user_answer_ids', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, size=None, verbose_name='ID ответов пользователя')),
                ('completed_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата завершения')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_histories', to='webapp.test', verbose_name='Тест')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_histories', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'История прохождения теста',
                'verbose_name_plural': 'Истории прохождения тестов',
                'unique_together': {('user', 'test')},
            },
        ),
        migrations.CreateModel(

            name='LessonProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('in_progress', 'В процессе'), ('done', 'Закончен')], default='in_progress', max_length=50, verbose_name='Статус')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('finished_at', models.DateTimeField(blank=True, null=True, verbose_name='Дата завершения')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_progress', to='webapp.lesson', verbose_name='Урок')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_progress', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'unique_together': {('lesson', 'user')},
            },
        ),
    ]
