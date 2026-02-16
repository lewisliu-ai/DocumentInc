#ifndef STATEMENT_H
#define STATEMENT_H

class Statement {

private:
	string statementId;
	Date statementDate;
	String pdfUrl;
	String type;

public:
	void view();

	File download();

	List searchByDate();
};

#endif
