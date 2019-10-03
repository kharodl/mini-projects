#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <sys/wait.h>
#include <unistd.h>
#include <string.h>
#include <pthread.h>
#include <time.h>

#define numProcs 64

typedef struct node {
    long long data;
    struct node * next;
    struct node * prev;
} Node;

typedef struct  {
    long long numToDiv;
    Node * head;
} parameters;

typedef struct {
    long long numToDiv;
    long long rangeStart;
    long long rangeEnd;
    Node * head;
} rangeParams;

void freeNodes(Node * head) {
    if (head->next != NULL)
        freeNodes(head->next);
    head->prev = head->next = NULL;
    head = NULL;
    free(head);
}

void * factorRange(void * params) {
    rangeParams * data = (rangeParams *) params;
    long long numToDiv = data->numToDiv;
    double rangeStart = data->rangeStart;
    double rangeEnd = data->rangeEnd;
    Node * current = malloc(sizeof(Node));
    data->head = current;

    for (long long i = rangeStart; i < rangeEnd; i++) {
        if (numToDiv % i == 0) {
            current->data = i;
            current->next = malloc(sizeof(Node));
            current->next->prev = current;
            current = current->next;
        }
    }
    if (data->head != current) {
        current->prev->next = NULL;
        free(current);
        pthread_exit((void *) 0);
    }
    free(current);
    pthread_exit((void *) 1);
}

void * findFactors(void * params) {
    parameters * data = (parameters *) params;
    long long numToDiv = data->numToDiv;

    if (numToDiv <= 0) {
        printf("Invalid input: %lld\n", numToDiv);
        pthread_exit((void *) -1);
    }

    long long ranges[numProcs + 1];
    double sqrtNum = sqrt(numToDiv);
    int perfSquare = 0;
    for (int i = 0; i < numProcs + 1; ++i)
        ranges[i] = i * (sqrtNum / (numProcs)) + 1;
    if (sqrtNum == (int) sqrtNum)
        perfSquare = 1;

    pthread_t thread[numProcs];
    rangeParams **rangeData = malloc(numProcs * sizeof(rangeParams *));
    for (int i = 0; i < numProcs; ++i) {
        rangeData[i] = malloc(sizeof(rangeParams));
        rangeData[i]->numToDiv = numToDiv;
        rangeData[i]->rangeStart = ranges[i];
        rangeData[i]->rangeEnd = ranges[i+1];
        pthread_create(&thread[i], NULL, factorRange, rangeData[i]);
    }

    Node * current = NULL;
    void ** temp = malloc(sizeof(void *));
    int firstNode = 1;
    for (int i = 0; i < numProcs; ++i) {
        pthread_join(thread[i], temp);
        if (* temp < (void *) 0)
            exit(-1);
        if (* temp == (void *) 0) {
            if (firstNode) {
                data->head = rangeData[i]->head;
                current = data->head;
                current->prev = NULL;
                firstNode = 0;
            } else {
                current->next = rangeData[i]->head;
                rangeData[i]->head->prev = current;
            }
            while (current->next != NULL)
                current = current->next;
        }
        free(rangeData[i]);
    }
    free(temp);
    free(rangeData);

    Node * endNode;
    if (perfSquare && numToDiv != 1)
        endNode = current->prev;
    else
        endNode = current;

    for (Node * n = endNode; n != data->head; n = n->prev) {
        current->next = malloc(sizeof(Node));
        current->next->prev = current;
        current = current->next;
        current->data = numToDiv / n->data;
    }
    current->next = NULL;

    pthread_exit((void *) 0);
}

int main(int argc, char** argv) {
    pthread_t thread[argc-1];
    parameters **data = malloc((argc-1) * sizeof(parameters *));
    struct timespec startTime, endTime;
    clock_gettime(CLOCK_MONOTONIC, &startTime);

    for (int i = 0; i < argc-1; ++i) {
        data[i] = malloc(sizeof(parameters));
        data[i]->numToDiv = strtoll(argv[i+1], NULL, 10);
        data[i]->head = NULL;
        pthread_create(&thread[i], NULL, findFactors, data[i]);
    }

    void ** temp = malloc(sizeof(void *));
    for (int i = 0; i < argc-1; ++i) {
        pthread_join(thread[i], temp);
        if (* temp < (void *) 0)
            exit(-1);
        printf("%lld: ", data[i]->numToDiv);
        for (Node * n = data[i]->head; n != NULL; n = n->next)
            printf("%lld ", n->data);
        printf("%lld\n", data[i]->numToDiv);
        freeNodes(data[i]->head);
        free(data[i]);
    }
    free(temp);
    free(data);
    clock_gettime(CLOCK_MONOTONIC, &endTime);
    double timeTaken = endTime.tv_sec - startTime.tv_sec;
    timeTaken += (endTime.tv_nsec - startTime.tv_nsec) / 1000000000.0;
    printf("\nOperation took %lf seconds\n", timeTaken);
    return 0;
}

