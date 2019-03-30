#include <iostream>
#include "Definitions.h"
#include <string.h>
#include <sstream>
#include <unistd.h>
#include <getopt.h>
#include <stdlib.h>
#include <stdio.h>
#include <list>
#include <math.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdio.h>
#include <sys/times.h>
#include <sys/time.h>

typedef void* HANDLE;
typedef int BOOL;

using namespace std;

int main(){

HANDLE keyHandle = 0x40001;
unsigned short node = 1;
string deviceName = "EPOS";
string protocolStackName = "MAXON_RS232";
string interfaceName = "RS232";
string portName = "ttyS0";
//baudrate = "115200";
unsigned int errorCode = 0;

long vel = 2000;

VCS_MoveWithVelocity(keyHandle,node,vel,&errorCode);

return 1;
}