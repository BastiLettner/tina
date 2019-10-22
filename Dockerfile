FROM python:3-slim

LABEL maintainer="sebastian.lettner24@gmail.com"
LABEL version="1.0"
LABEL description="Background Processing Server"

ARG user=sebastian
ARG group=sebastian
ARG uid=1001
ARG gid=1001

# Add user
RUN addgroup --gid ${gid} ${group} && \
    adduser --home /home/${user} --uid ${uid} --ingroup ${group} --shell /bin/bash ${user}
RUN apt-get update


WORKDIR /home/${user}/app
RUN chown -R ${user} /home/${user}
RUN pip install --upgrade pip
USER ${user}

# copy source code and install deps
COPY . .
RUN pip install --user -e . --no-warn-script-location

CMD ["/bin/bash"]
