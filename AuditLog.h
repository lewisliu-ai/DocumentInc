#ifndef AUDITLOG_H
#define AUDITLOG_H

class AuditLog {

private:
	String logId;
	String action;
	Date timestamp;
	String details;

public:
	void create();

	List query();
};

#endif
