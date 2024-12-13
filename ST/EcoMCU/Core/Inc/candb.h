/*
 * candb.h
 *
 *  Created on: Dec 13, 2024
 *      Author: leona
 */

#ifndef INC_CANDB_H_
#define INC_CANDB_H_

#define MAX_PAYLOAD_SIZE 64
#define MAX_MESSAGES 9

// Struttura per un messaggio CAN FD

typedef enum {
	PRECHARGE_p,
	VOLTAGE_p,
	CURRENT_p,
	RELAY1_p,
	RELAY2_p,
	RELAY3_p,
	RELAY4_p,
	TEMPERATURE_p
} Payload_t;

/*
 * @brief CANFD messages struct def
 */
typedef struct {
    uint32_t id;                   // ID del messaggio
    uint32_t dlc;                  // Lunghezza del payload (DLC)
    Payload_t payload;
} CANFD_Message;

/*
 * @brief CANFD Database struc def
 */
typedef struct {
    const CANFD_Message *messages[MAX_MESSAGES]; // Array di puntatori ai messaggi
    uint32_t numMessages;                        // Numero totale di messaggi
} CANFD_Database;

/*
 * @brief CANFD messages init
 */
const CANFD_Message msg1 = { .id = 0x000002AA,	.dlc = 1,	.payload = PRECHARGE_p		};
const CANFD_Message msg2 = { .id = 0x0000020A,	.dlc = 60,	.payload = VOLTAGE_p		};
const CANFD_Message msg3 = { .id = 0x0000020B,	.dlc = 60,	.payload = CURRENT_p		};
const CANFD_Message msg4 = { .id = 0x0000020C,	.dlc = 60,	.payload = RELAY1_p			};
const CANFD_Message msg5 = { .id = 0x0000020D,	.dlc = 60,	.payload = RELAY2_p			};
const CANFD_Message msg6 = { .id = 0x0000020E,	.dlc = 60,	.payload = RELAY3_p			};
const CANFD_Message msg7 = { .id = 0x0000020F,	.dlc = 60,	.payload = RELAY4_p			};
const CANFD_Message msg8 = { .id = 0x000003AA,	.dlc = 1,	.payload = TEMPERATURE_p	};
const CANFD_Message msg9 = { .id = 0x0000030A,	.dlc = 2,	.payload = TEMPERATURE_p	};

const CANFD_Database CANDB = {
    .messages = {&msg1, &msg2, &msg3, &msg4, &msg5, &msg6, &msg7, &msg8, &msg9},
    .numMessages = 9
};



#endif /* INC_CANDB_H_ */
