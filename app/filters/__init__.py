from loguru import logger

from app.loader import dp

from .HasAccess import HasAccess

if __name__ == "app.filters":
    text_messages = [
        dp.message_handlers,
        dp.edited_message_handlers,
        dp.channel_post_handlers,
        dp.edited_channel_post_handlers,
    ]

    dp.bind_filter(HasAccess, event_handlers=text_messages)

    logger.info('Filters are successfully configured')
