# Python base image
FROM python:3.10-slim-buster

# copy source code
COPY . /app
WORKDIR /app

# Copy python libraries requirements
COPY requirements.txt requirements.txt

# update linux packages
RUN apt-get update 

# Install additional linux packages in order to compile some python librarires 
RUN apt-get install -y --no-install-recommends gcc libsasl2-dev python-dev \ 
    libldap2-dev libssl-dev libsnmp-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python libraries
RUN pip install -r requirements.txt 

# Delete the additional linux packages since they are no longer needed for compiling 
RUN apt-get purge -y --auto-remove gcc libsasl2-dev python-dev libldap2-dev libssl-dev libsnmp-dev

# Expose port
EXPOSE 80

# Launch the fastAPI server
CMD ["uvicorn","server:app", "--host", "0.0.0.0","--port", "80" ]


