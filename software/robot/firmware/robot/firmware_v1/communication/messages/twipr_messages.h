/*
 * twipr_messages.h
 *
 *  Created on: 3 Mar 2023
 *      Author: lehmann_workstation
 */

#ifndef COMMUNICATION_TWIPR_MESSAGES_H_
#define COMMUNICATION_TWIPR_MESSAGES_H_

#include "core.h"

//template<typename data_type_t, int message_id>
//class TWIPR_Message {
//public:
//	TWIPR_Message(){
//		this->data = &this->data_union.data;
//		this->rx_callback = NULL;
//	}
//
//	TWIPR_Message(void (*rx_callback)(data_type_t*)){
//		this->rx_callback = rx_callback;
//	}
//
//	/* ---------------------------------------------------------- */
//	void set(uint8_t *buffer) {
//		for (uint8_t i = 0; i < sizeof(data_type_t); i++) {
//			this->data_union.data_buffer[i] = buffer[i];
//		}
//	}
//
//	/* ---------------------------------------------------------- */
//	uint8_t serialize(uint8_t *buffer) {
//		for (uint8_t i = 0; i < sizeof(data_type_t); i++) {
//			buffer[i] = this->data_union.data_buffer[i];
//		}
//		return sizeof(data_type_t);
//	}
//	/* ---------------------------------------------------------- */
//	void callback(){
//		this->rx_callback(this->data);
//	}
//
//	/* ---------------------------------------------------------- */
//	union data_union_t {
//		uint8_t data_buffer[sizeof(data_type_t)];
//		data_type_t data;
//	} data_union;
//
//	/* ---------------------------------------------------------- */
//	int id = message_id;
//	data_type_t* data;
//	void (*rx_callback)(data_type_t*);
//};

#endif /* COMMUNICATION_TWIPR_MESSAGES_H_ */
