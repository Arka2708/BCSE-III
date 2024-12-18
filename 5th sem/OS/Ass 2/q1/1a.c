#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <time.h>

#define ITERATIONS 10
#define MIN_RANDOM_NUMBER 50000
#define MAX_RANDOM_NUMBER 100000

int getRandomNumber(){
    return rand()%((MAX_RANDOM_NUMBER+1)-MIN_RANDOM_NUMBER) + MIN_RANDOM_NUMBER;
}

void displayData(char* processName, int iteration){
    printf("Process  : %s  | PID : %d | Iteration : %d\n", processName, getpid(), iteration+1);
    usleep(getRandomNumber());  // Sleep random time
}

int main()
{
    srand(time(NULL));
    int pidX = -1;
    int pidY = -1;
    pidX = fork();
    if (pidX == 0){
        // Inside child X
        for (int i = 0; i < ITERATIONS; i++){
            displayData("X", i);
        }
    }
    else{
        pidY = fork();
        if (pidY == 0){
            // Inside Child Y
            for (int i = 0; i < ITERATIONS; i++) {
                displayData("Y", i);
            }
        }
    }
    for (int i = 1; i <= 2; i++){
       wait(NULL);
    }
    return 0;
}