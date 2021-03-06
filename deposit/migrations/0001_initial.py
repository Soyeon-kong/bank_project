# Generated by Django 3.0.6 on 2020-06-11 06:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('deposit_id', models.IntegerField(primary_key=True, serialize=False)),
                ('bank', models.CharField(max_length=100)),
                ('product', models.CharField(max_length=100)),
                ('rate_6', models.CharField(default='-', max_length=100)),
                ('rate_12', models.CharField(default='-', max_length=100)),
                ('rate_24', models.CharField(default='-', max_length=100)),
                ('rate_36', models.CharField(default='-', max_length=100)),
                ('rate_type', models.CharField(default='', max_length=100)),
                ('join_way', models.CharField(default='', max_length=100)),
                ('mtrt_int', models.TextField(default='')),
                ('spcl_cnd', models.TextField(default='')),
                ('join_member', models.CharField(default='', max_length=100)),
                ('etc_note', models.TextField(default='')),
                ('max_limit', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Mydepositlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100)),
                ('member_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='member.Member')),
            ],
        ),
    ]
