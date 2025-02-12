################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (12.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/libraries/stm32_core_cpp_lib/hardware/UART/core_hardware_UART.cpp 

OBJS += \
./stm32_core_cpp_lib/hardware/UART/core_hardware_UART.o 

CPP_DEPS += \
./stm32_core_cpp_lib/hardware/UART/core_hardware_UART.d 


# Each subdirectory must supply rules for building sources it contributes
stm32_core_cpp_lib/hardware/UART/core_hardware_UART.o: /Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/libraries/stm32_core_cpp_lib/hardware/UART/core_hardware_UART.cpp stm32_core_cpp_lib/hardware/UART/subdir.mk
	arm-none-eabi-g++ "$<" -mcpu=cortex-m7 -std=gnu++14 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32H743xx -DBOARD_REV_4 -DUSE_PWR_LDO_SUPPLY -c -I../Core/Inc -I../Drivers/STM32H7xx_HAL_Driver/Inc -I../Drivers/STM32H7xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32H7xx/Include -I../Drivers/CMSIS/Include -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/libraries/robot-control_std_lib" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/libraries/stm32_core_cpp_lib" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/libraries/stm32_core_cpp_lib/communication/modbus_rtu" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/libraries/stm32_core_cpp_lib/utils" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/libraries/stm32_core_cpp_lib/hardware/UART" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/stm32-mcu-projects/twipr_firmware_project_rev4/Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/stm32-mcu-projects/twipr_firmware_project_rev4/Middlewares/Third_Party/FreeRTOS/Source/include" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/stm32-mcu-projects/twipr_firmware_project_rev4/Middlewares/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM4F" -I../Middlewares/Third_Party/FreeRTOS/Source/include -I../Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2 -I../Middlewares/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM4F -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/libraries/stm32_core_cpp_lib/estimation" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/robot/firmware_v1" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/robot/firmware_v1/communication" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/robot/firmware_v1/communication/messages" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/robot/firmware_v1/communication/modules" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/robot/firmware_v1/control" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/robot/firmware_v1/drive" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/robot/firmware_v1/errors" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/robot/firmware_v1/drive/simplexmotion_motors" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/robot/firmware_v1/estimation" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/robot/firmware_v1/io" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/robot/firmware_v1/logging" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/robot/firmware_v1/model" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/robot/firmware_v1/safety" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/robot/firmware_v1/sequencer" -O0 -ffunction-sections -fdata-sections -fno-exceptions -fno-rtti -fno-use-cxa-atexit -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-stm32_core_cpp_lib-2f-hardware-2f-UART

clean-stm32_core_cpp_lib-2f-hardware-2f-UART:
	-$(RM) ./stm32_core_cpp_lib/hardware/UART/core_hardware_UART.cyclo ./stm32_core_cpp_lib/hardware/UART/core_hardware_UART.d ./stm32_core_cpp_lib/hardware/UART/core_hardware_UART.o ./stm32_core_cpp_lib/hardware/UART/core_hardware_UART.su

.PHONY: clean-stm32_core_cpp_lib-2f-hardware-2f-UART

