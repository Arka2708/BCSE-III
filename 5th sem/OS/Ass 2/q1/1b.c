#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <unistd.h>
#include <semaphore.h>
#include <fcntl.h>
#include <sys/wait.h>
#include <time.h>

#define ITERATIONS 10
#define MIN_RANDOM_NUMBER 50000
#define MAX_RANDOM_NUMBER 100000

sem_t* mutex;

int getRandomNumber(){
    return rand()%((MAX_RANDOM_NUMBER+1)-MIN_RANDOM_NUMBER) + MIN_RANDOM_NUMBER;
}

void displayData(char* processName, int iteration){
    printf("Process  : %s  | PID : %d | Iteration : %d\n", processName, getpid(), iteration+1);
    usleep(getRandomNumber());  // Sleep random time
}

int main(){
    srand(time(NULL));
    //sem_init(&mutex, 1, 0);
    sem_unlink("mutex015");
    mutex = sem_open("mutex015", O_CREAT, 0777, 0);
    int pidX = -1;
    int pidY = -1;
    pidX = fork();
    if (pidX == 0){
        // Inside child X
        for (int i = 0; i < ITERATIONS; i++){
            displayData("X", i);
        }
        sem_post(mutex);
    }
    else{
        pidY = fork();
        if (pidY == 0){
            // Inside Child Y
            sem_wait(mutex);
            for (int i = 0; i < ITERATIONS; i++)
            {
                displayData("Y", i);
            }
        }
    }

    for (int i = 1; i <= 2; i++){
        wait(NULL);
    }
    sem_destroy(mutex);
    return 0;
}