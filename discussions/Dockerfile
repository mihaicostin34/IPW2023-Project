FROM python
RUN pip install flask redis datetime
COPY discussions.py ./
CMD ["flask", "--app", "discussions.py","run", "--host", "0.0.0.0"]