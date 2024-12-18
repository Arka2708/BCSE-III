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
#define MIN_RANDOM_NUMBER 1
#define MAX_RANDOM_NUMBER 6

sem_t *write_mutex;
sem_t *mutex;
int *read_counter;
int *resource;

int getRandomNumber(){
    return rand() % ((MAX_RANDOM_NUMBER + 1) - MIN_RANDOM_NUMBER) + MIN_RANDOM_NUMBER;
}

int main()
{
    int no_of_readers;
    int no_of_writers;

    printf("Enter no of readers: ");
    scanf("%d", &no_of_readers);
    printf("Enter no of writers: ");
    scanf("%d", &no_of_writers);

    sem_unlink("mutex34");
    sem_unlink("mute56");
    write_mutex = sem_open("mutex34", O_CREAT, 0777, 1);
    mutex = sem_open("mutex56", O_CREAT, 0777, 1);

    read_counter = mmap(NULL, sizeof *read_counter, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    resource = mmap(NULL, sizeof *resource, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    int id;

    id = fork();

    if (id == 0) {
        // Start reader processes
        for (int i = 0; i < no_of_readers; i++) {
            id = fork();
            if (id == 0){
                time_t t;
                srand((int)time(&t) % getpid());
                // Reader process
                sleep(getRandomNumber());
                  
                sem_wait(mutex);
                *read_counter++;
                if (*read_counter == 1) sem_wait(write_mutex);
                sem_post(mutex);

                // Read
                printf("Reader %d read %d\n", i + 1, *resource);

                sem_wait(mutex);
                *read_counter--;
                if (*read_counter == 0) sem_post(write_mutex);
                sem_post(mutex);

                exit(1);
            }
        }
        // Wait for all childs to finish
        for (int i = 0; i < no_of_readers; i++)
        {
            wait(NULL);
        }
        exit(1);
    }
    else {
        for (int i = 0; i < no_of_writers; i++){
            id = fork();
            if (id == 0){
                time_t t;
                srand((int)time(&t) % getpid());
                sleep(getRandomNumber());

                sem_wait(write_mutex);

                // Write
                *resource = getRandomNumber();
                printf("Writer %d wrote %d\n", i + 1, *resource);

                sem_post(write_mutex);
                exit(1);
            }
        }

        // Wait for all childs to finish
        for (int i = 0; i < no_of_readers; i++){
            wait(NULL);
        }
        wait(NULL);
    }
    return 0;
}