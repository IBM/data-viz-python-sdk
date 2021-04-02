#===============================================================
# IBM Confidential
#
# OCO Source Materials
#
# Copyright IBM Corp. 2018,2019
#
# The source code for this program is not published or otherwise
# divested of its trade secrets, irrespective of what has been
# deposited with the U.S. Copyright Office.
#===============================================================

ARG BASE_IMAGE
FROM $BASE_IMAGE
ARG S3FS_VERSION=v1.79
ARG PROJECT_VERSION
ENV VERSION=${PROJECT_VERSION}
ENV STAGE_SCRIPT=${STAGE_SCRIPT}

ENV SOURCE_DIRECTORY=/src/

ENV SOURCE_DIRECTORY_AMHAIRC=/src/amhairc
ENV INSTALL_DIRECTORY_AMHAIRC=/opt/src/amhairc
ENV INSTALL_DIRECTORY=/opt/src

ENV IMAGE_OUTPUT_DIRECTORY=/opt/output
ENV TMP_DIRECTORY=/opt/tmp

RUN mkdir -p $INSTALL_DIRECTORY_AMHAIRC

ADD $SOURCE_DIRECTORY_AMHAIRC $INSTALL_DIRECTORY_AMHAIRC
ADD src/run.sh /opt/run.sh
ADD src/amhairc.py /opt/amhairc.py
ADD src/api.py /opt/api.py

RUN ["chmod", "+x", "/opt/run.sh"]
RUN ["chmod", "+x", "/opt/amhairc.py"]
RUN ["chmod", "+x", "/opt/api.py"]

WORKDIR /opt
CMD ["/opt/amhairc.py"]
ENTRYPOINT ["python3"]

