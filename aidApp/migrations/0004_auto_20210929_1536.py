# Generated by Django 3.2.4 on 2021-09-29 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aidApp', '0003_alter_patient_d_o_b'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='age',
            field=models.CharField(default=1, max_length=5),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='patient',
            name='D_O_B',
            field=models.CharField(max_length=20),
        ),
    ]