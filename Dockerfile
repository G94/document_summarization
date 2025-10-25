FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN ls -al /app

# RUN python -m venv .venv
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt



### copy the rest of the documents 
COPY ./app .
# COPY ./Makefile /app/Makefile

# ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV PYTHONPATH="/app"
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]