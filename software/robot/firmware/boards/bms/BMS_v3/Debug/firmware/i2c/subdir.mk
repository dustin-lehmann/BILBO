################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (12.3.rel1)
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
	arm-none-eabi-g++ "$<" -mcpu=cortex-m4 -std=gnu++14 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32L432xx -c -I../Core/Inc -I../Drivers/STM32L4xx_HAL_Driver/Inc -I../Drivers/STM32L4xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32L4xx/Include -I../Drivers/CMSIS/Include -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/boards/bms/BMS_v3/firmware/i2c" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/boards/bms/BMS_v3/firmware" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/boards/bms/BMS_v3/firmware/utils" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/boards/bms/BMS_v3/firmware/adc" -O0 -ffunction-sections -fdata-sections -fno-exceptions -fno-rtti -fno-use-cxa-atexit -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-firmware-2f-i2c

clean-firmware-2f-i2c:
	-$(RM) ./firmware/i2c/i2c_slave.cyclo ./firmware/i2c/i2c_slave.d ./firmware/i2c/i2c_slave.o ./firmware/i2c/i2c_slave.su

.PHONY: clean-firmware-2f-i2c

