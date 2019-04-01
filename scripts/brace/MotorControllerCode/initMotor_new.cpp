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

HANDLE keyHandle = CreateFile("/dev/ttyS1", GENERIC_READ | GENERIC_WRITE,0,0, OPEN_EXSISTING,FILE_FLAG_OVERLAPPED,0);
//DWORD HAND = 0x40001;
unsigned short node = 1;
string deviceName = "EPOS";
string protocolStackName = "MAXON_RS232";
string interfaceName = "RS232";
string portName = "/dev/ttyS1";
//baudrate = "115200";
unsigned int errorCode = 0;

//keyHandle = VCS_OpenDevice(pDeviceName, pProtocolStackName, pInterfaceName, pPortName, &errorCode);
cout << &keyHandle <<endl;
VCS_SetProtocolStackSettings(keyHandle,115200,500,&errorCode);

//long vel[3] = {2000,5000,8000};
long vel = 2000;
VCS_ActivateProfileVelocityMode(keyHandle,node,&errorCode);
VCS_SetEnableState(keyHandle,node,&errorCode);
VCS_MoveWithVelocity(keyHandle,node,vel,&errorCode);
	
return 1;
}