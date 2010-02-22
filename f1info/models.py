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

    def get_heat_count(self):
        u"""Гонок"""
        pass

    def get_season_count(self):
        u"""Сезонов"""
        pass

    def get_win_count(self):
        u"""Побед"""
        pass

    def get_stage_count(self):
        u"""Подиумов"""
        pass

    def get_score_count(self):
        u"""Очков"""
        pass

    def get_qualification_count(self):
        u"""Побед в квалификации"""
        pass

    def get_best_count(self):
        u"""Быстрейщий кругов"""
        pass

    def get_descent_count(self):
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

    def __unicode__(self):
        return u'%s' % self.name


class Team(models.Model):
    class Meta:
        ordering = ['name']
        verbose_name = u'Команда'
        verbose_name_plural = u'Команды'
    name = models.CharField(verbose_name=u'Название', max_length=100)

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

class Score(models.Model):
    class Meta:
        ordering = ['place']
        verbose_name = u'Очки'
        verbose_name_plural = u'Очки'
        unique_together = (
            ('season', 'place',),
        )
    season = models.ForeignKey(Season, verbose_name=u'Сезон', related_name='seasons')
    place = models.IntegerField(verbose_name=u'Место')
    score = models.IntegerField(verbose_name=u'Очки')

    def __unicode__(self):
        return u''

class Heat(models.Model):
    class Meta:
        ordering = ['date']
        verbose_name = u'Заезд'
        verbose_name_plural = u'Заезды'
        unique_together = (
            ('season', 'type', 'name',),
        )
    TYPE = (
        ('1', u'Тренировачные заезды 1',),
        ('2', u'Тренировачные заезды 2',),
        ('3', u'Тренировачные заезды 3',),
        ('Q', u'Квалификация',),
        ('W', u'Warm-up',),
        ('R', u'Гонка',),
    )
    season = models.ForeignKey(Season, verbose_name=u'Сезон', related_name='heats')
    name = models.CharField(verbose_name=u'Гран-при', max_length=100)
    type = models.CharField(verbose_name=u'Тип', max_length=1, choices=TYPE)
    date = models.DateField(verbose_name=u'Дата', default=datetime.date.today)
    time = models.TimeField(verbose_name=u'Время заезда')
    round = models.IntegerField(verbose_name=u'Кругов заезда')

    def __unicode__(self):
        return u'%s %s' % (self.season, self.name)

class Result(models.Model):
    class Meta:
        ordering = ['delta']
        verbose_name = u'Результат'
        verbose_name_plural = u'Результаты'
        unique_together = (
            ('racer', 'heat',),
        )
    racer = models.ForeignKey(Racer, verbose_name=u'Гонщик', related_name='results')
    heat = models.ForeignKey(Heat, verbose_name=u'Заезд', related_name='results')
    delta = models.FloatField(verbose_name=u'Отставание (время)', null=True, blank=True)
    round = models.IntegerField(verbose_name=u'Отставание (кругов)', null=True, blank=True)
    fail = models.CharField(verbose_name=u'Причина схода', max_length=100, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.racer

class BestRound(models.Model):
    class Meta:
        ordering = ['heat', 'result', ]
        verbose_name = u'Лучший круг'
        verbose_name_plural = u'Лучшие круги'
        unique_together = (
            ('heat', 'result',),
        )
    heat = models.ForeignKey(Heat, verbose_name=u'Заезд', related_name='bests')
    result = models.ForeignKey(Result, verbose_name=u'Результат', related_name='bests')
    round = models.IntegerField(verbose_name=u'Круг')
    time = models.TimeField(verbose_name=u'Время круга')

    def __unicode__(self):
        return u''
