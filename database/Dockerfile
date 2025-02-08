FROM postgres:16.1

ADD initdb.sql /docker-entrypoint-initdb.d/
RUN chown postgres:postgres /docker-entrypoint-initdb.d/initdb.sql
USER postgres