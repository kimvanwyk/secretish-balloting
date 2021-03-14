# Generated by Django 3.1.7 on 2021-03-14 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('balloting', '0005_voter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voter',
            name='description_text',
            field=models.CharField(help_text='A descriptive note for this voter', max_length=200, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='voter',
            name='email_text',
            field=models.EmailField(max_length=254, verbose_name='Email address'),
        ),
        migrations.AlterField(
            model_name='voter',
            name='emailed_bool',
            field=models.BooleanField(default=False, verbose_name='Voter has been emailed voting instructions'),
        ),
        migrations.AlterField(
            model_name='voter',
            name='url_fragment_text',
            field=models.CharField(blank=True, default=None, max_length=20, null=True, unique=True),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='balloting.choice')),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='balloting.voter')),
            ],
        ),
    ]
