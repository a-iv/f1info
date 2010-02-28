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
        pass
#        return self.results.filter(racer__type=Heat.RACE).count()

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
        pass
#        return self.results.filter(racer__type=Heat.RACE).count()

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
        pass
#        return self.results.filter(racer__type=Heat.RACE).count()

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
