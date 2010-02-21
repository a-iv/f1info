from django.db.models.signals import pre_save
from trustedhtml import pretty
from trustedhtml.signals import rule_done
from trustedhtml.classes import Uri
from modelurl.utils import ReplaceByView
from pages.models import Content
from easy_news.models import News

def content_save(sender, instance, **kwargs):
    if instance.type == 'main_content':
        instance.body = pretty.validate(instance.body)

pre_save.connect(content_save, sender=Content)

def news_save(sender, instance, **kwargs):
    instance.short = pretty.validate(instance.short)
    instance.text = pretty.validate(instance.text)

pre_save.connect(news_save, sender=News)

def url_done(sender, rule, value, source, **kwargs):
    return ReplaceByView(silent=True).url(value)

rule_done.connect(url_done, sender=Uri)
