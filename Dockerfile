FROM ubuntu:latest

RUN apt-get update && apt-get install -y python-pip python-dev nmap
COPY src /network-scanner
RUN pip install -r /network-scanner/requirements.txt
WORKDIR /network-scanner
CMD python scanner.py
