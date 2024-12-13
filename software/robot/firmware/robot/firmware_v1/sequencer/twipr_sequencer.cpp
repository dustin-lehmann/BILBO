/*
 * twipr_sequencer.cpp
 *
 *  Created on: Nov 20, 2024
 *      Author: Dustin Lehmann
 */

#include "twipr_sequencer.h"
#include "twipr_communication.h"
#include "robot-control_std.h"

TWIPR_Sequencer::TWIPR_Sequencer() {

}
/* =============================================================== */
void TWIPR_Sequencer::init(twipr_sequencer_config_t config) {
	this->config = config;
	this->sequence_tick = 0;
	this->mode = TWIPR_SEQUENCER_MODE_IDLE;

	this->config.comm->registerCallback(TWIPR_COMM_CALLBACK_NEW_TRAJECTORY,
			core_utils_Callback<void, uint16_t>(this,
					&TWIPR_Sequencer::spiSequenceReceived_callback));
}
/* =============================================================== */
void TWIPR_Sequencer::start() {

}

/* ======================================================== */
void TWIPR_Sequencer::registerCallback(
		twipr_sequencer_callback_id_t callback_id,
		core_utils_Callback<void, uint16_t> callback) {
	switch (callback_id) {
	case TWIPR_SEQUENCER_CALLBACK_SEQUENCE_STARTED: {
		this->_callbacks.started = callback;
		break;
	}
	case TWIPR_SEQUENCER_CALLBACK_SEQUENCE_FINISHED: {
		this->_callbacks.finished = callback;
		break;
	}
	case TWIPR_SEQUENCER_CALLBACK_SEQUENCE_ABORTED: {
		this->_callbacks.aborted = callback;
		break;
	}
	}
}
/* =============================================================== */
void TWIPR_Sequencer::update() {

	if (this->mode == TWIPR_SEQUENCER_MODE_IDLE) {
		return;
	}

	// Do the Update

}
/* =============================================================== */
void TWIPR_Sequencer::startSequence(uint16_t id) {
	this->sequence_tick = 0;

	// Check the requirements
	if (!this->_sequence_received){
		return;
	}

	// Check the control mode

	// Check if the loaded sequence has the same id

	this->mode = TWIPR_SEQUENCER_MODE_RUNNING;

	// Disable External Inputs to the controller
	this->config.control->disableExternalInput();

	// Give an audio queue
	rc_buzzer.setConfig(900, 250, 1);
	rc_buzzer.start();

	// Call the callback(s)

	if (this->_callbacks.started.registered) {
		this->_callbacks.started.call((uint16_t) id);
	}
}

/* =============================================================== */
void TWIPR_Sequencer::abortSequence() {

	// TODO: I need to reflect in the sample if the sequence was finished or aborted

	// Enable external inputs to the controller
	this->config.control->enableExternalInput();

	// Set the mode
	this->mode = TWIPR_SEQUENCER_MODE_IDLE;

	// Give an audio queue
	rc_buzzer.setConfig(900, 100, 3);
	rc_buzzer.start();

	//
	if (this->_callbacks.aborted.registered) {
		this->_callbacks.aborted.call(
				(uint16_t) this->loaded_sequence.sequence_id);
	}
}

/* =============================================================== */
void TWIPR_Sequencer::stopSequence() {

	// Enable external inputs to the controller
	this->config.control->enableExternalInput();

	// Set the mode
	this->mode = TWIPR_SEQUENCER_MODE_IDLE;

	// Give an audio queue
	rc_buzzer.setConfig(900, 150, 2);
	rc_buzzer.start();

	//
	if (this->_callbacks.finished.registered) {
		this->_callbacks.finished.call(
				(uint16_t) this->loaded_sequence.sequence_id);
	}
}
/* =============================================================== */
void TWIPR_Sequencer::loadSequence(
		twipr_sequencer_sequence_data_t sequence_data) {
	this->loaded_sequence = sequence_data;
	this->_sequence_received = false;
	this->config.comm->receiveTrajectory();
}
/* =============================================================== */
void TWIPR_Sequencer::resetSequenceData() {

}

/* =============================================================== */
twipr_sequencer_sample_t TWIPR_Sequencer::getSample() {
	twipr_sequencer_sample_t sample;

	if (this->mode == TWIPR_SEQUENCER_MODE_RUNNING) {
		sample.sequence_id = this->loaded_sequence.sequence_id;
		sample.sequence_tick = this->sequence_tick;
	} else {
		sample.sequence_id = 0;
		sample.sequence_tick = 0;
	}

	sample.sequence_id = 2;
	sample.sequence_tick = 3;

	return sample;
}

/* =============================================================== */
void TWIPR_Sequencer::spiSequenceReceived_callback(uint16_t trajectory_length) {
	// Copy the trajectory into the buffer
	memcpy((uint8_t*) this->sequence_buffer,
			(uint8_t*) this->rx_sequence_buffer,
			sizeof(twipr_sequence_input_t) * TWIPR_SEQUENCE_BUFFER_SIZE);

	this->_sequence_received = true;
}
