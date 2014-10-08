all: magic.so

magic.so: magic.c
	gcc -std=c99 -O3 -shared -o magic.so magic.c
