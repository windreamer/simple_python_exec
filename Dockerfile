FROM python:3.10-slim

WORKDIR /app

RUN pip install --upgrade pip && \
    pip install numpy pandas scipy scikit-learn matplotlib seaborn sympy fastmcp

COPY server.py /app/server.py

EXPOSE 8080

USER 1000

CMD ["python", "/app/server.py"]
