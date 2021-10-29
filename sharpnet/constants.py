import os
from pathlib import Path

p = Path("/sharpnet/files/")
etc_nginx = Path("/etc/nginx/")
letsencrypt = Path("/etc/letsencrypt")

SITE_CONF = (etc_nginx / "conf.d" / "site.conf").as_posix()
DEFAULT_SITE_CONF = (etc_nginx / "conf.d" / "default.conf").as_posix()
NGINX_CONF = (etc_nginx / "nginx.conf").as_posix()
DUMMY_CONF = (etc_nginx / "dummy.conf").as_posix()
TEST_SITE_CONF = (etc_nginx / "conf.d" / "test.conf").as_posix()

OPTIONS_SSL_NGINX_CONF = (letsencrypt / "options-ssl-nginx.conf").as_posix()

DEFAULT_CONF = (p / "default.conf").as_posix()
SECURITY_CONF = (p / "security.conf").as_posix()
REDIRECT_CONF = (p / "redirect.conf").as_posix()
TEST_CONF = (p / "test.conf").as_posix()
HTMLFILE = (p / "index.html").as_posix()

SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL")
DOMAIN = os.environ.get("DOMAIN")

# These must all be set to start-up

if None in [SENDER_EMAIL, RECEIVER_EMAIL, DOMAIN]:
    print("FAILED: one of the domain/email vars is not set!")
    quit()

if os.environ.get("DEV") == "TRUE":
    NETWORK = "sharpnet_testing"
    DEV = True

else:
    NETWORK = "sharpnet"
    DEV = False

CERTBOT_COMMAND = f"certbot --nginx --email {RECEIVER_EMAIL} --cert-name {DOMAIN} --agree-tos --redirect --noninteractive --expand"
