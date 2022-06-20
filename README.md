[![CircleCI](https://circleci.com/gh/SharpSet/sharpnet/tree/master.svg?style=svg)](https://circleci.com/gh/SharpSet/sharpnet/tree/master)

![Sharpnet](https://files.mcaq.me/39387.png)
# Auto HTTPS and config with NGINX

Sharpnet is a service that controls NGINX allowing for painless and automatic control of your websites and webapps with automatic SSL certification.

![Example of Sharpnet (Diagram)](https://files.mcaq.me/c07c2.png)

## Configuration

Sharpnet is configured to be installed using a docker-compose file:
Click [Here](https://github.com/SharpSet/sharpnet/blob/master/docker-compose.yml) to see an example

## Enviroment Options

Note that all of these are required

| Key | Type | Description |
| --- | --- | --- |
| `HTTP_PORT` | int | Port for http connections. |
| `HTTPS_PORT` | int | Port for https connections. |
| `DEV` | bool [TRUE?FALSE] | For debugging. |
| `DEBUG_LOGGING` | bool [TRUE?FALSE] | For debugging. |
| `NETWORK` | str | The docker network that sharpnet will listen to for new connections. |
| `MAILPASS` | str | The google one-time password for mail services |
| `SENDER_EMAIL` | str | Must be a gmail email |
| `RECEIVER_EMAIL` | str | The email you want on the certificates and to receive emails to |
| `DOMAIN` | str | The domain all certificates will be linked to |

## SharpCD Install

- Make sure [SharpCD](https://github.com/Sharpz7/sharpcd) has been installed.

- Ensure the enviromental variables have been set in an enviromental variable (.env) file

- Run the following command to install the registry:

```bash
sharpcd --remotefile https://raw.githubusercontent.com/Sharpz7/sharpnet/master/.sharpcd/sharpcd.yml
```

## Maintainers

- [Adam McArthur](https://mcaq.me)
