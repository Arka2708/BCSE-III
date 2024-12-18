/*5. Write a program for p-producer c-consumer problem. A shared circular buffer that can hold 20 items is
to be used. Each producer process can store any numbers between 1 to 50 (along with the producer id) in
the buffer. Each consumer process can read from the buffer and add them to a variable GRAND (initialized
to 0). Though any consumer process can read any of the numbers in the buffer, the only constraint being
that any number written by some producer should be read exactly once by exactly one of the consumers.
(a) Assume 5 producers and 10 consumers, with each producer doing 10 iterations and each consumer
doing 4 iterations. .
(b) After the rounds are finished, the parent process prints the value of GRAND.
(c) Can you induce race condition in this problem? Justify your answer.*/
#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>
#include <stdlib.h>
#include <unistd.h>

#define BUFFER_SIZE 20
#define NUM_PRODUCERS 5
#define NUM_CONSUMERS 10
#define PRODUCER_ITERATIONS 10
#define CONSUMER_ITERATIONS 6

int buffer[BUFFER_SIZE];
int next_in = 0;
int next_out =0;
int producer_id = 0;
int GRAND = 0;
int consumed[50];

sem_t buffer_mutex, empty, full;
int allConsumed() {
    for (int i = 0; i < BUFFER_SIZE; i++) {
        if (buffer[i] != -1) 
            return 0;
    }
    return 1;
}
void *producer(void *arg) {
    int id = *(int *)arg;
    for (int i = 0; i < PRODUCER_ITERATIONS; i++) {
          if(allConsumed()){
             break;
          }
        int item = (rand() % 50) + 1; // Generate a random number between 1 and 50
        sem_wait(&empty);
        sem_wait(&buffer_mutex);

        while(consumed[item-1]==1){
            item= (rand()%50) +1;
        }
        buffer[next_in] = item;
        printf("Producer %d produced: %d ->", id, item);
        next_in = (next_in + 1) % BUFFER_SIZE;
        
        for(int i=0 ;i<20 ;i++) printf("%d ", buffer[i]);
        printf("\n");
        sem_post(&buffer_mutex);
        sem_post(&full);
    }
    pthread_exit(NULL);
}

void *consumer(void *arg) {
    int id = *(int *)arg;
    for (int i = 0; i < CONSUMER_ITERATIONS; i++) {
         if(allConsumed()){
             break;
          }
        sem_wait(&full);
        sem_wait(&buffer_mutex);
        
         while(buffer[next_out]==-1 || buffer[next_out]==0){
           next_out = (next_out + 1) % BUFFER_SIZE;
        }
        int item = buffer[next_out];
        item=buffer[next_out];
        buffer[next_out]=-1;
        consumed[item-1]=1;
        printf("Consumer %d consumed: %d ->", id, item);
        GRAND += item;
       next_out = (next_out + 1) % BUFFER_SIZE;     
        for(int i=0 ;i<20 ;i++) printf("%d ", buffer[i]);
        printf("\n");
        sem_post(&buffer_mutex);
        sem_post(&empty);
    }
     pthread_exit(NULL);
}

int main() {
    srand(time(NULL));

    sem_init(&buffer_mutex, 0, 1);
    sem_init(&empty, 0, BUFFER_SIZE);
    sem_init(&full, 0, 0);

    pthread_t producers[NUM_PRODUCERS];
    pthread_t consumers[NUM_CONSUMERS];
    int producer_ids[NUM_PRODUCERS];
    int consumer_ids[NUM_CONSUMERS];
     for(int i=0 ;i<50 ;i++) consumed[i]=0;

    for (int i = 0; i < NUM_PRODUCERS; i++) {
        producer_ids[i] = i;
        pthread_create(&producers[i], NULL, producer, &producer_ids[i]);
    }

    for (int i = 0; i < NUM_CONSUMERS; i++) {
        consumer_ids[i] = i;
        pthread_create(&consumers[i], NULL, consumer, &consumer_ids[i]);
    }

    for (int i = 0; i < NUM_PRODUCERS; i++) {
        pthread_join(producers[i], NULL);
    }
    
    for (int i = 0; i < NUM_CONSUMERS; i++) {
        pthread_join(consumers[i], NULL);
    }
    sem_destroy(&empty);
    sem_destroy(&full);
    sem_destroy(&buffer_mutex);

    printf("GRAND: %d\n", GRAND);

    return 0;
}
