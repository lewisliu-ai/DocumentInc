#ifndef CLIENTADMIN_H
#define CLIENTADMIN_H

class ClientAdmin {

private:
	String clientId;
	String emailDomain;

public:
	List searchUsers();

	List viewUserHistory();

	boolean createAdmin();
};

#endif
