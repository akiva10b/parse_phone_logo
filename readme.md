# Logo and Phone Parser

Logo and Phone Parser is a Python Script that prints the urls and logo link

## Installation

Build docker image

```bash
 docker build --tag app .
```

Or install locally using pip
```bash
 pip3 install -r requirements.txt
```
## Usage

In the base folder there is a file called `urls.txt`, when running the script directly you can put in any file path you wish like so:

```bash
 docker run app /Users/akiva/PycharmProjects/urls.txt
```

If you want to run on Docker, alter the file `urls.txt` and build the docker.
To run the script on docker, run the following command:
```bash
 docker run app urls.txt
```
