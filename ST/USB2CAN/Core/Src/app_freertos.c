/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * File Name          : app_freertos.c
  * Description        : Code for freertos applications
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

/* Includes ------------------------------------------------------------------*/
#include "FreeRTOS.h"
#include "task.h"
#include "main.h"
#include "cmsis_os.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
/* USER CODE BEGIN Variables */

/* USER CODE END Variables */
osThreadId TaskCANHandle;
osThreadId TaskUSBHandle;
osThreadId TaskSUPERVISORHandle;

/* Private function prototypes -----------------------------------------------*/
/* USER CODE BEGIN FunctionPrototypes */

/* USER CODE END FunctionPrototypes */

void StartTaskCAN(void const * argument);
void StartTaskUSB(void const * argument);
void StartTaskSUPERVISOR(void const * argument);

void MX_FREERTOS_Init(void); /* (MISRA C 2004 rule 8.1) */

/**
  * @brief  FreeRTOS initialization
  * @param  None
  * @retval None
  */
void MX_FREERTOS_Init(void) {
  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* USER CODE BEGIN RTOS_MUTEX */
  /* add mutexes, ... */
  /* USER CODE END RTOS_MUTEX */

  /* USER CODE BEGIN RTOS_SEMAPHORES */
  /* add semaphores, ... */
  /* USER CODE END RTOS_SEMAPHORES */

  /* USER CODE BEGIN RTOS_TIMERS */
  /* start timers, add new ones, ... */
  /* USER CODE END RTOS_TIMERS */

  /* USER CODE BEGIN RTOS_QUEUES */
  /* add queues, ... */
  /* USER CODE END RTOS_QUEUES */

  /* Create the thread(s) */
  /* definition and creation of TaskCAN */
  osThreadDef(TaskCAN, StartTaskCAN, osPriorityNormal, 0, 128);
  TaskCANHandle = osThreadCreate(osThread(TaskCAN), NULL);

  /* definition and creation of TaskUSB */
  osThreadDef(TaskUSB, StartTaskUSB, osPriorityIdle, 0, 128);
  TaskUSBHandle = osThreadCreate(osThread(TaskUSB), NULL);

  /* definition and creation of TaskSUPERVISOR */
  osThreadDef(TaskSUPERVISOR, StartTaskSUPERVISOR, osPriorityIdle, 0, 128);
  TaskSUPERVISORHandle = osThreadCreate(osThread(TaskSUPERVISOR), NULL);

  /* USER CODE BEGIN RTOS_THREADS */
  /* add threads, ... */
  /* USER CODE END RTOS_THREADS */

}

/* USER CODE BEGIN Header_StartTaskCAN */
/**
  * @brief  Function implementing the TaskCAN thread.
  * @param  argument: Not used
  * @retval None
  */
/* USER CODE END Header_StartTaskCAN */
void StartTaskCAN(void const * argument)
{
  /* init code for USB_Device */
  MX_USB_Device_Init();
  /* USER CODE BEGIN StartTaskCAN */
  /* Infinite loop */
  for(;;)
  {
    osDelay(1);
  }
  /* USER CODE END StartTaskCAN */
}

/* USER CODE BEGIN Header_StartTaskUSB */
/**
* @brief Function implementing the TaskUSB thread.
* @param argument: Not used
* @retval None
*/
/* USER CODE END Header_StartTaskUSB */
void StartTaskUSB(void const * argument)
{
  /* USER CODE BEGIN StartTaskUSB */
  /* Infinite loop */
  for(;;)
  {
    osDelay(1);
  }
  /* USER CODE END StartTaskUSB */
}

/* USER CODE BEGIN Header_StartTaskSUPERVISOR */
/**
* @brief Function implementing the TaskSUPERVISOR thread.
* @param argument: Not used
* @retval None
*/
/* USER CODE END Header_StartTaskSUPERVISOR */
void StartTaskSUPERVISOR(void const * argument)
{
  /* USER CODE BEGIN StartTaskSUPERVISOR */
  /* Infinite loop */
  for(;;)
  {
    osDelay(1);
  }
  /* USER CODE END StartTaskSUPERVISOR */
}

/* Private application code --------------------------------------------------*/
/* USER CODE BEGIN Application */

/* USER CODE END Application */

