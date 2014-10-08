#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_LENGTH 4096

typedef unsigned long long bb;

typedef struct {
    int length;
    int bits;
    bb keys[MAX_LENGTH];
    bb values[MAX_LENGTH];
} Model;

int rand_int(int n) {
    int result;
    while (n <= (result = rand() / (RAND_MAX / n)));
    return result;
}

double rand_double() {
    return (double)rand() / (double)RAND_MAX;
}

bb rand_magic() {
    bb result = 0;
    bb a = rand_int(0x10000);
    bb b = rand_int(0x10000);
    bb c = rand_int(0x10000);
    bb d = rand_int(0x10000);
    result |= a;
    result |= b << 16;
    result |= c << 32;
    result |= d << 48;
    return result;
}

int magic_test(Model *model, bb magic) {
    int shift = 64 - model->bits;
    bb *table = calloc(1 << model->bits, sizeof(bb));
    for (int i = 0; i < model->length; i++) {
        int index = (model->keys[i] * magic) >> shift;
        if (table[index]) {
            if (table[index] != model->values[i]) {
                free(table);
                return 0;
            }
        }
        else {
            table[index] = model->values[i];
        }
    }
    free(table);
    return 1;
}

int magic_energy(Model *model, bb magic) {
    int result = 0;
    int shift = 64 - model->bits;
    bb *table = calloc(1 << model->bits, sizeof(bb));
    for (int i = 0; i < model->length; i++) {
        int index = (model->keys[i] * magic) >> shift;
        if (table[index]) {
            if (table[index] != model->values[i]) {
                result++;
            }
        }
        else {
            table[index] = model->values[i];
        }
    }
    free(table);
    return result;
}

bb magic_anneal(Model *model, double max_temp, double min_temp, int steps) {
    bb magic = rand_magic();
    bb best = magic;
    double factor = -log(max_temp / min_temp);
    int energy = magic_energy(model, magic);
    int previous_energy = energy;
    int best_energy = energy;
    int total = 0;
    int jumps = 0;
    for (int step = 0; step < steps; step++) {
        double temp = max_temp * exp(factor * step / steps);
        bb undo = magic;
        magic ^= (bb)1 << rand_int(64);
        energy = magic_energy(model, magic);
        double change = energy - previous_energy;
        total++;
        if (change > 0 && exp(-change / temp) < rand_double()) {
            magic = undo;
        }
        else {
            if (change > 0) {
                jumps++;
            }
            previous_energy = energy;
            if (energy < best_energy) {
                double pct = 100.0 * jumps / total;
                printf("t=%f, e=%d, jumps=%.2f%%\n", temp, energy, pct);
                total = 0;
                jumps = 0;
                best_energy = energy;
                best = magic;
            }
            if (energy == 0) {
                return magic;
            }
        }
    }
    return 0;
}

bb magic_search(Model *model, double max_temp, double min_temp, int steps) {
    srand(time(NULL));
    while (1) {
        bb result = magic_anneal(model, max_temp, min_temp, steps);
        if (result) {
            return result;
        }
    }
}

bb magic_search_random(Model *model) {
    srand(time(NULL));
    while (1) {
        bb magic = rand_magic() & rand_magic() & rand_magic();
        if (magic_test(model, magic)) {
            return magic;
        }
    }
}
