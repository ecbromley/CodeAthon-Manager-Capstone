FROM gcc:latest

COPY . /usr/src/cpp_test

WORKDIR /usr/src/cpp_test

RUN g++ -o Test main.cpp

CMD [ "./Test | output.txt", "echo output.txt" ]