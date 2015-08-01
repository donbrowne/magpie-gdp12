# Data migration #



Say we need to add 2 extra fields to support our rule builder

```
    lchoice = models.IntegerField(default=0,choices=ANDOR_LCHOICES)           
    rchoice = models.IntegerField(default=0,choices=ANDOR_RCHOICES)
```

The  2 fields above where (and will be again) added to end of the RulePremise model. Its not too bad as because the new fields are added to the end of the model class so the following should work.

```
./manage.py dumpdata knowledge --format xml > knowledge.xml 
./manage.py sqlclear knowledge | python manage.py dbshell
./manage.py syncdb
./manage.py loaddata knowledge.xml 
```

The first command  dumps the existing data to xml text file.
the second command drops the knowlege sql tables
the third recreates them with the new fields.
the fourth reloads the data.

The fourth works because the  xml file only contains data about existing fields so these are loaded as  normal. Because lchoice and rchoice are defined with a default value of 0 the new rows when recreated by django will have 0 values assigned to them meaning the existing rules will be used as they where previously.

We  can add exclude = ('lchoice','rchoice'). to the RulePremiseInline admin that will hide these 2 new fields from the admin view until such time as the rest of the code need to support them has been added