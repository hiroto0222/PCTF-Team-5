#include <stdio.h>
#include <errno.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <signal.h>
#include <string.h>
#include <stdbool.h>
#include <time.h>

#define MAXMSG 512

int socketFD;
int PORT;

/*
 * Executes CMD using popen.
 * This function will return a character string with the stdout of the command
 * that was locally executed.
 *
 */
char *printCMD(char *cmd)
{

  printf("\nExecuting command: %s\n", cmd);

  // Reads 512 - 1 chars at a time.
  char line[512];
  char *buffer = NULL;
  unsigned int size = 0;
  FILE *fp = popen(cmd, "r");

  if (fp == NULL)
    error("Error opening pipe.");

  // Loops through entire pipe.
  // Increasing the size of the return buffer every time more characters are found.
  while (fgets(line, sizeof(line), fp))
  {
    size += strlen(line);
    strcat(buffer = realloc(buffer, size), line);
  }

  pclose(fp);

  return buffer;
}

/*
 * Create and Bind Socket on Server.
 *
 */
void makeSocket()
{

  struct sockaddr_in serverAddr;
  int servAddrLen = sizeof(serverAddr);

  // Create a new socket File Descriptor
  if ((socketFD = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    error("Socket failure.");

  // Clears buffer
  bzero((char *)&serverAddr, servAddrLen);

  // Fill server address struct info for binding socket.
  serverAddr.sin_family = AF_INET;
  serverAddr.sin_port = htons(PORT);
  serverAddr.sin_addr.s_addr = INADDR_ANY;

  // Associate and bind socket to address and port.
  if (bind(socketFD, (struct sockaddr *)&serverAddr, servAddrLen) < 0)
    error("Bind failure");
}

/*
 *	Perform any sort of parsing/modifying before sending the command to be executed.
 *
 */
char *parseBuffer(char buffer[])
{

  printf(buffer);

  return printCMD(buffer);
}

/*
 * This function will listen on the PORT, once connection is made the main thread will fork()
 * into a parent thread and child thread.
 * The child thread will execute parseBuffer() sending the incoming request message to parseBuffer().
 * Once parseBuffer() sends a response this function will send that formatted response through the socket.
 * Then close the socket and kill the child process since it is no longer needed.
 * The parent thread will simply close the socket it's instance of the socket and start the while
 * loop all over again listening on the PORT.
 *
 */
void startServer()
{

  int newSocketFD, in, pid;
  struct sockaddr_in clientAddr;
  int clientAddrLen = sizeof(clientAddr);
  char buffer[MAXMSG] = {0};
  // Create socket.
  makeSocket();

  // Allow server to listen for any connection on socket.
  if (listen(socketFD, 3) < 0)
    error("Listen Failure.");

  // Infinite loop to keep accepting socket connection requests.
  while (1)
  {
    // Block process until client connects to server.
    newSocketFD = accept(socketFD, (struct sockaddr *)&clientAddr, (socklen_t *)&clientAddrLen);
    if (newSocketFD < 0)
      error("Socket Accept Failure.");

    // Create a new process.
    pid = fork();
    if (pid < 0)
      error("Couldn't fork communication to seperate thread.");

    // Fork thread to child thread. Then close the socket to stop listening so that
    // server can process the incoming message and reply. Once done kill child thread.
    // Main thread keeps listening for new connections.
    if (pid == 0)
    { // Child thread
      close(socketFD);

      // Initialize Buffer
      bzero(buffer, MAXMSG);
      in = read(newSocketFD, buffer, MAXMSG);
      char *replyMsg = parseBuffer(buffer);
      send(newSocketFD, replyMsg, strlen(replyMsg), 0);
      printf("\nResponse:\n%s", replyMsg);

      // Close child thread socket and process.
      close(newSocketFD);
      exit(1);
    }
    else
    { // Parent thread
      close(newSocketFD);
    }
  }
}

int main(int argc, char *argv[])
{

  // Taken per professor Adam Doupe's post on Google group.
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);

  if (argc > 1)
  {
    sscanf(argv[1], "%d", &PORT);
    startServer();
  }
  else
  {
    error("Please specify Port # as argument.");
  }

  return 0;
}
