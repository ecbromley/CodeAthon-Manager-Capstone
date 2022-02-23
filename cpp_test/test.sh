#!/bin/bash
g++ -o Test main.cpp
touch output.txt
./Test >> output.txt