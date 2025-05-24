# Set container size limit to 10GB (10240MB) to accommodate Kali Linux installation
FROM kalilinux/kali-rolling:latest
WORKDIR /workdir
RUN apt update && apt -y install kali-linux-headless
RUN apt-get update
RUN apt-get install -y openvpn
COPY lab.ovpn /workdir/lab.ovpn
COPY setup.sh /workdir/setup.sh
RUN chmod +x /workdir/setup.sh
RUN /workdir/setup.sh