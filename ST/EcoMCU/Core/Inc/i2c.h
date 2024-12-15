/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file    i2c.h
  * @brief   This file contains all the function prototypes for
  *          the i2c.c file
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2024 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __I2C_H__
#define __I2C_H__

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* USER CODE BEGIN Includes */
#include "time.h"
/* USER CODE END Includes */

extern I2C_HandleTypeDef hi2c1;

/* USER CODE BEGIN Private defines */
#define EEPROM_AV_TRIALS 1
#define EEPROM_AV_TIMEOUT 10
#define EEPROM_TIMEOUT 200

#define EEPROM_TEST_ADDR 0x00000000
#define EEPROM_PAGE_SIZE 32


#define EEPROM_READ 0xA1
#define EEPROM_WRITE 0xA0
#define EEPROM_READ_PAGE 0xB1
#define EEPROM_WRITE_PAGE 0xB0

#define EEPROM_VOLTAGE_ADDR 0
#define EEPROM_TEMPERATURE_ADDR 1
#define EEPROM_CURRENT_ADDR 1
#define EEPROM_SOFTWARE_ADDR 3
#define EEPROM_PRECHARGE_ADDR 4


typedef enum {
	VOLTAGE,
	TEMPERATURE,
	CURRENT,
	SOFTWARE,
	PRECHARGE,
} Error_t;

typedef struct ErrorPayload {
	time_t timestamp;
	Error_t error_type;
	uint16_t value;
} ErrorPayload;
/* USER CODE END Private defines */

void MX_I2C1_Init(void);

/* USER CODE BEGIN Prototypes */
HAL_StatusTypeDef test_EEPROM();
void EEPROM_Write_PreCharge(uint8_t *pData, uint16_t Size);
void EEPROM_Write_ErrorTemperature(uint8_t *pData, uint16_t Size);
void EEPROM_Write_ErrorVoltage(uint8_t *pData, uint16_t Size);
void EEPROM_Write_ErrorSoftware(uint8_t *pData, uint16_t Size);
void EEPROM_Write_ErrorPreCharge(uint8_t *pData, uint16_t Size);
void EEPROM_Write_PreCharge(uint8_t *pData, uint16_t Size);
void EEPROM_Read_ErrorTemperature(uint8_t *pData, uint16_t Size);
void EEPROM_Read_ErrorVoltage(uint8_t *pData, uint16_t Size);
void EEPROM_Read_ErrorSoftware(uint8_t *pData, uint16_t Size);
void EEPROM_Read_ErrorPreCharge(uint8_t *pData, uint16_t Size);
/* USER CODE END Prototypes */

#ifdef __cplusplus
}
#endif

#endif /* __I2C_H__ */

