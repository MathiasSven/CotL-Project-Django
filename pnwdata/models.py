from django.db import models


class Alliance(models.Model):
    id = models.IntegerField(primary_key=True)
    date_founded = models.DateTimeField()
    name = models.CharField(max_length=30)
    acronym = models.CharField(max_length=10, blank=True)
    color = models.CharField(max_length=10, blank=True)
    rank = models.IntegerField()
    members_count = models.IntegerField()
    score = models.FloatField()
    # leaders = models.ForeignKey('Nation', on_delete=models.CASCADE, null=True)
    # officers = models.ForeignKey()
    # heirs = models.ForeignKey()
    avg_score = models.FloatField()
    flag_url = models.URLField(blank=True)
    forum_url = models.URLField(blank=True)
    irc_chan = models.CharField(max_length=30)


class Nation(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    leader = models.CharField(max_length=30)
    continent = models.CharField(max_length=30)
    war_policy = models.CharField(max_length=30)
    color = models.CharField(max_length=30)
    alliance = models.ForeignKey(Alliance, on_delete=models.SET_DEFAULT, default=0)
    city_count = models.IntegerField()
    infrastructure = models.FloatField()
    offensive_war_count = models.IntegerField()
    defensive_war_count = models.IntegerField()
    score = models.FloatField()
    rank = models.IntegerField()
    vc_mode = models.IntegerField()
    minutes_since_active = models.IntegerField()


class Bank(models.Model):
    alliance = models.ForeignKey(Alliance, on_delete=models.CASCADE)
    tax_rate = models.IntegerField()
    resource_tax_rate = models.IntegerField()
    money = models.FloatField()
    food = models.FloatField()
    coal = models.FloatField()
    oil = models.FloatField()
    uranium = models.FloatField()
    iron = models.FloatField()
    bauxite = models.FloatField()
    lead = models.FloatField()
    gasoline = models.FloatField()
    munitions = models.FloatField()
    steel = models.FloatField()
    aluminum = models.FloatField()

class AllianceMember(models.Model):
    nation = models.ForeignKey(Nation, on_delete=models.CASCADE)
    alliance = models.ForeignKey(Alliance, on_delete=models.CASCADE)
"cityprojecttimerturns": 0,
"update_tz": 0,
"bauxiteworks": "0",
"ironworks": "1",
"armsstockpile": "0",
"emgasreserve": "0",
"massirrigation": "0",
"inttradecenter": "1",
"missilepad": "1",
"nuclearresfac": "1",
"irondome": "1",
"vitaldefsys": "1",
"intagncy": "1",
"uraniumenrich": "1",
"propbureau": "1",
"cenciveng": "1",
"city_planning": "0",
"adv_city_planning": "0",
"space_program": "1",
"spy_satellite": "1",
"moon_landing": "0",
"green_technologies": "0",
"telecommunications_satellite": "0",
"recycling_initiative": "1",
"pirate_economy": "0",
"clinical_research_center": null,
"specialized_police_training": null,
"arable_land_agency": null,
"adv_engineering_corps": null,
"money": "369836263.38",
"food": "23788.39",
"coal": "4216.33",
"oil": "1038.50",
"uranium": "18250.80",
"bauxite": "2219.75",
"iron": "13.41",
"lead": "873.75",
"gasoline": "11523.13",
"munitions": "13684.17",
"aluminum": "33146.89",
"steel": "49494.83",
"credits": "5",
"soldiers": "0",
"tanks": "17800",
"aircraft": "2130",
"ships": "129",
"missiles": "0",
"nukes": "0",
"spies": "60"