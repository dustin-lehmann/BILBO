################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (12.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2/cmsis_os2.c 

C_DEPS += \
./Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2/cmsis_os2.d 

OBJS += \
./Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2/cmsis_os2.o 


# Each subdirectory must supply rules for building sources it contributes
Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2/%.o Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2/%.su Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2/%.cyclo: ../Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2/%.c Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m7 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32H743xx -DBOARD_REV_4 -c -I../Core/Inc -I../Drivers/STM32H7xx_HAL_Driver/Inc -I../Drivers/STM32H7xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32H7xx/Include -I../Drivers/CMSIS/Include -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/libraries/robot-control_std_lib" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/libraries/stm32_core_cpp_lib" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/libraries/stm32_core_cpp_lib/communication/modbus_rtu" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/estimation" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/control" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/communication" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/drive" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/errors" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/logging" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/communication/modules" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/communication/messages" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/libraries/stm32_core_cpp_lib/utils" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/libraries/stm32_core_cpp_lib/hardware/UART" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/stm32-mcu-projects/twipr_firmware_project_rev4/Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/stm32-mcu-projects/twipr_firmware_project_rev4/Middlewares/Third_Party/FreeRTOS/Source/include" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/stm32-mcu-projects/twipr_firmware_project_rev4/Middlewares/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM4F" -I../Middlewares/Third_Party/FreeRTOS/Source/include -I../Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2 -I../Middlewares/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM4F -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/safety" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/libraries/stm32_core_cpp_lib/estimation" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/sequencer" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/model" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/drive/simplexmotion_motors" -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Middlewares-2f-Third_Party-2f-FreeRTOS-2f-Source-2f-CMSIS_RTOS_V2

clean-Middlewares-2f-Third_Party-2f-FreeRTOS-2f-Source-2f-CMSIS_RTOS_V2:
	-$(RM) ./Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2/cmsis_os2.cyclo ./Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2/cmsis_os2.d ./Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2/cmsis_os2.o ./Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2/cmsis_os2.su

.PHONY: clean-Middlewares-2f-Third_Party-2f-FreeRTOS-2f-Source-2f-CMSIS_RTOS_V2
