################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (12.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/libraries/robot-control_std_lib/robot-control_extender.cpp \
J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/libraries/robot-control_std_lib/robot-control_indicators.cpp \
J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/libraries/robot-control_std_lib/robot-control_std.cpp 

OBJS += \
./robot-control_std_lib/robot-control_extender.o \
./robot-control_std_lib/robot-control_indicators.o \
./robot-control_std_lib/robot-control_std.o 

CPP_DEPS += \
./robot-control_std_lib/robot-control_extender.d \
./robot-control_std_lib/robot-control_indicators.d \
./robot-control_std_lib/robot-control_std.d 


# Each subdirectory must supply rules for building sources it contributes
robot-control_std_lib/robot-control_extender.o: J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/libraries/robot-control_std_lib/robot-control_extender.cpp robot-control_std_lib/subdir.mk
	arm-none-eabi-g++ "$<" -mcpu=cortex-m7 -std=gnu++14 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32H743xx -DBOARD_REV_4 -c -I../Core/Inc -I../Drivers/STM32H7xx_HAL_Driver/Inc -I../Drivers/STM32H7xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32H7xx/Include -I../Drivers/CMSIS/Include -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/libraries/robot-control_std_lib" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/libraries/stm32_core_cpp_lib" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/libraries/stm32_core_cpp_lib/communication/modbus_rtu" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/estimation" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/control" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/communication" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/drive" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/errors" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/logging" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/communication/modules" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/communication/messages" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/libraries/stm32_core_cpp_lib/utils" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/libraries/stm32_core_cpp_lib/hardware/UART" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/stm32-mcu-projects/twipr_firmware_project_rev4/Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/stm32-mcu-projects/twipr_firmware_project_rev4/Middlewares/Third_Party/FreeRTOS/Source/include" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/stm32-mcu-projects/twipr_firmware_project_rev4/Middlewares/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM4F" -I../Middlewares/Third_Party/FreeRTOS/Source/include -I../Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2 -I../Middlewares/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM4F -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/safety" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/libraries/stm32_core_cpp_lib/estimation" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/sequencer" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/model" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/drive/simplexmotion_motors" -O0 -ffunction-sections -fdata-sections -fno-exceptions -fno-rtti -fno-use-cxa-atexit -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"
robot-control_std_lib/robot-control_indicators.o: J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/libraries/robot-control_std_lib/robot-control_indicators.cpp robot-control_std_lib/subdir.mk
	arm-none-eabi-g++ "$<" -mcpu=cortex-m7 -std=gnu++14 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32H743xx -DBOARD_REV_4 -c -I../Core/Inc -I../Drivers/STM32H7xx_HAL_Driver/Inc -I../Drivers/STM32H7xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32H7xx/Include -I../Drivers/CMSIS/Include -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/libraries/robot-control_std_lib" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/libraries/stm32_core_cpp_lib" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/libraries/stm32_core_cpp_lib/communication/modbus_rtu" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/estimation" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/control" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/communication" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/drive" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/errors" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/logging" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/communication/modules" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/communication/messages" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/libraries/stm32_core_cpp_lib/utils" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/libraries/stm32_core_cpp_lib/hardware/UART" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/stm32-mcu-projects/twipr_firmware_project_rev4/Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/stm32-mcu-projects/twipr_firmware_project_rev4/Middlewares/Third_Party/FreeRTOS/Source/include" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/stm32-mcu-projects/twipr_firmware_project_rev4/Middlewares/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM4F" -I../Middlewares/Third_Party/FreeRTOS/Source/include -I../Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2 -I../Middlewares/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM4F -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/safety" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/libraries/stm32_core_cpp_lib/estimation" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/sequencer" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/model" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/drive/simplexmotion_motors" -O0 -ffunction-sections -fdata-sections -fno-exceptions -fno-rtti -fno-use-cxa-atexit -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"
robot-control_std_lib/robot-control_std.o: J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/libraries/robot-control_std_lib/robot-control_std.cpp robot-control_std_lib/subdir.mk
	arm-none-eabi-g++ "$<" -mcpu=cortex-m7 -std=gnu++14 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32H743xx -DBOARD_REV_4 -c -I../Core/Inc -I../Drivers/STM32H7xx_HAL_Driver/Inc -I../Drivers/STM32H7xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32H7xx/Include -I../Drivers/CMSIS/Include -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/libraries/robot-control_std_lib" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/libraries/stm32_core_cpp_lib" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/libraries/stm32_core_cpp_lib/communication/modbus_rtu" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/estimation" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/control" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/communication" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/drive" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/errors" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/logging" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/communication/modules" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/communication/messages" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/libraries/stm32_core_cpp_lib/utils" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/libraries/stm32_core_cpp_lib/hardware/UART" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/stm32-mcu-projects/twipr_firmware_project_rev4/Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/stm32-mcu-projects/twipr_firmware_project_rev4/Middlewares/Third_Party/FreeRTOS/Source/include" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/stm32-mcu-projects/twipr_firmware_project_rev4/Middlewares/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM4F" -I../Middlewares/Third_Party/FreeRTOS/Source/include -I../Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2 -I../Middlewares/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM4F -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/safety" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/libraries/stm32_core_cpp_lib/estimation" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/sequencer" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/model" -I"J:/work_dir/work_dir/projects/testbed/robots/TWIPR/software/robot/firmware/robot/firmware_v1/drive/simplexmotion_motors" -O0 -ffunction-sections -fdata-sections -fno-exceptions -fno-rtti -fno-use-cxa-atexit -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-robot-2d-control_std_lib

clean-robot-2d-control_std_lib:
	-$(RM) ./robot-control_std_lib/robot-control_extender.cyclo ./robot-control_std_lib/robot-control_extender.d ./robot-control_std_lib/robot-control_extender.o ./robot-control_std_lib/robot-control_extender.su ./robot-control_std_lib/robot-control_indicators.cyclo ./robot-control_std_lib/robot-control_indicators.d ./robot-control_std_lib/robot-control_indicators.o ./robot-control_std_lib/robot-control_indicators.su ./robot-control_std_lib/robot-control_std.cyclo ./robot-control_std_lib/robot-control_std.d ./robot-control_std_lib/robot-control_std.o ./robot-control_std_lib/robot-control_std.su

.PHONY: clean-robot-2d-control_std_lib
