# TRAEFIC

Traefik — is a reverse proxy-server, simplifying work with the microservices or simply containers of your app.

It is used to relay requests from the external network to any servers/services of the internal network (for example, web servers, databases or file storages) and allows:

1) to ensure the concealment of the structure of the internal network and details about the services located in it;

2) to perform load balancing between instances of the same service or servers with the same tasks;

3) to provide an encrypted (HTTPS) connection between the client and any service, in this case an SSL session is created between the client and the proxy, and an unencrypted HTTP connection is established between the proxy and the service in the internal network;

4) organize access control to services (client authentication), as well as set up a firewall.

### WHAT DOES TRAEFIC DO

See traefik.yml:

1) Exposes ports 80 and 443 to the internet

Two entrypoints are used for this (see [https://doc.traefik.io/traefik/routing/entrypoints/](https://doc.traefik.io/traefik/routing/entrypoints/) )
```
- --entryPoints.web.address=:80
- --entryPoints.websecure.address=:443
```
with redirect from 80 to 443 port:
```
- --entrypoints.web.http.redirections.entrypoint.to=websecure
- --entrypoints.web.http.redirections.entrypoint.scheme=https
- --entrypoints.web.http.redirections.entrypoint.permanent=false
```

2) Options
```
- --providers.docker=true
- --providers.docker.exposedbydefault=false
- --providers.docker.endpoint=unix:///var/run/docker.sock
- --providers.docker.swarmMode=false
```
enable docker support.

Traefic will monitor for new containers but won't expose their open ports automatically to the network.

For each service available to the Internet the following routing configuration should be created using labels.
More info: [https://doc.traefik.io/traefik/providers/docker/#routing-configuration-with-labels](https://doc.traefik.io/traefik/providers/docker/#routing-configuration-with-labels)

This example is from /ci/stage/services/main_api.yml

```
labels:
  - traefik.enable=true
  - traefik.docker.network=proxy
  - traefik.http.middlewares.limit.buffering.maxRequestBodyBytes=200000000
  - traefik.http.middlewares.limit.buffering.memRequestBodyBytes=200000000
  - traefik.http.routers.main_api.entrypoints=websecure
  - traefik.http.routers.main_api.rule=Host(`${API_DOMAIN}`)
  - traefik.http.routers.main_api.tls=true
  - traefik.http.routers.main_api.tls.certresolver=letsencrypt
  - traefik.http.routers.main_api.service=main_api_service
  - traefik.http.services.main_api_service.loadbalancer.server.port=80
```

3) Automatically creates Let's Encrypt certificates for the DOMAIN provided

```
- traefik.http.routers.wildcard-certs.tls.domains[0].main=${DOMAIN}
- traefik.http.routers.wildcard-certs.tls.domains[0].sans=*.${DOMAIN}

# letsencrypt
- --certificatesresolvers.letsencrypt.acme.email=alert@goodbit.dev
- --certificatesresolvers.letsencrypt.acme.storage=/letsencrypt/acme.json

# used during the challenge
- --certificatesresolvers.letsencrypt.acme.httpchallenge.entrypoint=web
```

See about HTTP challenge setup for Let's Encrypt: [https://doc.traefik.io/traefik/user-guides/docker-compose/acme-http/](https://doc.traefik.io/traefik/user-guides/docker-compose/acme-http/)

4) Provides a dashboard available by the url: [https://traefik.eatchefs.goodbit.dev/](https://traefik.eatchefs.goodbit.dev/)  (username: user password: palad900)
```
- --api.dashboard=true

- traefik.http.routers.dashboard.middlewares=auth
- traefik.http.middlewares.auth.basicauth.users=user:$$2y$$05$$MZ29B0k0q7DhDzCoQtAJXuknGjd0/6/AoSnw2KzmtYdgzkQTeDsVG

- traefik.http.routers.dashboard.rule=Host(`traefik.${DOMAIN}`)
- traefik.http.routers.dashboard.entrypoints=websecure
- traefik.http.routers.dashboard.service=api@internal
- traefik.http.routers.dashboard.tls=true
- traefik.http.routers.dashboard.tls.certresolver=letsencrypt
```

All the routes from containers are here [https://traefik.eatchefs.goodbit.dev/dashboard/#/http/routers](https://traefik.eatchefs.goodbit.dev/dashboard/#/http/routers)

5) This option
```
- --pilot.token=0b15cdd6-1726-438e-8bea-28d82fe020db
```
is for possible connection to Traefik Pilot for monitoring: [https://doc.traefik.io/traefik-pilot/](https://doc.traefik.io/traefik-pilot/)

