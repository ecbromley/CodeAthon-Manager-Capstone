FROM gcc:latest

COPY . /usr/src/cpp_test

WORKDIR /usr/src/cpp_test

RUN chmod a+x test.sh

CMD [ "./test.sh" ]