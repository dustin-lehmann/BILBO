################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (12.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
S_SRCS += \
../Core/Startup/startup_stm32h743vitx.s 

S_DEPS += \
./Core/Startup/startup_stm32h743vitx.d 

OBJS += \
./Core/Startup/startup_stm32h743vitx.o 


# Each subdirectory must supply rules for building sources it contributes
Core/Startup/%.o: ../Core/Startup/%.s Core/Startup/subdir.mk
	arm-none-eabi-gcc -mcpu=cortex-m7 -g3 -DDEBUG -DBOARD_REV_4 -c -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/libraries/robot-control_std_lib" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/libraries/stm32_core_cpp_lib" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/libraries/stm32_core_cpp_lib/communication/modbus_rtu" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/libraries/stm32_core_cpp_lib/utils" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/libraries/stm32_core_cpp_lib/hardware/UART" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/stm32-mcu-projects/twipr_firmware_project_rev4/Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/stm32-mcu-projects/twipr_firmware_project_rev4/Middlewares/Third_Party/FreeRTOS/Source/include" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/stm32-mcu-projects/twipr_firmware_project_rev4/Middlewares/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM4F" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/libraries/stm32_core_cpp_lib/estimation" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/robot/firmware_v1" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/robot/firmware_v1/communication" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/robot/firmware_v1/communication/messages" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/robot/firmware_v1/communication/modules" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/robot/firmware_v1/control" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/robot/firmware_v1/drive" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/robot/firmware_v1/errors" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/robot/firmware_v1/drive/simplexmotion_motors" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/robot/firmware_v1/estimation" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/robot/firmware_v1/io" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/robot/firmware_v1/logging" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/robot/firmware_v1/model" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/robot/firmware_v1/safety" -I"/Users/lehmann/work_dir/work_dir/projects/testbed/robots/BILBO/software/robot/firmware/robot/firmware_v1/sequencer" -x assembler-with-cpp -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -o "$@" "$<"

clean: clean-Core-2f-Startup

clean-Core-2f-Startup:
	-$(RM) ./Core/Startup/startup_stm32h743vitx.d ./Core/Startup/startup_stm32h743vitx.o

.PHONY: clean-Core-2f-Startup

