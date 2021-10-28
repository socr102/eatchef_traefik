import os
import sys


def up_traefik(pods=1):
    os.system(f'docker-compose -f services/traefik.yml up -d')


def stop_traefik():
    os.system(f'docker-compose -f services/traefik.yml stop')


if __name__ == "__main__":
    args = sys.argv
    # args[0] = current file
    # args[1] = function name
    # args[2:] = function args : (*unpacked)
    globals()[args[1]](*args[2:])
