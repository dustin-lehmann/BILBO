################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (12.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
S_SRCS += \
../Core/Startup/startup_stm32l431ccux.s 

S_DEPS += \
./Core/Startup/startup_stm32l431ccux.d 

OBJS += \
./Core/Startup/startup_stm32l431ccux.o 


# Each subdirectory must supply rules for building sources it contributes
Core/Startup/%.o: ../Core/Startup/%.s Core/Startup/subdir.mk
	arm-none-eabi-gcc -mcpu=cortex-m4 -g3 -DDEBUG -c -I"J:/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/boards/control-board/v4/RC_v4_BoardExtender/firmware/neopixel" -I"J:/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/boards/control-board/v4/RC_v4_BoardExtender/firmware/utils" -I"J:/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/boards/control-board/v4/RC_v4_BoardExtender/firmware/led" -I"J:/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/boards/control-board/v4/RC_v4_BoardExtender/firmware/i2c" -I"J:/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/boards/control-board/v4/RC_v4_BoardExtender/firmware/eeprom" -I"J:/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/boards/control-board/v4/RC_v4_BoardExtender/firmware/callbacks" -I"J:/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/boards/control-board/v4/RC_v4_BoardExtender/firmware/buzzer" -I"J:/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/boards/control-board/v4/RC_v4_BoardExtender/firmware" -x assembler-with-cpp -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@" "$<"

clean: clean-Core-2f-Startup

clean-Core-2f-Startup:
	-$(RM) ./Core/Startup/startup_stm32l431ccux.d ./Core/Startup/startup_stm32l431ccux.o

.PHONY: clean-Core-2f-Startup

