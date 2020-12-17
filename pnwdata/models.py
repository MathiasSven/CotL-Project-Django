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
    avg_score = models.FloatField()
    flag_url = models.URLField(blank=True)
    forum_url = models.URLField(blank=True)
    irc_chan = models.CharField(max_length=30)

    last_updated = models.DateTimeField(auto_now=True)


class Nation(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    leader = models.CharField(max_length=30)
    continent = models.CharField(max_length=30)
    war_policy = models.CharField(max_length=30)
    color = models.CharField(max_length=30)
    alliance = models.ForeignKey(Alliance, on_delete=models.SET_DEFAULT, default=0)
    alliance_position = models.IntegerField()
    city_count = models.IntegerField()
    infrastructure = models.FloatField()
    offensive_war_count = models.IntegerField()
    defensive_war_count = models.IntegerField()
    score = models.FloatField()
    rank = models.IntegerField()
    vc_mode = models.IntegerField()
    minutes_since_active = models.IntegerField()

    last_updated = models.DateTimeField(auto_now=True)


class NationMilitary(models.Model):
    nation = models.OneToOneField(Nation, on_delete=models.CASCADE)

    soldiers = models.IntegerField()
    tanks = models.IntegerField()
    aircraft = models.IntegerField()
    ships = models.IntegerField()
    missiles = models.IntegerField()
    nukes = models.IntegerField()
    spies = models.IntegerField()

    last_updated = models.DateTimeField(auto_now=True)


class Projects(models.Model):
    nation = models.OneToOneField(Nation, on_delete=models.CASCADE)

    bauxiteworks = models.BooleanField(default=False)
    ironworks = models.BooleanField(default=False)
    armsstockpile = models.BooleanField(default=False)
    emgasreserve = models.BooleanField(default=False)
    massirrigation = models.BooleanField(default=False)
    inttradecenter = models.BooleanField(default=False)
    missilepad = models.BooleanField(default=False)
    nuclearresfac = models.BooleanField(default=False)
    irondome = models.BooleanField(default=False)
    vitaldefsys = models.BooleanField(default=False)
    intagncy = models.BooleanField(default=False)
    uraniumenrich = models.BooleanField(default=False)
    propbureau = models.BooleanField(default=False)
    cenciveng = models.BooleanField(default=False)
    city_planning = models.BooleanField(default=False)
    adv_city_planning = models.BooleanField(default=False)
    space_program = models.BooleanField(default=False)
    spy_satellite = models.BooleanField(default=False)
    moon_landing = models.BooleanField(default=False)
    green_technologies = models.BooleanField(default=False)
    telecommunications_satellite = models.BooleanField(default=False)
    recycling_initiative = models.BooleanField(default=False)
    pirate_economy = models.BooleanField(default=False)
    clinical_research_center = models.BooleanField(default=False)
    specialized_police_training = models.BooleanField(default=False)
    arable_land_agency = models.BooleanField(default=False)
    adv_engineering_corps = models.BooleanField(default=False)

    last_updated = models.DateTimeField(auto_now=True)


class Resources(models.Model):

    money = models.FloatField()
    food = models.FloatField()
    coal = models.FloatField()
    oil = models.FloatField()
    uranium = models.FloatField()
    bauxite = models.FloatField()
    iron = models.FloatField()
    lead = models.FloatField()
    gasoline = models.FloatField()
    munitions = models.FloatField()
    aluminum = models.FloatField()
    steel = models.FloatField()

    class Meta:
        abstract = True


class NationResources(Resources):
    nation = models.OneToOneField(Nation, on_delete=models.CASCADE)

    credits = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)


class Bank(Resources):
    alliance = models.OneToOneField(Alliance, on_delete=models.CASCADE)
    tax_rate = models.IntegerField()
    resource_tax_rate = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)


class Loan(Resources):
    nation = models.ForeignKey(Nation, on_delete=models.CASCADE)
    pay_by = models.DateField()


class Deposit(Resources):
    nation = models.ForeignKey(Nation, on_delete=models.CASCADE)


class AllianceMember(models.Model):
    nation = models.OneToOneField(Nation, on_delete=models.CASCADE)
    alliance = models.ForeignKey(Alliance, on_delete=models.CASCADE)

    city_project_timer_turns = models.IntegerField()
    update_tz = models.IntegerField()
