################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (11.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
../firmware/i2c/i2c_slave.cpp 

OBJS += \
./firmware/i2c/i2c_slave.o 

CPP_DEPS += \
./firmware/i2c/i2c_slave.d 


# Each subdirectory must supply rules for building sources it contributes
firmware/i2c/%.o firmware/i2c/%.su firmware/i2c/%.cyclo: ../firmware/i2c/%.cpp firmware/i2c/subdir.mk
	arm-none-eabi-g++ "$<" -mcpu=cortex-m0plus -std=gnu++14 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32G031xx -c -I../Core/Inc -I../Drivers/STM32G0xx_HAL_Driver/Inc -I../Drivers/STM32G0xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32G0xx/Include -I../Drivers/CMSIS/Include -I"C:/work_dir/projects/testbed/software/robots/software_board/board_manager_mcu/rc_board-extender_firmware/firmware/neopixel" -I"C:/work_dir/projects/testbed/software/robots/software_board/board_manager_mcu/rc_board-extender_firmware/firmware" -I"C:/work_dir/projects/testbed/software/robots/software_board/board_manager_mcu/rc_board-extender_firmware/firmware/buzzer" -I"C:/work_dir/projects/testbed/software/robots/software_board/board_manager_mcu/rc_board-extender_firmware/firmware/led" -I"C:/work_dir/projects/testbed/software/robots/software_board/board_manager_mcu/rc_board-extender_firmware/firmware/utils" -I"C:/work_dir/projects/testbed/software/robots/software_board/board_manager_mcu/rc_board-extender_firmware/firmware/eeprom" -I"C:/work_dir/projects/testbed/software/robots/software_board/board_manager_mcu/rc_board-extender_firmware/firmware/i2c" -I"C:/work_dir/projects/testbed/software/robots/software_board/board_manager_mcu/rc_board-extender_firmware/firmware/callbacks" -O0 -ffunction-sections -fdata-sections -fno-exceptions -fno-rtti -fno-use-cxa-atexit -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"

clean: clean-firmware-2f-i2c

clean-firmware-2f-i2c:
	-$(RM) ./firmware/i2c/i2c_slave.cyclo ./firmware/i2c/i2c_slave.d ./firmware/i2c/i2c_slave.o ./firmware/i2c/i2c_slave.su

.PHONY: clean-firmware-2f-i2c

