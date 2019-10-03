#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <sys/wait.h>
#include <unistd.h>

#define numProcs 4

struct Node {
	int data;
	struct Node *prev;
};

void freeNodes(struct Node *toFree) {
	if (toFree->prev != NULL)
		freeNodes(toFree->prev);
	free(toFree->prev);
	toFree->prev = NULL;
}

int main(int argc, char** argv) {
	long long numToDiv;

	for (int argIndex = 1; argIndex < argc; argIndex++) {
		numToDiv = strtoll(argv[argIndex], NULL, 10);
		if (numToDiv <= 0) {
			printf("Invalid input\n");
			exit(-1);
		}
		int infopipe[numProcs][2];
		long long ranges[numProcs + 1];
		for (int i = 0; i < numProcs; ++i)
			pipe(infopipe[i]);
		double sqrtNum = sqrt(numToDiv);
		int perfSquare = 0;
		for (int i = 0; i < numProcs + 1; ++i)
			ranges[i] = i * (sqrtNum / (numProcs)) + 1;
		if (sqrtNum == (int) sqrtNum)
			perfSquare = 1;

		pid_t pids[numProcs];
		for (int i = 0; i < numProcs; ++i) {
			fflush(stdout);
			pids[i] = fork();
			if (pids[i] < 0) {
				printf("Fork error");
				exit(-1);
			} else if (pids[i] == 0) {
				close(infopipe[i][0]);
				for (long long j = ranges[i]; j < ranges[i + 1]; j++) {
					if (numToDiv % j == 0) {
						write(infopipe[i][1], &j, sizeof(j));
					}
				}
				close(infopipe[i][1]);
				exit(0);
			}
		}

		for (int i = 0; i < numProcs; ++i)
			wait(NULL);

		struct Node* tail = (struct Node*) malloc(sizeof(struct Node));
		struct Node* temp;

		printf("%lld: ", numToDiv);
		for (int i = 0; i < numProcs; ++i) {
			close(infopipe[i][1]);
			while (1) {
				long long childVal;
				if (read(infopipe[i][0], &childVal, sizeof(childVal)) > 0) {
					printf("%lld ", childVal);
					tail->data = childVal;
					temp = (struct Node*) malloc(sizeof(struct Node));
					temp->prev = tail;
					tail = temp;

				} else {
					break;
				}
			}
			close(infopipe[i][0]);
		}

		if (perfSquare && numToDiv != 1)
			temp = tail->prev;
		else
			temp = tail;
		for (struct Node* n = temp->prev; n->prev != NULL; n = n->prev)
			printf("%lld ", numToDiv / n->data);
		printf("%lld ", numToDiv);
		printf("\n");

		freeNodes(tail);
		free(tail);
	}
	return 0;
}
