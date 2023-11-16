# Generated by Django 4.2.1 on 2023-10-15 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_fishmeponda_ingredient_recipe'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipePreparation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step', models.CharField(max_length=150)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='ingredient',
            name='unit',
            field=models.CharField(choices=[('cm', 'Cm'), ('lt', 'Lt'), ('kg', 'Kg'), ('gramas', 'Gramas'), ('peças', 'peças')], default='kg', max_length=8),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='quantity',
            field=models.IntegerField(),
        ),
        migrations.AddField(
            model_name='recipe',
            name='preparation_steps',
            field=models.ManyToManyField(blank=True, to='app.recipepreparation'),
        ),
    ]