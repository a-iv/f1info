# -*- coding: utf-8 -*-

import datetime
from django.db import models
from django.core.cache import cache
from decimal import Decimal
#from f1info.fields import ResultField

class VerboseModel(models.Model):
    class Meta:
        abstract = True

    def get_verbose_name(self):
        result = {}
        for field in self._meta.fields:
            result[field.name] = field.verbose_name
        for name in dir(self):
            if not name.startswith('_'):
                try:
                    value = getattr(self, name)
                    if callable(value):
                        result[name] = value.verbose_name
                except AttributeError:
                    pass
        result['self'] = self._meta.verbose_name
        return result

def add_verbose_name(name):
    def wrapper(func):
        func.verbose_name = name
        return func
    return wrapper

class StatModel(VerboseModel):
    class Meta:
        abstract = True

    @add_verbose_name(u'Гонок')
    def get_race_count(self):
        return self.results.filter(heat__type=Heat.RACE).count()

    @add_verbose_name(u'Гран-При')
    def get_grand_prix_count(self):
        filter = {'heats__results__%s' % self._meta.module_name: self}
        grand_prixs = []
        for grand_prix in GrandPrix.objects.filter(**filter):
            if grand_prix not in grand_prixs:
                grand_prixs.append(grand_prix)
        return len(grand_prixs)

    @add_verbose_name(u'Сезонов')
    def get_season_count(self):
        filter = {'grandprixs__heats__results__%s' % self._meta.module_name: self}
        seasons = []
        for season in Season.objects.filter(**filter):
            if season not in seasons:
                seasons.append(season)
        return len(seasons)

    @add_verbose_name(u'Чемпион мира')
    def get_racer_champion(self):
        champion = []
        for racer in Champions.objects.filter(racer=self):
            if racer not in champion:
                champion.append(racer.season)
        return champion
    
    @add_verbose_name(u'Кубок конструкторов')
    def get_team_champion(self):
        constructor = []
        for team in Champions.objects.filter(team=self):
            if team not in constructor:
                constructor.append(team.season)
        return constructor

    @add_verbose_name(u'Побед')
    def get_win_count(self):
        return self.results.filter(heat__type=Heat.RACE, dsq=False, position=1).count()

    @add_verbose_name(u'Подиумов')
    def get_podium_count(self):
        return self.results.filter(heat__type=Heat.RACE, dsq=False, position__gte=1, position__lte=3).count()

    @add_verbose_name(u'Очков')
    def get_points_count(self):
        total = 0
        for result in self.results.filter(heat__type=Heat.RACE, dsq=False):
            total += result.get_points_count()
        return total

    @add_verbose_name(u'Поул-позишн')
    def get_poles_count(self):
        return self.results.filter(heat__type=Heat.GRID, position=1).count()

    @add_verbose_name(u'Быстрейших кругов')
    def get_bestlap_count(self):
        return self.results.filter(heat__type=Heat.BEST, position=1).count()

    @add_verbose_name(u'Сходов')
    def get_fail_count(self):
        return self.results.exclude(fail='').exclude(fail='25s penalty').exclude(dsq=True).count()
   
    @add_verbose_name(u'Возраст')
    def get_age(self):
        today = datetime.date.today()
        if self.deathday:
            delta = self.deathday.year - self.birthday.year - 1
            if datetime.date(self.birthday.year, self.deathday.month, self.deathday.day) >= self.birthday:
                delta += 1
        else:
            delta = today.year - self.birthday.year - 1
            if datetime.date(self.birthday.year, today.month, today.day) >= self.birthday:
                delta += 1
        
        if delta % 10 == 0:
            return str(delta) + u' лет'
        elif delta % 10 == 1:
            return str(delta) + u' год'
        elif delta % 10 in range(2,5):
            return str(delta) + u' года'
        elif delta % 10 in range(5,10):
            return str(delta) + u' лет'
        else:
            return delta
        
    @add_verbose_name(u'Первый Гран-При')
    def get_first_grandprix(self):
        try:
            return get_first(self.results).heat.grandprix
        except IndexError:
            pass

    @add_verbose_name(u'Последний Гран-При')
    def get_last_grandprix(self):
        try:
            return get_last(self.results).heat.grandprix
        except IndexError:
            pass

    def get_first_year(self):
        try:
            return get_first(self.results).heat.grandprix.season
        except IndexError:
            pass

    def get_last_year(self):
        try:
            return get_last(self.results).heat.grandprix.season
        except IndexError:
            pass

    @add_verbose_name(u'Последняя команда')
    def get_last_team(self):
        try:
            return get_last(self.results).team
        except IndexError:
            pass

    @add_verbose_name(u'Последние шины')
    def get_last_tyre(self):
        try:
            return get_last(self.results).tyre
        except IndexError:
            pass

    @add_verbose_name(u'Последний двигатель')
    def get_last_engine(self):
        try:
            return get_last(self.results).engine
        except IndexError:
            pass


def get_first(query_set):
    return query_set.all()[0]

def get_last(query_set):
    if query_set.model._meta.ordering:
        ordering = []
        for order in query_set.model._meta.ordering:
            if order.startswith('-'):
                order = order[1:]
            else:
                order = '-' + order
            ordering.append(order)
        return query_set.order_by(*ordering)[0]
    else:
        count = query_set.count()
        return query_set.all()[count - 1]


def time_to_str(time):
    millisecond = int((time % 1) * 1000)
    time = int(time)
    second = time % 60
    time = time / 60
    minute = time % 60
    hour = time / 60
    result = ''
    if hour:
        result += '%2d:' % hour
    #if minute:
        #if minute < 10 and minute > 0:
        #    result += '%2d:' % minute
        #else:
    result += '%02d:' % minute
    result += '%02d.%03d' % (second, millisecond)
    return result

def time_to_str_gap(time):
    millisecond = int((time % 1) * 1000)
    time = int(time)
    second = time % 60
    time = time / 60
    minute = time % 60
    result = ''
    if minute:
        if minute < 10:
            result += '%2d:' % minute
        else:
            result += '%02d:' % minute
        result += '%02d.%03d' % (second, millisecond)
    else:
        result += ' %2d.%03d' % (second, millisecond)
    return result


class Country(models.Model):
    class Meta:
        ordering = ['name']
        verbose_name = u'Страна'
        verbose_name_plural = u'Страны'
    name = models.CharField(verbose_name=u'Название', max_length=100)
    en_name = models.CharField(verbose_name=u'English', max_length=100)

    def __unicode__(self):
        return '%s' % self.name

class Racer(StatModel):
    class Meta:
        ordering = ['family_name', 'first_name', ]
        verbose_name = u'Гонщик'
        verbose_name_plural = u'Гонщики'
        unique_together = (
            ('family_name', 'first_name',),
        )
    first_name = models.CharField(verbose_name=u'Имя', max_length=100)
    family_name = models.CharField(verbose_name=u'Фамилия', max_length=100)
    en_first_name = models.CharField(verbose_name=u'Имя по-английски', max_length=100, default='', blank=True)
    en_family_name = models.CharField(verbose_name=u'Фамилия по-английски', max_length=100, default='', blank=True)
    slug = models.SlugField(verbose_name=u'Слаг', max_length=100, unique=True)
    country = models.ForeignKey(Country, verbose_name=u'Страна', related_name='racers', null=True, blank=True)
    birthday = models.DateField(verbose_name=u'Дата рождения', null=True, blank=True)
    deathday = models.DateField(verbose_name=u'Дата смерти', null=True, blank=True)
    comment = models.CharField(verbose_name=u'Комментарий', max_length=200, default='', blank=True)
    website = models.CharField(verbose_name=u'Веб-сайт', max_length=200, null=True, blank=True)
    twitter = models.CharField(verbose_name=u'Twitter', max_length=200, null=True, blank=True)
    photo = models.ImageField(verbose_name=u'Фото', upload_to='upload/drivers/', null=True, blank=True)

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.family_name)


class Engine(StatModel):
    class Meta:
        ordering = ['name']
        verbose_name = u'Двигатель'
        verbose_name_plural = u'Двигатели'
    name = models.CharField(verbose_name=u'Название', max_length=100)
    en_name = models.CharField(verbose_name=u'English', max_length=100)
    founder = models.CharField(verbose_name=u'Основатель', max_length=100, null=True, blank=True)
    country = models.ForeignKey(Country, verbose_name=u'Страна', related_name='engines', null=True, blank=True)
    website = models.CharField(verbose_name=u'Веб-сайт', max_length=200, null=True, blank=True)
    slug = models.SlugField(verbose_name=u'Слаг', max_length=100, unique=True)

    def __unicode__(self):
        return u'%s' % self.name


class Tyre(StatModel):
    class Meta:
        ordering = ['name']
        verbose_name = u'Шина'
        verbose_name_plural = u'Шины'
    name = models.CharField(verbose_name=u'Название', max_length=100)
    en_name = models.CharField(verbose_name=u'English', max_length=100)
    country = models.ForeignKey(Country, verbose_name=u'Страна', related_name='tyres', null=True, blank=True)
    slug = models.SlugField(verbose_name=u'Слаг', max_length=100, unique=True)

    def __unicode__(self):
        return u'%s' % self.name


class Team(StatModel):
    class Meta:
        ordering = ['name']
        verbose_name = u'Команда'
        verbose_name_plural = u'Команды'
    name = models.CharField(verbose_name=u'Название', max_length=100)
    en_name = models.CharField(verbose_name=u'English', max_length=100)
    founder = models.CharField(verbose_name=u'Основатель', max_length=100, null=True, blank=True)
    country = models.ForeignKey(Country, verbose_name=u'Страна', related_name='teams', null=True, blank=True)
    website = models.CharField(verbose_name=u'Веб-сайт', max_length=200, null=True, blank=True)
    slug = models.SlugField(verbose_name=u'Слаг', max_length=100, unique=True)

    def __unicode__(self):
        return '%s' % self.name

class Season(VerboseModel):
    class Meta:
        ordering = ['year']
        verbose_name = u'Сезон'
        verbose_name_plural = u'Сезоны'
    year = models.IntegerField(verbose_name=u'Год')

    def get_racer_table(self):
        racers = []
        #fastest = {}
        for racer in Racer.objects.filter(results__heat__grandprix__season=self):
            if racer not in racers:
                setattr(racer, 'counted_total', 0)
                setattr(racer, 'counted_out', 0)
                setattr(racer, 'counted_results', [])
                racers.append(racer)
        for grandprix in self.grandprixs.all():
#            for heat in grandprix.heats.filter(type=Heat.BEST):
#                for result in heat.results.filter(position=1):
#                    fastest = { grandprix : result.racer }
            
            for heat in grandprix.heats.filter(type=Heat.RACE):
                left_racers = racers[:]
                #fastest_racer = fastest[heat.grandprix]
                for result in heat.results.filter(dsq=False):
                    racer = racers[racers.index(result.racer)]
                    points = result.get_points_count()
#                    if racer == fastest_racer:
#                        points = points + 1
                    racer.counted_total += points
                    if points:
                        racer.counted_results.append(points)
                    else:
                        #racer.counted_results.append('-')
                        racer.counted_results.append(0)
                    left_racers.remove(racer)
                    
                for racer in left_racers:
                    #racer.counted_results.append('')
                    racer.counted_results.append(-1)
                break
            else:
                for racer in racers:
                    #racer.counted_results.append('')
                    racer.counted_results.append(-1)
            
        for racer in racers:
            temp = racer.counted_results
            if self.year in range(1981,1991):
                temp = sorted(racer.counted_results, reverse=True)[:11]
            elif self.year == 1980:
                temp = sorted(racer.counted_results[:7], reverse=True)[:5] + sorted(racer.counted_results[7:], reverse=True)[:5]
            elif self.year == 1979:
                temp = sorted(racer.counted_results[:7], reverse=True)[:4] + sorted(racer.counted_results[7:], reverse=True)[:4]
            elif self.year == 1978 or self.year == 1976:
                temp = sorted(racer.counted_results[:8], reverse=True)[:7] + sorted(racer.counted_results[8:], reverse=True)[:7]
            elif self.year == 1977:
                temp = sorted(racer.counted_results[:9], reverse=True)[:8] + sorted(racer.counted_results[9:], reverse=True)[:7]
            elif self.year == 1975:
                temp = sorted(racer.counted_results[:7], reverse=True)[:6] + sorted(racer.counted_results[7:], reverse=True)[:6]
            elif self.year == 1974 or self.year == 1973:
                temp = sorted(racer.counted_results[:8], reverse=True)[:7] + sorted(racer.counted_results[8:], reverse=True)[:6]
            elif self.year == 1972 or self.year == 1968:
                temp = sorted(racer.counted_results[:6], reverse=True)[:5] + sorted(racer.counted_results[6:], reverse=True)[:5]
            elif self.year == 1971 or self.year == 1969 or self.year == 1967:
                temp = sorted(racer.counted_results[:6], reverse=True)[:5] + sorted(racer.counted_results[6:], reverse=True)[:4]
            elif self.year == 1970:
                temp = sorted(racer.counted_results[:7], reverse=True)[:6] + sorted(racer.counted_results[7:], reverse=True)[:5]
            elif self.year == 1966 or self.year == 1962 or self.year == 1961 or self.year == 1959 or self.year in range(1954,1958):
                temp = sorted(racer.counted_results, reverse=True)[:5]
            elif self.year in range(1950,1954):
                temp = sorted(racer.counted_results, reverse=True)[:4]
            
            racer.counted_out = 0
            for pts in temp:
                if pts >= 0:
                    racer.counted_out += pts

        racers.sort(cmp=lambda a, b: int(b.counted_out - a.counted_out))
        return racers

    def get_team_table(self):
        teams = []
        for team in Team.objects.filter(results__heat__grandprix__season=self):
            if team not in teams:
                setattr(team, 'counted_total', 0)
                setattr(team, 'counted_results', [])
                teams.append(team)
        for grandprix in self.grandprixs.all():
            for heat in grandprix.heats.filter(type=Heat.RACE):
                for team in teams:
                    setattr(team, 'counted_temp', 0)
                left_teams = teams[:]
                for result in heat.results.filter(dsq=False):
                    team = teams[teams.index(result.team)]
                    points = result.get_points_count()
                    team.counted_total += points
                    team.counted_temp += points
                    if team in left_teams:
                        left_teams.remove(team)
                for team in teams:
                    if team in left_teams:
                        team.counted_results.append('')
                    elif team.counted_temp:
                        team.counted_results.append(team.counted_temp)
                    else:
                        team.counted_results.append('-')
                break
            else:
                for team in teams:
                    team.counted_results.append('')
                
        teams.sort(cmp=lambda a, b: int(b.counted_total - a.counted_total))
        #cache.set("teams", teams, 36000)
        return teams


    def __unicode__(self):
        return u'%d' % self.year


class Champions(VerboseModel):
    class Meta:
        ordering = ['season']
        verbose_name = u'Чемпион'
        verbose_name_plural = u'Чемпионы'
    season = models.ForeignKey(Season, verbose_name=u'Сезон', related_name='champions', unique=True)
    racer = models.ForeignKey(Racer, verbose_name=u'Гонщик', related_name='champions')
    team = models.ForeignKey(Team, verbose_name=u'Команда', related_name='champions', null=True, blank=True)

    def __unicode__(self):
        return u'%s: %s %s' % (self.season, self.racer, self.team)


class Point(VerboseModel):
    class Meta:
        ordering = ['season', 'position']
        verbose_name = u'Очки'
        verbose_name_plural = u'Очки'
        unique_together = (
            ('season', 'position',),
        )
    season = models.ForeignKey(Season, verbose_name=u'Сезон', related_name='points')
    position = models.IntegerField(verbose_name=u'Место')
    point = models.IntegerField(verbose_name=u'Очки')

    def __unicode__(self):
        return u''


class Track(VerboseModel):
    class Meta:
        ordering = ['name']
        verbose_name = u'Трасса'
        verbose_name_plural = u'Трассы'
    name = models.CharField(verbose_name=u'Трасса', max_length=100)
    en_name = models.CharField(verbose_name=u'English', max_length=100)
    slug = models.SlugField(verbose_name=u'Слаг', max_length=100, unique=True)
    googlemaps = models.CharField(verbose_name=u'Google Maps', max_length=300, default='', blank=True)
    website = models.CharField(verbose_name=u'Веб-сайт', max_length=100, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % (self.name)


class TrackLen(VerboseModel):
    class Meta:
        ordering = ['length']
        verbose_name = u'Длина трассы'
        verbose_name_plural = u'Длины трассы'
    track = models.ForeignKey(Track, null=True)
    length = models.IntegerField(verbose_name=u'Длина трассы', default=0, blank=True)
    photo = models.ImageField(verbose_name=u'Схема', upload_to='upload/tracks/', null=True, blank=True)

    def __unicode__(self):
        if self.track:
            return u'%s: %s' % (self.track, self.length)
        else:
            return u''

class GPName(VerboseModel):
    class Meta:
        ordering = ['name']
        verbose_name = u'Гран-При'
        verbose_name_plural = u'Гран-При'
    name = models.CharField(verbose_name=u'Гран-При', max_length=100)
    en_name = models.CharField(verbose_name=u'English', max_length=100)
    abbr = models.CharField(verbose_name=u'Сокращённо', max_length=3, default='', blank=True)

    def __unicode__(self):
        return u'%s' % self.name

class GrandPrix(VerboseModel):
    class Meta:
        ordering = ['season__year', 'index']
        verbose_name = u'Гран-при'
        verbose_name_plural = u'Гран-при'
        unique_together = (
            ('season', 'name',),
        )

    index = models.IntegerField(verbose_name=u'Индекс', null=True)
    season = models.ForeignKey(Season, verbose_name=u'Сезон', related_name='grandprixs')
    name = models.ForeignKey(GPName, verbose_name=u'Гран-При', related_name='grandprixs', null=True, blank=True)
    slug = models.SlugField(verbose_name=u'Слаг', max_length=100, unique=True)
    country = models.ForeignKey(Country, verbose_name=u'Страна', related_name='grandprixs', null=True, blank=True)
    tracklen = models.ForeignKey(TrackLen, verbose_name=u'Трасса', related_name='tracks', null=True, blank=True)

    def __unicode__(self):
        return u'%s: %s' % (self.season, self.name)


class Heat(VerboseModel):
    class Meta:
        ordering = ['date']
        verbose_name = u'Заезд'
        verbose_name_plural = u'Заезды'
        unique_together = (
            ('grandprix', 'type',),
        )
    FP1 = '1'
    FP2 = '2'
    FP3 = '3'
    WARM = 'W'
    RACE = 'R'
    QUAL = 'Q'
    GRID = 'G'
    BEST = 'B'
    TYPE = (
        (FP1, u'Практика 1',),
        (FP2, u'Практика 2',),
        (FP3, u'Практика 3',),
        (QUAL, u'Квалификация',),
        (WARM, u'Warm-up',),
        (GRID, u'Стартовая решетка',),
        (BEST, u'Быстрейшие круги',),
        (RACE, u'Гонка',),
    )
    grandprix = models.ForeignKey(GrandPrix, verbose_name=u'Гран-При', related_name='heats')
    type = models.CharField(verbose_name=u'Тип', max_length=1, choices=TYPE)
    date = models.DateTimeField(verbose_name=u'Дата', default=datetime.datetime.now)
    time = models.DecimalField(verbose_name=u'Время победителя', max_digits=8, decimal_places=3)
    laps = models.IntegerField(verbose_name=u'Кругов заезда', null=True, blank=True)
    half_points = models.BooleanField(verbose_name=u'Делить очки пополам', default=False)
    slug = models.SlugField(verbose_name=u'Слаг', max_length=100, unique=True)

    def get_results(self):
        return self.results.filter(models.Q(fail='') | models.Q(laps__lte=self.laps / 10 + 1))

    def get_fails(self):
        return self.results.exclude(models.Q(fail='') | models.Q(laps__lte=self.laps / 10 + 1))
      
    def get_speed(self):
        if self.type == self.RACE:
            return ((Decimal(self.grandprix.tracklen.length) * self.laps)/1000) / (self.time/3600)
        else:
            return (self.grandprix.tracklen.length/1000.0) / (float(self.time)/3600.0)

    def __unicode__(self):
        return u'%s - %s' % (self.grandprix, self.get_type_display())


class Result(VerboseModel):
    class Meta:
        ordering = ['heat__date', 'position']
        verbose_name = u'Результат'
        verbose_name_plural = u'Результаты'
        unique_together = (
            ('racer', 'heat',),
        )
    heat = models.ForeignKey(Heat, verbose_name=u'Заезд', related_name='results')
    position = models.IntegerField(verbose_name=u'Поз')
    num = models.IntegerField(verbose_name=u'№', null=True, blank=True)
    racer = models.ForeignKey(Racer, verbose_name=u'Гонщик', related_name='results')
    team = models.ForeignKey(Team, verbose_name=u'Команда', related_name='results')
    engine = models.ForeignKey(Engine, verbose_name=u'Двигатель', related_name='results')
    tyre = models.ForeignKey(Tyre, verbose_name=u'Шины', related_name='results')
    delta = models.DecimalField(verbose_name=u'Отставание (время)', max_digits=8, decimal_places=3, null=True, blank=True)
    laps = models.IntegerField(verbose_name=u'Кругов заезда', null=True, blank=True)
    fail = models.CharField(verbose_name=u'Причина схода', max_length=100, default='', blank=True)
    dsq = models.BooleanField(verbose_name=u'DSQ', default=False, blank=True)

    _points_count = models.FloatField(default=0)

    def is_classified(self):
        u'Классифицируется'
        if self.laps is None:
            return True
        elif self.delta or self.delta == 0:
            return True
        return self.heat.laps / 10 + 1 >= self.laps

    def get_time_display(self):
        u'Время'
        if self.delta is None:
            return ''
        return time_to_str(self.heat.time + self.delta)

    def get_delta_display(self):
        u'Отставание'
        if self.delta == 0:
            return ''
        elif self.delta is None:
            if self.laps == 1:
                return '+%d %s' % (self.laps, u'круг')
            elif 2 <= self.laps <= 4:
                return '+%d %s' % (self.laps, u'круга')
            elif 5 <= self.laps < 100:
                return '+%d %s' % (self.laps, u'кругов')
            return ''
        else:
            return '+%s' % time_to_str_gap(self.delta)
    
    def get_lap_display(self):
        u'Круг схода'
        if self.delta == 0:
            return ''
        elif self.delta is None:
            self.lap = self.heat.laps - self.laps
            return self.lap
        else:
            return '+%s' % time_to_str_gap(self.delta)
        
    def _get_points_count(self):
        if self.heat.type != Heat.RACE:
            return 0
        try:
            value = self.heat.grandprix.season.points.get(position=self.position).point
            if self.heat.half_points:
                value /= 2.0
            if not self.is_classified():
                value = 0
            return value
        except models.ObjectDoesNotExist:
            return 0

    def get_points_count(self):
        return self._points_count

    def save(self, *args, **kwargs):
        self._points_count = self._get_points_count()
        super(Result, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.racer


class BestLap(VerboseModel):
    class Meta:
        ordering = ['heat__date', 'result', ]
        verbose_name = u'Лучший круг'
        verbose_name_plural = u'Лучшие круги'
        unique_together = (
            ('heat', 'result',),
        )
    heat = models.ForeignKey(Heat, verbose_name=u'Заезд', related_name='bests')
    result = models.ForeignKey(Result, verbose_name=u'Результат', related_name='bests')
    lap = models.IntegerField(verbose_name=u'Круг')
    time = models.DecimalField(verbose_name=u'Время круга', max_digits=8, decimal_places=3)

    def get_time_display(self):
        u'Время'
        if self.time is None:
            return ''
        return time_to_str(self.time)

    def __unicode__(self):
        return u''
