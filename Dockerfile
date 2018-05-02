FROM python

# copy the rest of the app
COPY . /app

# Workdir
WORKDIR /app
RUN pip install -r requirements.txt
