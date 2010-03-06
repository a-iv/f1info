# -*- coding: utf-8 -*-

import datetime
from django.db import models

class Racer(models.Model):
    class Meta:
        ordering = ['family_name', 'first_name', ]
        verbose_name = u'Гонщик'
        verbose_name_plural = u'Гонщики'
        unique_together = (
            ('family_name', 'first_name',),
        )
    family_name = models.CharField(verbose_name=u'Фамилия', max_length=100)
    first_name = models.CharField(verbose_name=u'Имя', max_length=100)
    nationality = models.CharField(verbose_name=u'Начиональность', max_length=100)
    birthday = models.DateField(verbose_name=u'Дата рождения')
    comment = models.CharField(verbose_name=u'Комментарий', max_length=200, default='')

    def get_race_count(self):
        u"""Гонок"""
        return self.results.filter(racer__type=Heat.RACE).count()

    def get_grand_prix_count(self):
        u"""Гран-при"""
        return #self.results.count()

    def get_last_team(self):
        u"""Команда"""
        return #self.results.count()

    def get_season_count(self):
        u"""Сезонов"""
#        for result in self.results:
        pass

    def get_win_count(self):
        u"""Побед"""
        pass

    def get_podium_count(self):
        u"""Подиумов"""
        pass

    def get_points_count(self):
        u"""Очков"""
        pass

    def get_poles_count(self):
        u"""Поул-позишн"""
        pass

    def get_bestlap_count(self):
        u"""Быстрейщих кругов"""
        pass

    def get_fail_count(self):
        u"""Сходов"""
        pass

    def __unicode__(self):
        return u'%s %s' % (self.family_name, self.first_name)

class Engine(models.Model):
    class Meta:
        ordering = ['name']
        verbose_name = u'Двигатель'
        verbose_name_plural = u'Двигатели'
    name = models.CharField(verbose_name=u'Название', max_length=100)

    def get_race_count(self):
        u"""Гонок"""
        return self.results.filter(racer__type=Heat.RACE).count()

    def get_grand_prix_count(self):
        u"""Гран-при"""
        return #self.results.count()

    def get_season_count(self):
        u"""Сезонов"""
#        for result in self.results:
        pass

    def get_win_count(self):
        u"""Побед"""
        pass

    def get_podium_count(self):
        u"""Подиумов"""
        pass

    def get_points_count(self):
        u"""Очков"""
        pass

    def get_poles_count(self):
        u"""Поул-позишн"""
        pass

    def get_bestlap_count(self):
        u"""Быстрейщих кругов"""
        pass

    def get_fail_count(self):
        u"""Сходов"""
        pass

    def __unicode__(self):
        return u'%s' % self.name


class Tyre(models.Model):
    class Meta:
        ordering = ['name']
        verbose_name = u'Шина'
        verbose_name_plural = u'Шины'
    name = models.CharField(verbose_name=u'Название', max_length=100)

    def get_race_count(self):
        u"""Гонок"""
        return self.results.filter(racer__type=Heat.RACE).count()

    def get_grand_prix_count(self):
        u"""Гран-при"""
        return #self.results.count()

    def get_season_count(self):
        u"""Сезонов"""
#        for result in self.results:
        pass

    def get_win_count(self):
        u"""Побед"""
        pass

    def get_podium_count(self):
        u"""Подиумов"""
        pass

    def get_points_count(self):
        u"""Очков"""
        pass

    def get_poles_count(self):
        u"""Поул-позишн"""
        pass

    def get_bestlap_count(self):
        u"""Быстрейщих кругов"""
        pass

    def get_fail_count(self):
        u"""Сходов"""
        pass

    def __unicode__(self):
        return u'%s' % self.name


class Team(models.Model):
    class Meta:
        ordering = ['name']
        verbose_name = u'Команда'
        verbose_name_plural = u'Команды'
    name = models.CharField(verbose_name=u'Название', max_length=100)

    def get_race_count(self):
        u"""Гонок"""
        return self.results.filter(racer__type=Heat.RACE).count()

    def get_grand_prix_count(self):
        u"""Гран-при"""
        return #self.results.count()

    def get_season_count(self):
        u"""Сезонов"""
#        for result in self.results:
        pass

    def get_win_count(self):
        u"""Побед"""
        pass

    def get_podium_count(self):
        u"""Подиумов"""
        pass

    def get_points_count(self):
        u"""Очков"""
        pass

    def get_poles_count(self):
        u"""Поул-позишн"""
        pass

    def get_bestlap_count(self):
        u"""Быстрейщих кругов"""
        pass

    def get_fail_count(self):
        u"""Сходов"""
        pass

    def __unicode__(self):
        return '%s' % self.name

class Season(models.Model):
    class Meta:
        ordering = ['year']
        verbose_name = u'Сезон'
        verbose_name_plural = u'Сезоны'
    year = models.IntegerField(verbose_name=u'Год')

    def __unicode__(self):
        return u'%d' % self.year

class Point(models.Model):
    class Meta:
        ordering = ['place']
        verbose_name = u'Очки'
        verbose_name_plural = u'Очки'
        unique_together = (
            ('season', 'place',),
        )
    season = models.ForeignKey(Season, verbose_name=u'Сезон', related_name='seasons')
    place = models.IntegerField(verbose_name=u'Место')
    point = models.IntegerField(verbose_name=u'Очки')

    def __unicode__(self):
        return u''

class GrandPrix(models.Model):
    class Meta:
        #ordering = ['heats__data']
        verbose_name = u'Гран-при'
        verbose_name_plural = u'Гран-при'
        unique_together = (
            ('season', 'name',),
        )

    season = models.ForeignKey(Season, verbose_name=u'Сезон', related_name='grandprix')
    name = models.CharField(verbose_name=u'Наименование', max_length=100)

    def __unicode__(self):
        return u'%s' % self.name


class Heat(models.Model):
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
    round = models.IntegerField(verbose_name=u'Кругов заезда')
    half_points = models.BooleanField(verbose_name=u'Делить очки пополам', default=False)

    def __unicode__(self):
        return u'%s - %s' % (self.grandprix, self.get_type_display())

class Result(models.Model):
    class Meta:
        ordering = ['position']
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
    round = models.IntegerField(verbose_name=u'Отставание (кругов)', null=True, blank=True)
    fail = models.CharField(verbose_name=u'Причина схода', max_length=100, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.racer

class BestLap(models.Model):
    class Meta:
        ordering = ['heat', 'result', ]
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
