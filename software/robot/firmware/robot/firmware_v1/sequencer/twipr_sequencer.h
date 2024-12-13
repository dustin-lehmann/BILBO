/*
 * twipr_sequencer.h
 *
 *  Created on: Nov 20, 2024
 *      Author: Dustin Lehmann
 */

#ifndef SEQUENCER_TWIPR_SEQUENCER_H_
#define SEQUENCER_TWIPR_SEQUENCER_H_

#include "twipr_control.h"

class TWIPR_CommunicationManager;

typedef struct twipr_sequencer_config_t {

	TWIPR_ControlManager *control;
	TWIPR_CommunicationManager* comm;

} twipr_sequencer_config_t;

typedef enum twipr_sequencer_mode_t {
	TWIPR_SEQUENCER_MODE_IDLE = 0, TWIPR_SEQUENCER_MODE_RUNNING = 1,
} twipr_sequencer_mode_t;


typedef struct twipr_sequencer_sequence_data_t {
	uint16_t sequence_id; // ID of the sequence
	uint16_t length; // Number of samples
	bool require_control_mode; // true: Control mode has to be set in advance. false: Sequencer sets control mode
	uint16_t wait_time_beginning; // Wait time in ticks before starting sequence
	uint16_t wait_time_end; // Time in ticks after sequence
	twipr_control_mode_t control_mode; // Control mode in which the sequence is run
	twipr_control_mode_t control_mode_end; // Control mode to witch to after the sequence
} twipr_sequencer_sequence_data_t;

typedef enum twipr_sequencer_callback_id_t {
	TWIPR_SEQUENCER_CALLBACK_SEQUENCE_STARTED = 1,
	TWIPR_SEQUENCER_CALLBACK_SEQUENCE_FINISHED = 2,
	TWIPR_SEQUENCER_CALLBACK_SEQUENCE_ABORTED = 3,
}twipr_sequencer_callback_id_t;

typedef struct twipr_sequence_input_t {
	uint32_t step;
	float u_1;
	float u_2;
} twipr_sequence_input_t;


typedef struct twipr_sequencer_sample_t {
	uint16_t sequence_id;
	uint32_t sequence_tick;
} twipr_sequencer_sample_t;


//typedef struct twipr_sequencer_reg_entries_t {
//	core_utils_RegisterFunction<void, twipr_sequencer_sequence_data_t> regf_load_sequence;
//	core_utils_RegisterFunction<void, void> regf_stop_sequence;
//	core_utils_RegisterFunction<void, void> regf_start_sequence;
//} twipr_sequencer_reg_entries_t;


typedef struct twipr_sequencer_callbacks_t {
	core_utils_Callback<void, uint16_t> started;
	core_utils_Callback<void, uint16_t> finished;
	core_utils_Callback<void, uint16_t> aborted;
} twipr_sequencer_callbacks_t;

class TWIPR_Sequencer {
public:
	TWIPR_Sequencer();
	void init(twipr_sequencer_config_t config);
	void start();

	void update();


	void startSequence(uint16_t id);
	void abortSequence();
	void stopSequence();
	void loadSequence(twipr_sequencer_sequence_data_t);
	void resetSequenceData();

	void registerCallback(twipr_sequencer_callback_id_t callback_id,
			core_utils_Callback<void, uint16_t> callback);

	twipr_sequencer_sample_t getSample();


	void spiSequenceReceived_callback(uint16_t length);

	twipr_sequencer_mode_t mode;
	uint32_t sequence_tick;
	twipr_sequencer_config_t config;
	twipr_sequencer_sequence_data_t loaded_sequence;

	twipr_sequence_input_t rx_sequence_buffer[TWIPR_SEQUENCE_BUFFER_SIZE];
	twipr_sequence_input_t sequence_buffer[TWIPR_SEQUENCE_BUFFER_SIZE];

private:


	bool _sequence_received;
	twipr_sequencer_callbacks_t _callbacks;


};

#endif /* SEQUENCER_TWIPR_SEQUENCER_H_ */
