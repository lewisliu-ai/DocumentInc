#ifndef ACCOUNT_H
#define ACCOUNT_H

class Account {

private:
	String accountNumber;
	String Last4SSN;
	boolean isLinked;

public:
	boolean verify();

	boolean link();

	boolean unlink();
};

#endif
