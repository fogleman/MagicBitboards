all: magic

magic: magic.c
	gcc -std=c99 -O3 -o magic magic.c
