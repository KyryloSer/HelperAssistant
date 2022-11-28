FROM python:3.10
RUN apt update
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8080
RUN chmod +x run.sh
CMD ["./run.sh"]