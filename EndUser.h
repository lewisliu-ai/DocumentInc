#ifndef ENDUSER_H
#define ENDUSER_H

class EndUser {

private:
	String deliverPreference;
	Date lastLogin;

public:
	boolean registerUser();

	void opIn();

	void optOut();

	boolean linkAccount();
};

#endif
