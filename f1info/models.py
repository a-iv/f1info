# -*- coding: utf-8 -*-

import datetime
from django.db import models

class VerboseItem(object):
    def __init__(self, object):
        self._object = object

    def __getattribute__(self, name):
        if name.startswith('_'):
            return super(VerboseItem, self).__getattribute__(name)
        if name == 'self':
            return self._object._meta.verbose_name
        try:
            return self._object._meta.get_field(name).verbose_name
        except models.FieldDoesNotExist:
            object = getattr(self._object, name)
            try:
                return object.verbose_name
            except AttributeError:
                if object.__doc__:
                    return object.__doc__
                raise

class VerboseModel(models.Model):
    class Meta:
        abstract = True

    def __getattribute__(self, name):
        if name == 'get_verbose_name':
            return VerboseItem(self)
        return super(VerboseModel, self).__getattribute__(name)


class StatModel(VerboseModel):
    class Meta:
        abstract = True

    def get_race_count(self):
        u'Гонок'
        return self.results.filter(heat__type=Heat.RACE).count()

    def get_grand_prix_count(self):
        u'Гран-при'
        filter = {'heats__results__%s' % self._meta.module_name: self}
        return GrandPrix.objects.filter(**filter).count()

    def get_season_count(self):
        u'Сезонов'
        filter = {'grandprixs__heats__results__%s' % self._meta.module_name: self}
        return Season.objects.filter(**filter).count()

    def get_win_count(self):
        u'Побед'
        return self.results.filter(heat__type=Heat.RACE, position=1).count()

    def get_podium_count(self):
        u'Подиумов'
        return self.results.filter(heat__type=Heat.RACE, position__lte=3).count()

    def get_points_count(self):
        u'Очков'
        total = 0
        for result in self.results.all():
            total += result.get_points_count()
        return total

    def get_poles_count(self):
        u'Поул-позишн'

    def get_bestlap_count(self):
        u'Быстрейщих кругов'
        filter = {'result__%s' % self._meta.module_name: self}
        return BestLap.objects.filter(**filter).count()

    def get_fail_count(self):
        u'Сходов'
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


class Racer(StatModel):
    class Meta:
        ordering = ['family_name', 'first_name', ]
        verbose_name = u'Гонщик'
        verbose_name_plural = u'Гонщики'
        unique_together = (
            ('family_name', 'first_name',),
        )
    family_name = models.CharField(verbose_name=u'Фамилия', max_length=100)
    first_name = models.CharField(verbose_name=u'Имя', max_length=100)
    nationality = models.CharField(verbose_name=u'Национальность', max_length=100)
    birthday = models.DateField(verbose_name=u'Дата рождения')
    comment = models.CharField(verbose_name=u'Комментарий', max_length=200, default='')

    def get_last_team(self):
        u'Последняя команда'
        return get_last(self.results).team

    def get_last_tyre(self):
        u'Последние шины'
        return get_last(self.results).tyre

    def get_last_engine(self):
        u'Последний двигатель'
        return get_last(self.results).engine

    def __unicode__(self):
        return u'%s %s' % (self.family_name, self.first_name)


class Engine(StatModel):
    class Meta:
        ordering = ['name']
        verbose_name = u'Двигатель'
        verbose_name_plural = u'Двигатели'
    name = models.CharField(verbose_name=u'Название', max_length=100)

    def __unicode__(self):
        return u'%s' % self.name


class Tyre(StatModel):
    class Meta:
        ordering = ['name']
        verbose_name = u'Шина'
        verbose_name_plural = u'Шины'
    name = models.CharField(verbose_name=u'Название', max_length=100)

    def __unicode__(self):
        return u'%s' % self.name


class Team(StatModel):
    class Meta:
        ordering = ['name']
        verbose_name = u'Команда'
        verbose_name_plural = u'Команды'
    name = models.CharField(verbose_name=u'Название', max_length=100)

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
#        ordering = ['heats__date']
        verbose_name = u'Гран-при'
        verbose_name_plural = u'Гран-при'
        unique_together = (
            ('season', 'name',),
        )

    season = models.ForeignKey(Season, verbose_name=u'Сезон', related_name='grandprixs')
    name = models.CharField(verbose_name=u'Наименование', max_length=100)

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
    RACE = 'R'
    TYPE = (
        ('1', u'Тренировачные заезды 1',),
        ('2', u'Тренировачные заезды 2',),
        ('Q', u'Квалификация',),
        ('3', u'Тренировачные заезды 3',),
        ('W', u'Warm-up',),
        (RACE, u'Гонка',),
    )
    grandprix = models.ForeignKey(GrandPrix, verbose_name=u'Гран-при', related_name='heats')
    type = models.CharField(verbose_name=u'Тип', max_length=1, choices=TYPE)
    date = models.DateField(verbose_name=u'Дата', default=datetime.date.today)
    time = models.DecimalField(verbose_name=u'Время заезда', max_digits=8, decimal_places=3)
    laps = models.IntegerField(verbose_name=u'Кругов заезда')
    half_points = models.BooleanField(verbose_name=u'Делить очки пополам', default=False)

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
    position = models.IntegerField(verbose_name=u'Место')
    racer = models.ForeignKey(Racer, verbose_name=u'Гонщик', related_name='results')
    team = models.ForeignKey(Team, verbose_name=u'Команда', related_name='results')
    engine = models.ForeignKey(Engine, verbose_name=u'Двигатель', related_name='results')
    tyre = models.ForeignKey(Tyre, verbose_name=u'Шины', related_name='results')
    delta = models.DecimalField(verbose_name=u'Отставание (время)', max_digits=8, decimal_places=3, null=True, blank=True)
    laps = models.IntegerField(verbose_name=u'Кругов заезда', null=True, blank=True)
    fail = models.CharField(verbose_name=u'Причина схода', max_length=100, default='', blank=True)

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
