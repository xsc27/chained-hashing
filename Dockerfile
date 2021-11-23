ARG PY_VER=3
ARG IMG_VARIANT=-alpine

FROM python:${PY_VER}${IMG_VARIANT} as build
COPY . /tmp/app/
SHELL ["/bin/ash", "-euxc"]
RUN \
    apk add gcc libc-dev ;\
    pip3 install --compile --target /opt/req --requirement /tmp/app/requirements/lock.txt ;\
    pip3 install --compile --target /opt/app --no-dependencies \
      "$(find /tmp/app -type f -name \*.whl -print0 | xargs -r -0 ls -1 -t | head -1)"

FROM python:${PY_VER}${IMG_VARIANT}
ENV PYTHONPATH=/opt/app/
COPY --from=build /opt/req/ /opt/app/
COPY --from=build /opt/app/ /opt/app/
SHELL ["/bin/ash", "-euxc"]
RUN find /opt/app/bin/ -maxdepth 1 -type f -executable -exec ln -sv "{}" /usr/local/bin/ \;

USER guest
ENTRYPOINT ["chained_hashing"]
CMD ["--help"]
