# Build step #1: build the React front end
FROM node:16-alpine as build-step
WORKDIR /usr/src/app
# TODO: if there's a yarn.lock file use
# COPY frontend/package.json frontend/yarn.lock ./
COPY frontend/ ./
RUN yarn install \
  --prefer-offline \
  --frozen-lockfile \
  --non-interactive \
  --production=false
RUN yarn build

# build the api
FROM python:3.10.7-slim-buster
WORKDIR /usr/src/app
# copy the frontend build to be served statically
COPY --from=build-step /usr/src/app/dist ./build

RUN mkdir ./api
WORKDIR /usr/src/app/api

# install dependencies
RUN pip install --upgrade pip
COPY backend/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY backend/ .
RUN chmod +x entrypoint.sh
