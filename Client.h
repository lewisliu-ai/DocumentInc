#ifndef CLIENT_H
#define CLIENT_H

class Client {

private:
	String clientId;
	String clientName;
	int retentionDays;

public:
	int getRetentionSettings();

	int retentionDays();
};

#endif
