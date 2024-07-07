FROM bitnami/minio:latest

# give admin permission
USER root

# Expose the default MinIO port
EXPOSE 9000
EXPOSE 9001

# Set the default environment variables
ENV MINIO_ROOT_USER=admin
ENV MINIO_ROOT_PASSWORD=password
ENV MINIO_DEFAULT_BUCKETS=files

# Set the data directory
VOLUME ["/data"]

# Set the work directory
CMD ["minio", "server", "/data", "--console-address", ":9001"]


# docker build -t minio .
# docker run -d --name minio -p 9000:9000 -p 9001:9001 minio