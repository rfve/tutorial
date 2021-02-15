# -*- coding: utf-8 -*-
""" An extension to export items to a Telegram chat. """
import logging

from telegram import Bot
from scrapy import signals
import importlib
from scrapy.exceptions import NotConfigured


logger = logging.getLogger(__name__)


class TGItemExporterExtension(object):
    def __init__(self, crawler):
        self._crawler = crawler
        settings = crawler.settings
        if not settings.getbool('TELEGRAM_EXPORT_ENABLED', False):
            raise NotConfigured
        logger.debug('TG export extension is enabled')

        self._tg_api_key = settings.get('818802616:AAE2jGAQUfdndClq0UoNVjL5TNAYAWSEAIQ')
        self._tg_chat_id = settings.get('1001280329146')

        self._tg_bot = None
        preprocessor_func_name = settings.get('TELEGRAM_MESSAGE_PREPROCESSOR')
        if preprocessor_func_name:
            mod_name, func_name = preprocessor_func_name.rsplit('.', 1)
            mod = importlib.import_module(mod_name)
            self._item_preprocessor = getattr(mod, func_name)
        else:
            self._item_preprocessor = self.default_preprocessor
        crawler.signals.connect(self.spider_opened, signals.spider_opened)
        crawler.signals.connect(self.process_item_scraped,
                                signals.item_scraped)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def spider_opened(self, spider):
        self._tg_bot = Bot(token=self._tg_api_key)

    def process_item_scraped(self, item, response, spider):
        item_text, send_item = self._item_preprocessor(item, response)
        if send_item:
            self._tg_bot.send_message(chat_id=self._tg_chat_id,
                                      text=item_text,
                                      parse_mode="Markdown")
            self._crawler.stats.inc_value('telegram/sent')
        else:
            self._crawler.stats.inc_value('telegram/skipped')

    def default_preprocessor(self, item, response):
        return str(item), True