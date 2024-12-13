################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (11.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
../firmware/neopixel/old/ws2812.cpp 

OBJS += \
./firmware/neopixel/old/ws2812.o 

CPP_DEPS += \
./firmware/neopixel/old/ws2812.d 


# Each subdirectory must supply rules for building sources it contributes
firmware/neopixel/old/%.o firmware/neopixel/old/%.su firmware/neopixel/old/%.cyclo: ../firmware/neopixel/old/%.cpp firmware/neopixel/old/subdir.mk
	arm-none-eabi-g++ "$<" -mcpu=cortex-m4 -std=gnu++14 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32L431xx -c -I../Core/Inc -I../Drivers/STM32L4xx_HAL_Driver/Inc -I../Drivers/STM32L4xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32L4xx/Include -I../Drivers/CMSIS/Include -O0 -ffunction-sections -fdata-sections -fno-exceptions -fno-rtti -fno-use-cxa-atexit -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-firmware-2f-neopixel-2f-old

clean-firmware-2f-neopixel-2f-old:
	-$(RM) ./firmware/neopixel/old/ws2812.cyclo ./firmware/neopixel/old/ws2812.d ./firmware/neopixel/old/ws2812.o ./firmware/neopixel/old/ws2812.su

.PHONY: clean-firmware-2f-neopixel-2f-old

