#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include "queue.h"

// cria uma nova queue
queue* new_queue()
{
    queue* qu = malloc(sizeof(queue));
    qu->q= malloc(sizeof(int)*TAMQUEUE);
    qu->primeiro = 0;
    qu->ultimo = TAMQUEUE-1;
    qu->numElem = 0;
        
	return qu;
}

//destroy a queue desalocando a memoria ocupada por esta
void queue_destroy(queue *qu)
{
	free(qu->q);
    free(qu);
}

//insere um elemento no fim da fila
void enqueue(queue *q, int n)
{
    if (q->numElem >= TAMQUEUE)
		printf("Queue cheia, nao e possivel inserir mais elementos.");
    else {
        q->ultimo = (q->ultimo+1) % TAMQUEUE;
        q->q[q->ultimo] = n;    
        q->numElem = q->numElem + 1;
    }
}

//remove o elemento no inicio da fila
int dequeue(queue *q)
{
	int n;

    if (q->numElem <= 0) 
        printf("Queue vazia, nao e possivel retirar mais elementos da fila.");
    else {
        n = q->q[ q->primeiro ];
        q->primeiro = (q->primeiro+1) % TAMQUEUE;
        q->numElem = q->numElem - 1;
    }

    return(n);
}

bool isEmpty(queue *q)
{
    return q->numElem <= 0;
}

void print_queue(queue *q)
{
    int i;

	i=q->primeiro; 
        
    while (i != q->ultimo) {
        printf("%d ",q->q[i]);
                i = (i+1) % TAMQUEUE;
        }

    printf("%2d ",q->q[i]);
    printf("\n");
}
