# Generated by Django 5.2 on 2025-06-30 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0002_rename_assignee_task_assigned_to'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('event_type', models.CharField(choices=[('meeting', 'Meeting'), ('workshop', 'Workshop'), ('party', 'Party'), ('competition', 'Competition'), ('other', 'Other')], default='meeting', max_length=20)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('location', models.CharField(max_length=255)),
                ('department', models.CharField(blank=True, choices=[('finance', 'Finance'), ('marketing', 'Marketing'), ('visual_creation', 'Visual Creation'), ('technical_team', 'Technical Team'), ('er', 'Er'), ('hr', 'Hr')], max_length=20, null=True)),
                ('is_mandatory', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('upcoming', 'Upcoming'), ('ongoing', 'Ongoing'), ('completed', 'Completed'), ('canceled', 'Canceled')], default='upcoming', max_length=20)),
                ('event_photo', models.ImageField(blank=True, null=True, upload_to='event_photos/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
