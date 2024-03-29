# Generated by Django 4.2.3 on 2024-01-20 11:19

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Opinion',
            fields=[
                ('ident', models.BigAutoField(primary_key=True, serialize=False)),
                ('puntuacion', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('texto', models.CharField(max_length=200)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('autor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
