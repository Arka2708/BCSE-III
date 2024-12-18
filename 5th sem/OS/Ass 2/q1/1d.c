#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <time.h>
#include <semaphore.h>
#include <fcntl.h>

#define ITERATIONS 10
#define MIN_RANDOM_NUMBER 50000
#define MAX_RANDOM_NUMBER 100000

sem_t* mutexX;
sem_t* mutexY;
sem_t* mutexZ;

int getRandomNumber(){
    return rand()%((MAX_RANDOM_NUMBER+1)-MIN_RANDOM_NUMBER) + MIN_RANDOM_NUMBER;
}
void displayData(char* processName, int iteration){
    printf("Process  : %s  | PID : %d | Iteration : %d\n", processName, getpid(), iteration+1);
    usleep(getRandomNumber());  // Sleep random time
}

int main(){
    srand(time(NULL));
    sem_unlink("mutexX");
    sem_unlink("mutexY");
    sem_unlink("mutexZ");

    mutexX = sem_open("mutexX", O_CREAT, 0644, 0);
    mutexY = sem_open("mutexY", O_CREAT, 0644, 0);
    mutexZ = sem_open("mutexZ", O_CREAT, 0644, 0);

    int pidX = -1;
    int pidY = -1;
    int pidZ = -1;
    /*
     Mutex XY
    */ 
    pidX = fork();
    if (pidX == 0){
        // Inside child X
        for (int i = 0; i < ITERATIONS; i++){
            if(i != 0){
                sem_wait(mutexX);
            }
            displayData("X", i);
            sem_post(mutexY);
        }
    }
    else{
        pidY = fork();
        if (pidY == 0){
            // Inside Child Y
            for (int i = 0; i < ITERATIONS; i++){
                sem_wait(mutexY);
                displayData("Y", i);
                sem_post(mutexZ);
            }
        }else{
            pidZ = fork();
            if(pidZ == 0){
                for (int i = 0; i < ITERATIONS; i++)
                {
                    sem_wait(mutexZ);
                    displayData("Z", i);
                    sem_post(mutexX);
                }
            }
        }
    }
    for (int i = 1; i <= 3; i++){
        wait(NULL);
    }
    sem_destroy(mutexX);
    sem_destroy(mutexY);
    sem_destroy(mutexY);
    return 0;
}