FROM python
RUN pip install flask redis datetime
COPY post.py ./
CMD ["flask", "--app", "post.py","run", "--host", "0.0.0.0"]