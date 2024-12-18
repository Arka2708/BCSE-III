/*6. Write a program for the Reader-Writer process for the following situations:
a) Multiple readers and one writer: writer gets to write whenever it is ready (reader/s wait)
b) Multiple readers and multiple writers: readers get priority over any writer (writer/s wait) 
c) Multiple readers and multiple writers: any writer gets to write whenever it is ready, provided no other
writer is currently writing (reader/s wait)*/
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

#define no_of_readers 5
#define MIN_RANDOM_NUMBER 1
#define MAX_RANDOM_NUMBER 5

sem_t *write_mutex;
int *read_counter;
sem_t *read_counter_mutex;
int *resource;

int getRandomNumber(){
    return rand() % ((MAX_RANDOM_NUMBER + 1) - MIN_RANDOM_NUMBER) + MIN_RANDOM_NUMBER;
}

int main()
{
    sem_unlink("mutex34");
    sem_unlink("mute56");
    write_mutex = sem_open("mutex34", O_CREAT, 0777, 1);
    read_counter_mutex = sem_open("mute56", O_CREAT, 0777, 1);
    read_counter = mmap(NULL, sizeof *read_counter, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    resource = mmap(NULL, sizeof *resource, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);

    int id;
    id = fork();
    if (id == 0){
        // Start reader processes
        for (int i = 0; i < no_of_readers; i++){
            id = fork();
            if (id == 0){
                time_t t;
                srand((int)time(&t) % getpid());
                // Reader process
                sleep(getRandomNumber());

                sem_wait(read_counter_mutex);
                *read_counter++;
                if (*read_counter == 1) sem_wait(write_mutex);
                sem_post(read_counter_mutex);

                // Read
                printf("Reader %d read %d\n", i + 1, *resource);

                sem_wait(read_counter_mutex);
                *read_counter--;
                if (*read_counter == 0) sem_post(write_mutex);
                sem_post(read_counter_mutex);
                
                exit(1);
            }
        }
    }
    else{
        time_t t;
        srand((int)time(&t) % getpid());
        sleep(getRandomNumber());
        // Wait for all readers to finish
        sem_wait(write_mutex);
        *resource = getRandomNumber();
        printf("Writer wrote %d\n", *resource);
        sem_post(write_mutex);
    }

    // Wait for all childs to finish
    for (int i = 0; i < no_of_readers + 1; i++) {
        wait(NULL);
    }

    return 0;
}