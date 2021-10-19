# SharpNet

Sharpnet is a service that controls NGINX allowing for painless and automatic control of your websites and webapps with automatic SSL certification.

![Example of Sharpnet Logs](https://files.mcaq.me/vi1u.png)

## Configuration

Sharpnet is configured to be installed using a docker-compose file:
Click [Here](https://github.com/Sharpz7/sharpnet/blob/master/docker-compose.yml) to see an example

## Enviroment Options

Note that all of these are required

| Key | Type | Description |
| --- | --- | --- |
| `HTTP_PORT` | int | Port for http connections. |
| `HTTPS_PORT` | int | Port for https connections. |
| `DEV` | bool [TRUE?FALSE] | For debugging. |
| `NETWORK` | str | The docker network that sharpnet will listen to for new connections. |
| `MAILPASS` | str | The google one-time password for mail services |
| `SENDER_EMAIL` | str | Must be a gmail email |
| `RECEIVER_EMAIL` | str | The email you want on the certificates and to receive emails to |
| `DOMAIN` | str | The domain all certificates will be linked to |

## Installation

Download the docker-compose file, set your env vars and run the file!

For seeing how to configue your websites and apps for sharpnet, please check my other public repositories with web-apps and websites to see examples.

## Maintainers

- [Adam McArthur](https://adam.mcaq.me)
