#include <sys/socket.h>
#include <error.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>
#include <string.h>
#include <fcntl.h>
#include <sys/stat.h>

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

    while(1){
        printf("---Waiting for connection---\n");
        int new_socket = accept(server_fd, (struct sockaddr*)&address, (socklen_t*)&addrlen);
        if(new_socket<0){
            perror("cannot create new socket\n");
            exit(EXIT_FAILURE);
        }
        
        char buffer[1024] = {0};
    
        int valread = read(new_socket, buffer, 1024);
        if(valread<0){
            printf("No bytes to read\n");
        }
        
        char filename[1024];
        sscanf(buffer, "GET /%s HTTP/1.1", filename);
        printf("GET %s HTTP/1.1\n",filename);
        int file_fd = open(filename, O_RDONLY);
        if(file_fd<0){
            char *response = "HTTP/1.1 404 NOT FOUND\r\n\r\n";
            write(new_socket, response, strlen(response));
            close(new_socket);
            continue;
        }
        
        printf("Hello\n");
        off_t file_size = lseek(file_fd, 0, SEEK_END);
        lseek(file_fd, 0, SEEK_SET);

        char *file_data = (char *)malloc(file_size);

        ssize_t content_length = read(file_fd, file_data, file_size);
        char response[61+content_length];
        snprintf(response,sizeof(response),"HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Length:%ld\n\n%s",content_length, file_data);
        printf("%s", response);
        
        //write(new_socket, response, strlen(response));
        write(new_socket, response,61+content_length);
        close(new_socket);
        }
    return 0;
    
}
