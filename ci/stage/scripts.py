import os
import sys

ENV_FILE = '.traefik.env'


def up_traefik(pods=1):
    os.system(f'docker-compose -f services/traefik.yml up -d')


def stop_traefik():
    os.system(f'docker-compose -f services/traefik.yml stop')


def check_network():
    os.system(f'docker network create --internal=false --attachable proxy')
    return


def create_env():
    text = f'DOMAIN={os.environ.get("DOMAIN", "")}\n' \
           f'NETWORK=proxy\n'
    with open(ENV_FILE, 'w+' if os.path.exists(ENV_FILE) else 'w') as file:
        file.write(text)
    return


def load_env():
    if os.path.exists(ENV_FILE) is False:
        print(f'{ENV_FILE} DOES NOT exist!!! Please create this file.')
        return
    with open(ENV_FILE, 'r') as fh:
        vars_dict = dict()
        for line in fh.readlines():
            if not line.startswith('#'):
                line_dict = (tuple(line.rstrip("\n").split('=', 1)))
                if len(line_dict) == 2:
                    [env, value] = line_dict
                    vars_dict[env] = value
    os.environ.update(vars_dict)


if __name__ == "__main__":
    load_env()
    args = sys.argv
    # args[0] = current file
    # args[1] = function name
    # args[2:] = function args : (*unpacked)
    globals()[args[1]](*args[2:])
