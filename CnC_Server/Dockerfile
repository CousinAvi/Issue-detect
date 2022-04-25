FROM node:14.17.1 as build
WORKDIR /base
COPY ./frontend/package.json .
COPY ./frontend/yarn.lock .
RUN yarn install
COPY ./frontend/ ./
RUN yarn build

FROM python:3.9
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
COPY --from=build /base/dist/ ./app/frontend/dist/
EXPOSE 80
#WORKDIR /code/app

CMD ["python3", "-m", "app"]