import logging
import sys


def config_logging(level=logging.INFO):

    # When run by 'uvicorn ...', a root handler is already
    # configured and the basicConfig below does nothing.
    # To get the desired formatting:
    logging.getLogger().handlers.clear()

    # 'uvicorn --log-config' is broken so we configure in the app.
    #   https://github.com/encode/uvicorn/issues/511
    stdout_handler = logging.StreamHandler(sys.stdout)
    handlers = [stdout_handler]

    logging.basicConfig(
        # match gunicorn format
        format='%(asctime)s %(process)d [%(name)s] {%(filename)s:%(lineno)d} %(levelname)s %(message)s',
        datefmt='[%Y-%m-%d %H:%M:%S %z]',
        level=level,
        handlers=handlers
    )

    # When run by 'gunicorn -k uvicorn.workers.UvicornWorker ...',
    # These loggers are already configured and propogating.
    # So we have double logging with a root logger.
    # (And setting propagate = False hurts the other usage.)
    # logging.getLogger('uvicorn.access').handlers.clear()
    # logging.getLogger('uvicorn.error').handlers.clear()
    # logging.getLogger('uvicorn.access').propagate = True
    # logging.getLogger('uvicorn.error').propagate = True
