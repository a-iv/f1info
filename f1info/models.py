# -*- coding: utf-8 -*-
import datetime
from django.db import models
from decimal import Decimal
from markitup.fields import MarkupField
from beautifulsoup import BeautifulSoup, Tag
import urllib2

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

    @add_verbose_name(u'Лучшая позиция в гонках')
    def get_best_race_pos(self):
        try:
            races = self.results.filter(heat__type=Heat.RACE)
            positions = []
            for race in races:
                if race.is_classified():
                    positions.append(race.position)
            return min(positions)
        except ValueError:
            return '-'

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

    @add_verbose_name(u'Лучшая позиция на старте')
    def get_best_grid_pos(self):
        try:
            races = self.results.filter(heat__type=Heat.GRID)
            positions = []
            for race in races:
                if race.position not in positions:
                    positions.append(race.position)
            return min(positions)
        except ValueError:
            return '-'

    @add_verbose_name(u'Быстрейших кругов')
    def get_bestlap_count(self):
        return self.results.filter(heat__type=Heat.BEST, position=1).count()

    @add_verbose_name(u'Сходов')
    def get_fail_count(self):
        return self.results.exclude(retire__reason=None).exclude(retire__reason='25s penalty').exclude(dsq=True).count()
   
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

    @add_verbose_name(u'Последний двигатель')
    def get_last_engine(self):
        try:
            return get_last(self.results).engine
        except IndexError:
            pass

    ### This method needs improvement ###
    @add_verbose_name(u'Выступал за команды')
    def get_teams(self):
        teams = []
        for result in self.results.all():
            year_team = (result.heat.grandprix.season.year, result.team.name)
            if year_team not in teams:
                teams.append(year_team)
        return teams

### STATISTICS ###
def get_grandprix_stat():
    list = []
    for racer in Racer.objects.all():
        list.append((racer.get_grandprix_count(), racer))
    return sorted(list, reverse=True)[:100]
### END ###

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
        if minute:
            if minute < 10 and minute > 0:
                result += '%02d:' % minute
            else:
                result += '%2d:' % minute
        else:
            result += '%02d:' % minute
    else:
        result += '%2d:' % minute
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


def get_alpha(racers):
    list = []
    for racer in racers:
        list.append(racer.family_name[0])
    alpha = set(list)

    result = []
    for letter in alpha:
        result.append(racers.filter(family_name__istartswith=letter)[0].id)

    return racers.filter(id__in=result)


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
    info = MarkupField(default='', null=True, blank=True)

    def letters(self):
        return Racer.objects.filter(family_name__istartswith=self.family_name[0])

    def photo_check(self):
        try:
            if self.photo.size:
                return self.photo
        except:
            pass

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
    slug = models.SlugField(verbose_name=u'Слаг', max_length=4, blank=True)

    def get_next_season(self):
        next = Season.objects.filter(id__gt=self.id)
        if next:
            return next.order_by('year')[0]

    def get_prev_season(self):
        prev = Season.objects.filter(id__lt=self.id)
        if prev:
            return prev.order_by('-year')[0]

    def get_season_index(self):
        seasons = []
        for season in Season.objects.all():
            if season not in seasons:
                seasons.append(season)
        return seasons.index(self) + 1

    def get_racer_table(self):
        racers = []
        dict = {}
        
        for racer in Racer.objects.filter(results__heat__grandprix__season=self):
            if racer not in racers:
                setattr(racer, 'counted_results', [])
                racers.append(racer)
        
        for grandprix in self.grandprixs.all():
            list = []
            for heat in grandprix.heats.filter(type=Heat.RACE):
                left_racers = racers[:]
                for result in heat.results.filter(dsq=False):
                    if result.racer not in list:
                        list.append(result.racer)
                        racer = racers[racers.index(result.racer)]
                        points = result.get_points_count()
                        if points:
                            racer.counted_results.append(points)
                        else:
                            racer.counted_results.append(0)
                        try:
                            left_racers.remove(racer)
                        except ValueError:
                            continue
                for racer in left_racers:
                    racer.counted_results.append(-1)
                break
            else:
                for racer in racers:
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
            elif self.year == 1958 or self.year == 1960 or self.year in range(1963,1966):
                temp = sorted(racer.counted_results, reverse=True)[:6]
            elif self.year in range(1950,1954):
                temp = sorted(racer.counted_results, reverse=True)[:4]
            
            positive = 0
            for pts in temp:
                if pts >=0:
                    positive += pts
            
            outof = 0
            for pts in racer.counted_results:
                if pts >=0:
                    outof += pts
            
            test = []
            test.append(sorted(racer.counted_results, reverse=True))
            test.append(racer.counted_results)
            test.append([positive])
            test.append([outof])
            
            dict[racer] = test
        sorted_racers = sorted(dict.iteritems(), key=lambda x: (x[1][2], x[1][0]), reverse=True)
        return sorted_racers

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
        return teams


    ### It needs to detect heat type from template ###
    def get_most_victories(self):
        racers = []
        teams = []
        count_racers = []
        count_teams = []
        for result in Result.objects.filter(heat__grandprix__season=self, position=1, dsq=False, heat__type=Heat.RACE):
            racers.append(result.racer)
            teams.append(result.team)
        for racer in racers:
            count_racers.append((racers.count(racer), racer))
        for team in teams:
            count_teams.append((teams.count(team), team))

        return sorted(set(count_racers), reverse=True), sorted(set(count_teams), reverse=True)


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
    info = MarkupField(default='', null=True, blank=True)

    def get_most(self, filter):
        try:
            racers = []
            winners = []
            for result in Result.objects.filter(**filter):
                racers.append(result.racer)
            for racer in racers:
                winners.append((racers.count(racer), racer))
            counter = sorted(set(winners), reverse=True)
            temp = []
            for wins in counter:
                temp.append(wins[0])
            return counter[:temp.count(temp[0])]
        except IndexError:
            pass

    def get_most_wins(self):
        filter = { 'position': 1, 'dsq': False, 'heat__type': 'R', 'heat__grandprix__tracklen__track': self }
        return self.get_most(filter)

    def get_most_poles(self):
        filter = { 'position': 1, 'heat__type': 'G', 'heat__grandprix__tracklen__track': self }
        return self.get_most(filter)

    def __unicode__(self):
        return u'%s' % (self.name)


class TrackLen(VerboseModel):
    class Meta:
        ordering = ['track']
        verbose_name = u'Длина трассы'
        verbose_name_plural = u'Длины трассы'
    track = models.ForeignKey(Track, null=True, related_name='tracks')
    length = models.IntegerField(verbose_name=u'Длина трассы', default=0, blank=True)
    photo = models.ImageField(verbose_name=u'Схема', upload_to='upload/tracks/', null=True, blank=True)

    def convert_to_km(self):
        return float(self.length) / 1000

    def __unicode__(self):
        if self.track:
            return u'%s: %s' % (self.track, self.length)

class GPName(VerboseModel):
    class Meta:
        ordering = ['name']
        verbose_name = u'Гран-При'
        verbose_name_plural = u'Гран-При'
    name = models.CharField(verbose_name=u'Гран-При', max_length=100)
    en_name = models.CharField(verbose_name=u'English', max_length=100)
    abbr = models.CharField(verbose_name=u'Сокращённо', max_length=3, default='', blank=True)
    photo = models.ImageField(verbose_name=u'Фото', upload_to='upload/grandprix/', null=True, blank=True)

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

    def get_heats_by_date(self):
        dates = []
        days = []
        for heat in self.heats.all():
            if heat.date.date() not in dates:
                dates.append(heat.date.date())
        for day in dates:
            days.append(self.heats.filter(date__year=day.year, date__month=day.month, date__day=day.day))
        return days

    def get_winners(self):
        return Result.objects.filter(position=1, heat__type=Heat.RACE, heat__grandprix__name=self.name)

    def get_track_record(self, filter):
        results = Heat.objects.filter(**filter)
        times = {}
        for result in results:
            times[result] = result.time
        heat = min(times, key=times.get)
        try:
            return heat.get_results()[0]
        except:
            pass

    def get_qual_record(self):
        filter = { 'type': 'Q', 'grandprix__tracklen': self.tracklen }
        return self.get_track_record(filter)

    def get_race_record(self):
        filter = { 'type': 'B', 'grandprix__tracklen': self.tracklen }
        return self.get_track_record(filter)

    def __unicode__(self):
        return u'Гран-При %s %s' % (self.name, self.season)

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
    FP4 = '4'
    WARM = 'W'
    RACE = 'R'
    QUAL = 'Q'
    GRID = 'G'
    BEST = 'B'
    TYPE = (
        (FP1, u'Практика 1',),
        (FP2, u'Практика 2',),
        (FP3, u'Практика 3',),
        (FP4, u'Практика 4',),
        (QUAL, u'Квалификация',),
        (WARM, u'Warm-Up',),
        (GRID, u'Стартовое поле',),
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
        if not self.results.filter(heat__type=Heat.RACE):
            return self.results.filter(models.Q(retire__reason=None) | models.Q(laps__lte=self.laps / 10 + 1)).order_by('position')
        else:
            return self.results.filter(models.Q(retire__reason=None) | models.Q(laps__lte=self.laps / 10 + 1))

    def get_fails(self):
        return self.results.exclude(models.Q(retire__reason=None) | models.Q(laps__lte=self.laps / 10 + 1))
      
    def get_speed(self):
        if self.time:
            if self.type == self.RACE:
                return ((Decimal(self.grandprix.tracklen.length) * self.laps)/1000) / (self.time/3600)
            else:
                return (self.grandprix.tracklen.length/1000.0) / (float(self.time)/3600.0)

    def get_race_length(self):
        return ((Decimal(self.grandprix.tracklen.length) * self.laps)/1000)

    def __unicode__(self):
        return u'%s - %s' % (self.grandprix, self.get_type_display())


class Retire(VerboseModel):
    class Meta:
        ordering = ['reason']
        verbose_name = u'Причина'
        verbose_name_plural = u'Причины'
    reason = models.CharField(verbose_name=u'Причина', max_length=100)
    en_reason = models.CharField(verbose_name=u'English', max_length=100)

    def __unicode__(self):
        return u'%s' % self.reason
    

class Result(VerboseModel):
    class Meta:
        ordering = ['heat__date', 'delta', 'laps', 'position']
        verbose_name = u'Результат'
        verbose_name_plural = u'Результаты'
    heat = models.ForeignKey(Heat, verbose_name=u'Заезд', related_name='results')
    position = models.IntegerField(verbose_name=u'Поз')
    num = models.IntegerField(verbose_name=u'№', null=True, blank=True)
    racer = models.ForeignKey(Racer, verbose_name=u'Гонщик', related_name='results')
    team = models.ForeignKey(Team, verbose_name=u'Команда', related_name='results')
    engine = models.ForeignKey(Engine, verbose_name=u'Двигатель', related_name='results')
    tyre = models.ForeignKey(Tyre, verbose_name=u'Шины', related_name='results')
    delta = models.DecimalField(verbose_name=u'Отставание (время)', max_digits=8, decimal_places=3, null=True, blank=True)
    laps = models.IntegerField(verbose_name=u'Кругов заезда', null=True, blank=True)
    retire = models.ForeignKey(Retire, verbose_name=u'Причина схода', related_name='results', null=True, blank=True)
    comment = models.CharField(verbose_name=u'Комментарий', max_length=100, default='', blank=True)
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
            return '-'
        return time_to_str(self.heat.time + self.delta)

    def get_delta_display(self):
        u'Отставание'
        if self.heat.type == Heat.RACE and self.delta <= 0 and self.delta is not None:
            return ''
        elif self.heat.type != Heat.RACE and self.delta == 0:
            if self.position == 1:
                return ''
            else:
                return '+ %s' % self.delta
        elif self.delta is None:
            if self.laps == 1:
                return '+ %d %s' % (self.laps, u'круг')
            elif 2 <= self.laps <= 4:
                return '+ %d %s' % (self.laps, u'круга')
            elif 5 <= self.laps < 100:
                return '+ %d %s' % (self.laps, u'кругов')
            return ''
        else:
            ### if some bug will be found in Results display - here's the reason below, lol
            if self.delta < 0:
                return '- %s' % abs(self.delta) ### bydlo-code
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

