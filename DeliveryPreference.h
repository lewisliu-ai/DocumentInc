#ifndef DELIVERYPREFERENCE_H
#define DELIVERYPREFERENCE_H

class DeliveryPreference {

private:
	boolean isDigital;
	Date effectiveDate;
	float paperFee;

public:
	void update();

	String getStatus();
};

#endif
