from django.db import models


# noinspection PyProtectedMember
def filter_kwargs(model, arg_dict):
    model_fields = [f.name for f in model._meta.get_fields()]
    return {k: v for k, v in arg_dict.items() if k in model_fields}


class Alliance(models.Model):
    id = models.IntegerField(primary_key=True)
    founddate = models.DateTimeField(null=True)
    name = models.CharField(max_length=30, null=True)
    acronym = models.CharField(max_length=10, null=True)
    color = models.CharField(max_length=10, null=True)
    rank = models.IntegerField(null=True)
    members = models.IntegerField(null=True)
    score = models.FloatField(null=True)
    avgscore = models.FloatField(null=True)
    flagurl = models.URLField(blank=True)
    forumurl = models.URLField(blank=True)
    ircchan = models.CharField(max_length=30, null=True)

    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s (%s)' % (self.name, self.id)


class Nation(models.Model):
    nationid = models.IntegerField(primary_key=True)
    nation = models.CharField(max_length=30, null=True)
    leader = models.CharField(max_length=30, null=True)
    continent = models.CharField(max_length=30, null=True)
    war_policy = models.CharField(max_length=30, null=True)
    color = models.CharField(max_length=30, null=True)
    alliance = models.ForeignKey(Alliance, on_delete=models.SET_NULL, blank=True, null=True)
    allianceposition = models.IntegerField(null=True)
    cities = models.IntegerField(null=True)
    infrastructure = models.FloatField(null=True)
    offensivewars = models.IntegerField(null=True)
    defensivewars = models.IntegerField(null=True)
    score = models.FloatField(null=True)
    rank = models.IntegerField(null=True)
    vacmode = models.IntegerField(null=True)
    minutessinceactive = models.IntegerField(null=True)

    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s (%s)' % (self.nation, self.nationid)


class NationMilitary(models.Model):
    nation = models.OneToOneField(Nation, on_delete=models.CASCADE, primary_key=True)

    soldiers = models.IntegerField(null=True)
    tanks = models.IntegerField(null=True)
    aircraft = models.IntegerField(null=True)
    ships = models.IntegerField(null=True)
    missiles = models.IntegerField(null=True)
    nukes = models.IntegerField(null=True)
    spies = models.IntegerField(null=True)

    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s (%s) Military' % (self.nation.nation, self.nation.nationid)


class Projects(models.Model):
    nation = models.OneToOneField(Nation, on_delete=models.CASCADE, primary_key=True)

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

    def project_count(self):
        model_fields = [f.name for f in self._meta.get_fields() if isinstance(f, models.fields.BooleanField)]
        projects = {k: v for k, v in self.__dict__.items() if k in model_fields}
        return sum(projects.values())

    def __str__(self):
        return '%s (%s) Projects' % (self.nation.nation, self.nation.nationid)


class Resources(models.Model):
    money = models.FloatField(null=True, default=0)
    food = models.FloatField(null=True, default=0)
    coal = models.FloatField(null=True, default=0)
    oil = models.FloatField(null=True, default=0)
    uranium = models.FloatField(null=True, default=0)
    bauxite = models.FloatField(null=True, default=0)
    iron = models.FloatField(null=True, default=0)
    lead = models.FloatField(null=True, default=0)
    gasoline = models.FloatField(null=True, default=0)
    munitions = models.FloatField(null=True, default=0)
    aluminum = models.FloatField(null=True, default=0)
    steel = models.FloatField(null=True, default=0)

    class Meta:
        abstract = True


class Bank(Resources):
    alliance = models.OneToOneField(Alliance, on_delete=models.CASCADE, primary_key=True)
    taxrate = models.IntegerField()
    resource_taxrate = models.IntegerField()

    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s (%s) Bank' % (self.alliance.name, self.alliance.id)


class AllianceMember(Resources):
    credits = models.FloatField()

    nation = models.OneToOneField(Nation, on_delete=models.CASCADE, primary_key=True)

    cityprojecttimerturns = models.IntegerField(null=True)
    update_tz = models.IntegerField(null=True)

    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s (%s) Alliance Member' % (self.nation.nation, self.nation.nationid)


class Loan(Resources):
    nation = models.ForeignKey(Nation, on_delete=models.CASCADE)
    borrowing_date = models.DateField(auto_now_add=True)
    pay_by = models.DateField(null=True)
    payed = models.BooleanField(default=False)
    payed_on = models.DateField(null=True)

    def save(self, *args, **kw):
        if self.payed:
            self.payed_on = models.fields.datetime.datetime.utcnow()
        super(Loan, self).save(*args, **kw)

    def __str__(self):
        return 'Loan by %s (%s)' % (self.nation.nation, self.nation.nationid)


class Holdings(Resources):
    nation = models.OneToOneField(Nation, on_delete=models.CASCADE, primary_key=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'holdings'
        verbose_name_plural = 'holdings'
    
    def save(self, *args, **kw):
        model_fields = [f.name for f in self._meta.get_fields() if isinstance(f, models.fields.FloatField)]
        projects = {k: v for k, v in self.__dict__.items() if k in model_fields}
        if sum(projects.values()) <= 0:
            self.delete()
        else:
            super(Holdings, self).save(*args, **kw)

    def __str__(self):
        return '%s (%s) Holdings' % (self.nation.nation, self.nation.nationid)
