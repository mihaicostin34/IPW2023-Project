FROM python
RUN pip install flask redis
COPY login.py ./
CMD ["flask", "--app", "login.py","run", "--host", "0.0.0.0"]