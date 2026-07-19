FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
      ca-certificates dumb-init fonts-liberation gosu socat wget xauth xvfb \
  && wget -q -O /tmp/chrome.deb \
      https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
  && apt-get install -y /tmp/chrome.deb \
  && rm -rf /var/lib/apt/lists/* /tmp/chrome.deb \
  && useradd --create-home --shell /bin/sh chrome \
  && install -d -o chrome -g chrome /data/chrome-profile

COPY start-chrome.sh run-xvfb-chrome.sh /usr/local/bin/
RUN chmod 0755 /usr/local/bin/start-chrome.sh /usr/local/bin/run-xvfb-chrome.sh

EXPOSE 9222
VOLUME ["/data/chrome-profile"]
ENTRYPOINT ["dumb-init", "--", "/usr/local/bin/start-chrome.sh"]
