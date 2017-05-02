swig -python omalley.i
g++ -O2 -fPIC -c omalley.c
g++ -O2 -fPIC -c omalley_wrap.c -I/usr/include/python2.7
g++ -shared omalley.o omalley_wrap.o -o _omalley.so
