/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.h
  * @brief          : Header for main.c file.
  *                   This file contains the common defines of the application.
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2022 STMicroelectronics.
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
#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32l4xx_hal.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "firmware_c.h"
/* USER CODE END Includes */

/* Exported types ------------------------------------------------------------*/
/* USER CODE BEGIN ET */

/* USER CODE END ET */

/* Exported constants --------------------------------------------------------*/
/* USER CODE BEGIN EC */

/* USER CODE END EC */

/* Exported macro ------------------------------------------------------------*/
/* USER CODE BEGIN EM */

/* USER CODE END EM */

/* Exported functions prototypes ---------------------------------------------*/
void Error_Handler(void);

/* USER CODE BEGIN EFP */

/* USER CODE END EFP */

/* Private defines -----------------------------------------------------------*/
#define ENABLE_MEAS_1_Pin GPIO_PIN_1
#define ENABLE_MEAS_1_GPIO_Port GPIOA
#define ENABLE_MEAS_3_Pin GPIO_PIN_5
#define ENABLE_MEAS_3_GPIO_Port GPIOA
#define DETECT_CHG_Pin GPIO_PIN_6
#define DETECT_CHG_GPIO_Port GPIOA
#define ENABLE_MEAS_4_Pin GPIO_PIN_1
#define ENABLE_MEAS_4_GPIO_Port GPIOB
#define LED_USER_Pin GPIO_PIN_11
#define LED_USER_GPIO_Port GPIOA
#define OUT_2_Pin GPIO_PIN_3
#define OUT_2_GPIO_Port GPIOB
#define OUT_1_Pin GPIO_PIN_5
#define OUT_1_GPIO_Port GPIOB
#define OUT_3_Pin GPIO_PIN_6
#define OUT_3_GPIO_Port GPIOB
#define OUT_4_Pin GPIO_PIN_7
#define OUT_4_GPIO_Port GPIOB

/* USER CODE BEGIN Private defines */

/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */
