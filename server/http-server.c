#include <sys/socket.h>
#include <error.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

int main(){
    struct sockaddr_in address;
    int addrlen = sizeof(address);
    const int PORT = 8000;
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = htonl(INADDR_ANY);
    address.sin_port = htons(PORT);

    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if(server_fd<0){
        perror("cannot creat socket\n");
        return 0;
    }

    int server_bind = bind(server_fd, (struct sockaddr *)&address, sizeof(address));
    if(server_bind<0){
        perror("Could not bind\n");
        return 0;
    }

    int server_listen = listen(server_fd, 3);
    if(server_listen<0){
        perror("Cannot listen\n");
        exit(EXIT_FAILURE);
    }

    int new_socket = accept(server_fd, (struct sockaddr*)&address, (socklen_t*)&addrlen);
    if(new_socket<0){
        perror("cannot create new socket\n");
        exit(EXIT_FAILURE);
    }
    
    char buffer[1024] = {0};

    int valread = read(new_socket, buffer, 1024);
    printf("%s\n",buffer);
    if(valread<0){
        printf("No bytes to read\n");
    }

    char *hello = "I am server!\n";
    write(new_socket, hello, strlen(hello));

    close(new_socket);

    return 0;
    
}
