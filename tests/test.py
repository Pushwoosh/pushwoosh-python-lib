"""
Use <unit> to run only unit tests.
Use <integration> to run only integration tests.

Before start integration test set PW_TOKEN, PW_APP_CODE and PW_APP_GROUP_CODE in your environment variables
"""


if __name__ == '__main__':
    import argparse
    import os
    import sys

    from nose.core import run

    base_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(base_dir)

    argv = [__file__, '-vv']
    parser = argparse.ArgumentParser(description='Run tests.')
    known_args, remaining_args = parser.parse_known_args()
    argv = argv + remaining_args
    run(argv=argv)