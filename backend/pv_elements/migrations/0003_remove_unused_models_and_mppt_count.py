from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pv_elements", "0002_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="PvString",
        ),
        migrations.DeleteModel(
            name="Installation",
        ),
        migrations.DeleteModel(
            name="Cable",
        ),
        migrations.RemoveField(
            model_name="inverter",
            name="mppt_count",
        ),
    ]
