#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <errno.h>
#include <fcntl.h>
#include <semaphore.h>
#include <time.h>
#include <sys/mman.h>
#include <sys/ipc.h>
#include <sys/shm.h>

int N;
enum Status{
	THINKING,
	HUNGRY,
	EATING
};

enum Status *state;
sem_t *mutex;
sem_t **condition;

char *mutex_key_from_no(int n){
	char *buffer;
	buffer = (char *)malloc(sizeof(char) * 50);
	sprintf(buffer, "mutex%d", n);
	return buffer;
}

// test left and right
void test(int i){
	if (state[i] == HUNGRY && state[(i + 1) % 5] != EATING && state[(i + 4) % 5] != EATING){
		// update state to eating
		sem_wait(mutex);
		state[i] = EATING;
		sem_post(mutex);
		
		sleep(2);
		// eating
		printf("Philosopher %d takes fork %d and %d\n", i + 1, (i + 4) % 5 + 1, i + 1);
		printf("Philosopher %d is Eating\n", i + 1);
		sem_post(condition[i]); // signal
	}
}

// pickup chopsticks
void pickup(int i){
	// update state to hungry
	sem_wait(mutex);
	state[i] = HUNGRY;
	printf("Philosopher %d is Hungry\n", i + 1);
	sem_post(mutex);

	// eat if neighbours are not eating
	test(i);
	// if unable to eat wait to be signalled
	sem_wait(condition[i]);
	sleep(1);
}

// put down chopsticks
void putdown(int i){
	// update state to thinking
	sem_wait(mutex);
	state[i] = THINKING;
	sem_post(mutex);

	printf("Philosopher %d putting fork %d and %d down\n", i + 1, (i + 4) % 5 + 1, i + 1);
	printf("Philosopher %d is thinking\n", i + 1);
	test((i + 4) % 5);
	test((i + 1) % 5);
}

// start philosopher action
void startPhilosopherAction(int num){
	while (1){
		sleep(1);
		pickup(num);
		sleep(0);
		putdown(num);
	}
}

int main(){
	printf("Enter value of N : ");
	scanf("%d", &N);

	// allocate memory
	state = mmap(NULL, sizeof(enum Status) * N, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
	condition = mmap(NULL, sizeof(sem_t *) * N, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);

	for (int i = 0; i < N; i++){
		state[i] = THINKING;
	}

	// initializemutex semaphore
	mutex = sem_open("mutex56", O_CREAT, 0777, 1);
	// initialize condition semaphore
	for (int i = 0; i < N; i++){
		condition[i] = sem_open(mutex_key_from_no(i), O_CREAT, 0777, 1);
	}

	int id = fork();
	if (id == 0){
		// Fork childs
		for (int i = 0; i < N; i++){
			id = fork();
			if (id == 0){
				startPhilosopherAction(i);
				exit(1);
			}
		}
		for (int i = 0; i < N; i++){
			wait(NULL);
		}
		exit(1);
	}else{
		wait(NULL);
	}
	return 0;
}