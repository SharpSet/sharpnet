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

if os.environ.get("DEV") == "TRUE":
    NETWORK = "sharpnet_testing"
    DEV = True

else:
    NETWORK = "sharpnet"
    DEV = False

CERTBOT_COMMAND = "certbot --nginx --email adam@mcaq.me --cert-name mcadesigns.co.uk --agree-tos --redirect --noninteractive --expand"
