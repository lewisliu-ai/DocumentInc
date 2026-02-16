#ifndef USER_H
#define USER_H

class User : EndUser, ClientAdmin {

private:
	String userId;
	String username;
	String password;
	String email;
	Date createdDate;

public:
	boolean login();

	void logout();

	boolean resetPassword();

	boolean updateEmail();
};

#endif
