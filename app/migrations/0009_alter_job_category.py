# Generated by Django 5.1.3 on 2025-02-06 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_job_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='category',
            field=models.CharField(choices=[('信息技术与软件', '信息技术与软件'), ('零售与销售', '零售与销售'), ('教育与辅导', '教育与辅导'), ('酒店与服务行业', '酒店与服务行业'), ('其他', '其他')], max_length=50),
        ),
    ]
