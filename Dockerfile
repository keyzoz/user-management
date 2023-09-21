FROM python:3.11.5-alpine3.17

RUN mkdir -p user_management_service
WORKDIR  /user_management_service

COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy

COPY . .


CMD ["uvicorn", "main:app", "--host=0.0.0.0" , "--reload" , "--port", "8000"]
