FROM nvcr.io/nvidia/tritonserver:21.03-py3
ARG DEBIAN_FRONTEND=noninteractive
WORKDIR /opt/tritonserver
USER root

ENTRYPOINT ["/opt/tritonserver/nvidia_entrypoint.sh"]