#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <unistd.h>
#include <netinet/in.h>
#include <string.h>
#include <arpa/inet.h>

int main(){
    struct sockaddr_in server_address;
    const int PORT = 8000;
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(PORT);
    char *hello = "I am the client!\n";
    char buffer[1024] = {0};
    
    int new_socket = socket(AF_INET, SOCK_STREAM, 0);
    if(new_socket<0){
        perror("cannot create new socket.\n");
        exit(EXIT_FAILURE);
    }

    int server_conn = connect(new_socket, (struct sockaddr *)&server_address, sizeof(server_address));
    if(server_conn<0){
        perror("Connection failed\n");
        exit(EXIT_FAILURE);
    }

    send(new_socket ,hello, strlen(hello),0);
    printf("Sent\n");
    int valread = read(new_socket, buffer, 1024);
    printf("From server: %s\n",buffer);
    return 0;
}
