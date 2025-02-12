################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (12.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
../firmware/adc/adc.cpp 

OBJS += \
./firmware/adc/adc.o 

CPP_DEPS += \
./firmware/adc/adc.d 


# Each subdirectory must supply rules for building sources it contributes
firmware/adc/%.o firmware/adc/%.su firmware/adc/%.cyclo: ../firmware/adc/%.cpp firmware/adc/subdir.mk
	arm-none-eabi-g++ "$<" -mcpu=cortex-m4 -std=gnu++14 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32L432xx -c -I../Core/Inc -I../Drivers/STM32L4xx_HAL_Driver/Inc -I../Drivers/STM32L4xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32L4xx/Include -I../Drivers/CMSIS/Include -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/boards/bms/BMS_v3/firmware/i2c" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/boards/bms/BMS_v3/firmware" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/boards/bms/BMS_v3/firmware/utils" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/boards/bms/BMS_v3/firmware/adc" -O0 -ffunction-sections -fdata-sections -fno-exceptions -fno-rtti -fno-use-cxa-atexit -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-firmware-2f-adc

clean-firmware-2f-adc:
	-$(RM) ./firmware/adc/adc.cyclo ./firmware/adc/adc.d ./firmware/adc/adc.o ./firmware/adc/adc.su

.PHONY: clean-firmware-2f-adc

