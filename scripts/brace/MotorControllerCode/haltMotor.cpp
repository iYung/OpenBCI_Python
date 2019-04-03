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

HANDLE keyHandle = 0;
unsigned short node = 1;
string deviceName = "EPOS";
string protocolStackName = "MAXON_RS232";
string interfaceName = "RS232";
string portName = "/dev/ttyS35";
//baudrate = "115200";
unsigned int errorCode = 0;

char* pDeviceName = new char[255];
	char* pProtocolStackName = new char[255];
	char* pInterfaceName = new char[255];
	char* pPortName = new char[255];

	strcpy(pDeviceName, deviceName.c_str());
	strcpy(pProtocolStackName, protocolStackName.c_str());
	strcpy(pInterfaceName, interfaceName.c_str());
	strcpy(pPortName, portName.c_str());

keyHandle = VCS_OpenDevice(pDeviceName, pProtocolStackName, pInterfaceName, pPortName, &errorCode);
cout << "key Handle: ";
cout << keyHandle <<endl;
if (keyHandle>0)
{
if (VCS_SetProtocolStackSettings(keyHandle,115200,500,&errorCode)>0) 
	{
	cout << "Success";
	printf("communication established\n");
	}
	else
	cout <<"FAIL22";
}
else 
	cout << "FAIL11!";




if(VCS_ActivateProfileVelocityMode(keyHandle,node,&errorCode))
	cout << "velocity mode activated" << endl;

VCS_SetEnableState(keyHandle,node,&errorCode);

if(VCS_HaltVelocityMovement(keyHandle, node, &errorCode)== 0){
	cout<< "error :" ;
	cout<< errorCode << endl;

}

return 1;
}
