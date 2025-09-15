#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys

FAILED_TO_IMPORT_DJANGO_MODULE = (
    "Couldn't import Django. Are you sure it's installed and "
    "available on your PYTHONPATH environment variable? Did you "
    "forget to activate a virtual environment?",
)


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "effect_edc.settings.debug")
    try:
        from django.core.management import execute_from_command_line  # noqa: PLC0415
    except ImportError as exc:
        raise ImportError(FAILED_TO_IMPORT_DJANGO_MODULE) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
