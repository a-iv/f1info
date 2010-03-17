# -*- coding: utf-8 -*-

import datetime
from django.db import models

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
        return GrandPrix.objects.filter(**filter).count()

    @add_verbose_name(u'Сезонов')
    def get_season_count(self):
        filter = {'grandprixs__heats__results__%s' % self._meta.module_name: self}
        return Season.objects.filter(**filter).count()

    @add_verbose_name(u'Побед')
    def get_win_count(self):
        return self.results.filter(heat__type=Heat.RACE, position=1).count()

    @add_verbose_name(u'Подиумов')
    def get_podium_count(self):
        return self.results.filter(heat__type=Heat.RACE, position__gte=1, position__lte=3).count()

    @add_verbose_name(u'Очков')
    def get_points_count(self):
        total = 0
        for result in self.results.filter(heat__type=Heat.RACE):
            total += result.get_points_count()
        return total

    @add_verbose_name(u'Поул-позишн')
    def get_poles_count(self):
        return self.results.filter(heat__type=Heat.QUAL, position=1).count()

    @add_verbose_name(u'Быстрейших кругов')
    def get_bestlap_count(self):
        filter = {'result__%s' % self._meta.module_name: self}
        return BestLap.objects.filter(**filter).count()

    @add_verbose_name(u'Сходов')
    def get_fail_count(self):
        return self.results.exclude(fail='').count()


def get_last(query_set):
    ordering = []
    for order in query_set.model._meta.ordering:
        ordering.insert(0, order)
    return query_set.order_by(*ordering)[0]


def time_to_str(time):
    millisecond = int((time % 1) * 1000)
    time = int(time)
    second = time % 60
    time = time / 60
    minute = time % 60
    hour = time / 60
    result = ''
    if hour:
        result += '%02d:' % hour
    if minute:
        result += '%02d:' % minute
    result += '%02d.%03d' % (second, millisecond)
    return result


class Country(models.Model):
    class Meta:
        ordering = ['name']
        verbose_name = u'Страна'
        verbose_name_plural = u'Страны'
    name = models.CharField(verbose_name=u'Название', max_length=100)
    photo = models.ImageField(verbose_name=u'Флаг', upload_to='upload/country/photo', null=True, blank=True)

    def __unicode__(self):
        return '%s' % self.name

class Racer(StatModel):
    class Meta:
        ordering = ['first_name', 'family_name', ]
        verbose_name = u'Гонщик'
        verbose_name_plural = u'Гонщики'
        unique_together = (
            ('family_name', 'first_name',),
        )
    first_name = models.CharField(verbose_name=u'Имя', max_length=100)
    family_name = models.CharField(verbose_name=u'Фамилия', max_length=100)
    slug = models.SlugField(verbose_name=u'Слаг', max_length=100, unique=True)
    country = models.ForeignKey(Country, verbose_name=u'Страна', related_name='racers', null=True, blank=True)
    birthday = models.DateField(verbose_name=u'Дата рождения')
    comment = models.CharField(verbose_name=u'Комментарий', max_length=200, default='', blank=True)
    photo = models.ImageField(verbose_name=u'Фото', upload_to='upload/racer/photo', null=True, blank=True)

    @add_verbose_name(u'Возраст')
    def get_age(self):
        today = datetime.date.today()
        delta = today.year - self.birthday.year - 1
        if datetime.date(self.birthday.year, today.month, today.day) > self.birthday:
            delta += 1
        return  delta

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

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.family_name)


class Engine(StatModel):
    class Meta:
        ordering = ['name']
        verbose_name = u'Двигатель'
        verbose_name_plural = u'Двигатели'
    name = models.CharField(verbose_name=u'Название', max_length=100)
    slug = models.SlugField(verbose_name=u'Слаг', max_length=100, unique=True)

    def __unicode__(self):
        return u'%s' % self.name


class Tyre(StatModel):
    class Meta:
        ordering = ['name']
        verbose_name = u'Шина'
        verbose_name_plural = u'Шины'
    name = models.CharField(verbose_name=u'Название', max_length=100)
    slug = models.SlugField(verbose_name=u'Слаг', max_length=100, unique=True)

    def __unicode__(self):
        return u'%s' % self.name


class Team(StatModel):
    class Meta:
        ordering = ['name']
        verbose_name = u'Команда'
        verbose_name_plural = u'Команды'
    name = models.CharField(verbose_name=u'Название', max_length=100)
    slug = models.SlugField(verbose_name=u'Слаг', max_length=100, unique=True)

    def __unicode__(self):
        return '%s' % self.name

class Season(VerboseModel):
    class Meta:
        ordering = ['year']
        verbose_name = u'Сезон'
        verbose_name_plural = u'Сезоны'
    year = models.IntegerField(verbose_name=u'Год')

    def __unicode__(self):
        return u'%d' % self.year

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


class GrandPrix(VerboseModel):
    class Meta:
        ordering = ['season', 'index']
        verbose_name = u'Гран-при'
        verbose_name_plural = u'Гран-при'
        unique_together = (
            ('season', 'name',),
        )

    index = models.IntegerField(verbose_name=u'Индекс', null=True)
    season = models.ForeignKey(Season, verbose_name=u'Сезон', related_name='grandprixs')
    name = models.CharField(verbose_name=u'Наименование', max_length=100)
    slug = models.SlugField(verbose_name=u'Слаг', max_length=100, unique=True)

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
    TYPE = (
        (FP1, u'Тренировачные заезды 1',),
        (FP2, u'Тренировачные заезды 2',),
        (FP3, u'Тренировачные заезды 3',),
        (QUAL, u'Квалификация',),
        (WARM, u'Warm-up',),
        (RACE, u'Гонка',),
    )
    grandprix = models.ForeignKey(GrandPrix, verbose_name=u'Гран-при', related_name='heats')
    type = models.CharField(verbose_name=u'Тип', max_length=1, choices=TYPE)
    date = models.DateTimeField(verbose_name=u'Дата', default=datetime.datetime.now)
    time = models.DecimalField(verbose_name=u'Время победителя', max_digits=8, decimal_places=3)
    laps = models.IntegerField(verbose_name=u'Кругов заезда')
    half_points = models.BooleanField(verbose_name=u'Делить очки пополам', default=False)
    slug = models.SlugField(verbose_name=u'Слаг', max_length=100, unique=True)

    def get_results(self):
        return self.results.filter(fail='')

    def get_fails(self):
        return self.results.exclude(fail='')

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
    position = models.IntegerField(verbose_name=u'Поз.')
    racer = models.ForeignKey(Racer, verbose_name=u'Гонщик', related_name='results')
    team = models.ForeignKey(Team, verbose_name=u'Команда', related_name='results')
    engine = models.ForeignKey(Engine, verbose_name=u'Двигатель', related_name='results')
    tyre = models.ForeignKey(Tyre, verbose_name=u'Шины', related_name='results')
    delta = models.DecimalField(verbose_name=u'Отставание (время)', max_digits=8, decimal_places=3, null=True, blank=True)
    laps = models.IntegerField(verbose_name=u'Кругов заезда', null=True, blank=True)
    fail = models.CharField(verbose_name=u'Причина схода', max_length=100, default='', blank=True)
    
    def is_classified(self):
        u'Классифицируется'
        if self.laps is None:
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
            return '+%d %s' % (self.laps, u'круга')
        else:
            return '+%s' % time_to_str(self.delta)

    def get_points_count(self):
        try:
            value = self.heat.grandprix.season.points.get(position=self.position).point
            if self.heat.half_points:
                value /= 2
            return value
        except models.ObjectDoesNotExist:
            return 0

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

    def __unicode__(self):
        return u''
