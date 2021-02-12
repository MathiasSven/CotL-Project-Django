from django.db import models
from django.utils.timezone import now
from datetime import datetime, timedelta


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

    def active_days_since(self, days_ago=0):
        active_days = 0
        for i in range(days_ago + 1):
            if self.activity_set.filter(active_datetime__date=datetime.utcnow() - timedelta(days=i)):
                active_days += 1
        return active_days

    def activity_on(self, date: datetime):
        return self.activity_set.filter(active_datetime__date=date)

    def get_activity(self):
        activity = self.activity_set.all().order_by('active_datetime')
        data = {"nationid": self.nation.nationid, "activity": {}}
        activity_dict = data["activity"]
        for activity_object in activity:

            year = activity_object.active_datetime.year
            month = activity_object.active_datetime.month
            day = activity_object.active_datetime.day

            if year not in activity_dict.keys():
                activity_dict[year] = {}
            if month not in activity_dict[year].keys():
                activity_dict[year][month] = {}
            if day not in activity_dict[year][month].keys():
                activity_dict[year][month][day] = 1
            else:
                activity_dict[year][month][day] += 1

        return data

    class Meta:
        ordering = ['nation__nationid']

    def __str__(self):
        return '%s (%s) Alliance Member' % (self.nation.nation, self.nation.nationid)


class Activity(models.Model):
    nation = models.ForeignKey(AllianceMember, on_delete=models.CASCADE)
    active_datetime = models.DateTimeField()

    class Meta:
        verbose_name = 'activity'
        verbose_name_plural = 'activity'


class TaxRecord(Resources):
    nation = models.ForeignKey(Nation, on_delete=models.CASCADE)
    date = models.DateTimeField()
    note = models.CharField(max_length=30)
    tax_id = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['nation', 'date'], name='unique_tax_record'),
        ]

    def __str__(self):
        return '%s (%s) Tax Record' % (self.nation.nation, self.nation.nationid)


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

    def available_holdings(self):
        withdraw_requests = Request.objects.filter(nation=self.nation, status=None)
        holdings_dict = filter_kwargs(Resources, self.__dict__)
        if not withdraw_requests:
            return holdings_dict
        for withdraw_request in withdraw_requests:
            withdraw_dict = withdraw_request.__dict__
            for key in holdings_dict:
                if key in withdraw_dict:
                    holdings_dict[key] -= withdraw_dict[key]
                else:
                    pass
        return holdings_dict

    def frozen_holdings(self):
        withdraw_requests = Request.objects.filter(nation=self.nation, status=None)
        if not withdraw_requests:
            return
        withdraws_dict = {f.name: 0 for f in Resources._meta.get_fields()}
        for withdraw_request in withdraw_requests:
            withdraw_dict = withdraw_request.__dict__
            for key in withdraws_dict:
                if key in withdraw_dict:
                    withdraws_dict[key] += withdraw_dict[key]
                else:
                    pass
        return withdraws_dict

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


class Deposit(Resources):
    tx_id = models.BigIntegerField(null=True, unique=True)
    deposited_on = models.DateTimeField(default=now)
    nation = models.ForeignKey(Nation, on_delete=models.CASCADE)

    def save(self, *args, **kw):
        if not self._state.adding:
            return None

        deposit_dict = filter_kwargs(Resources, self.__dict__)
        holding_exists = Holdings.objects.filter(nation=self.nation)
        if holding_exists:
            holding_dict = holding_exists[0].__dict__
            for key in holding_dict:
                if key in deposit_dict:
                    deposit_dict[key] += holding_dict[key]
                else:
                    pass
            holding_exists.update(**filter_kwargs(Resources, deposit_dict))
        else:
            Holdings.objects.create(
                nation=self.nation, **filter_kwargs(Resources, deposit_dict))

        super(Deposit, self).save(*args, **kw)

    def __str__(self):
        return f'Deposit ({self.tx_id}) by {self.nation.nation} ({self.nation.nationid})'


class Withdraw(Resources):
    tx_id = models.BigIntegerField(null=True, unique=True)
    withdrew_on = models.DateTimeField(default=now)
    nation = models.ForeignKey(Nation, on_delete=models.CASCADE)

    def save(self, *args, **kw):
        if not self._state.adding:
            return None

        withdraw_dict = filter_kwargs(Resources, self.__dict__)
        holding_exists = Holdings.objects.filter(nation=self.nation)
        holding_object = holding_exists[0]
        if holding_exists:
            holding_dict = holding_object.__dict__
            for key in holding_dict:
                if key in withdraw_dict:
                    holding_dict[key] -= withdraw_dict[key]
                else:
                    pass
            holding_dict.pop('_state')
            holding_exists.update(**filter_kwargs(Resources, holding_dict))

        super(Withdraw, self).save(*args, **kw)


class Request(Resources):
    STATUS_CHOICES = [
        ('Y', 'ACCEPTED'),
        ('N', 'DECLINED'),
        (None, 'PROCESSING')
    ]

    REQUEST_TYPE_CHOICES = [
        ('AID', 'Aid Request'),
        ('WITHDRAW', 'Withdraw Request'),
        ('LOAN', 'Loan Request')
    ]

    request_on = models.DateTimeField(auto_now=True)
    nation = models.ForeignKey(Nation, on_delete=models.CASCADE)
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPE_CHOICES)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=None, null=True)

    pay_by = models.DateField(null=True, blank=True)

    def request_link(self):

        request_link = f"https://politicsandwar.com/alliance/id=7452&display=bank&w_type=nation&w_recipient={self.nation.nation.replace(' ', '%20')}&w_note={self.request_type}"
        res_dict = filter_kwargs(Resources, self.__dict__)
        for res in res_dict:
            request_link += f"&w_{res}={int(res_dict[res])}"
        return request_link

    def save(self, *args, **kw):
        from .tasks import send_message
        if self.status == 'Y':
            if self.request_type == "WITHDRAW":
                new_withdraw_object = Withdraw(**filter_kwargs(Resources, self.__dict__))
                new_withdraw_object.nation = self.nation
                new_withdraw_object.save()
            if self.request_type == "LOAN":
                new_loan_object = Withdraw(**filter_kwargs(Loan, self.__dict__))
                new_loan_object.nation = self.nation
                new_loan_object.save()
            send_message(nation_id=self.nation.nationid, subject=f"{self.request_type} ACCEPTED", message=f"{filter_kwargs(Resources, self.__dict__)}")
        if self.status == 'N':
            send_message(nation_id=self.nation.nationid, subject=f"{self.request_type} DECLINED", message=f"{filter_kwargs(Resources, self.__dict__)}")
        else:
            send_message(nation_id=self.nation.nationid, subject=f"{self.request_type} PROCESSING", message=f"{filter_kwargs(Resources, self.__dict__)}")
        super(Request, self).save(*args, **kw)

    def __str__(self):
        return f'{self.request_type} by {self.nation.nation} ({self.nation.nationid})'
