################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (12.3.rel1)
################################################################################

-include ../makefile.init

RM := rm -rf

# All of the sources participating in the build are defined here
-include sources.mk
-include stm32_core_cpp_lib/utils/subdir.mk
-include stm32_core_cpp_lib/sensors/IMU/subdir.mk
-include stm32_core_cpp_lib/sensors/AMT22/subdir.mk
-include stm32_core_cpp_lib/memory/fram/subdir.mk
-include stm32_core_cpp_lib/memory/eeprom/subdir.mk
-include stm32_core_cpp_lib/hardware/board_hardware/subdir.mk
-include stm32_core_cpp_lib/hardware/UART/subdir.mk
-include stm32_core_cpp_lib/hardware/SPI/subdir.mk
-include stm32_core_cpp_lib/hardware/RS485/subdir.mk
-include stm32_core_cpp_lib/hardware/PWM/subdir.mk
-include stm32_core_cpp_lib/hardware/LED/subdir.mk
-include stm32_core_cpp_lib/hardware/ENCODER/subdir.mk
-include stm32_core_cpp_lib/hardware/BUTTON/subdir.mk
-include stm32_core_cpp_lib/ext/madgwick_ahrs/subdir.mk
-include stm32_core_cpp_lib/estimation/subdir.mk
-include stm32_core_cpp_lib/control/state_feedback/subdir.mk
-include stm32_core_cpp_lib/control/pid/subdir.mk
-include stm32_core_cpp_lib/communication/uart_interface/subdir.mk
-include stm32_core_cpp_lib/communication/modbus_rtu/subdir.mk
-include stm32_core_cpp_lib/communication/can/subdir.mk
-include robot-control_std_lib/subdir.mk
-include firmware/sequencer/subdir.mk
-include firmware/safety/subdir.mk
-include firmware/model/subdir.mk
-include firmware/logging/subdir.mk
-include firmware/estimation/subdir.mk
-include firmware/errors/subdir.mk
-include firmware/drive/simplexmotion_motors/subdir.mk
-include firmware/drive/subdir.mk
-include firmware/control/subdir.mk
-include firmware/communication/modules/subdir.mk
-include firmware/communication/messages/subdir.mk
-include firmware/communication/subdir.mk
-include firmware/subdir.mk
-include Middlewares/Third_Party/FreeRTOS/Source/portable/MemMang/subdir.mk
-include Middlewares/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM4F/subdir.mk
-include Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2/subdir.mk
-include Middlewares/Third_Party/FreeRTOS/Source/subdir.mk
-include Drivers/STM32H7xx_HAL_Driver/Src/subdir.mk
-include Core/Startup/subdir.mk
-include Core/Src/subdir.mk
-include objects.mk

ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(CC_DEPS)),)
-include $(CC_DEPS)
endif
ifneq ($(strip $(C++_DEPS)),)
-include $(C++_DEPS)
endif
ifneq ($(strip $(CCM_DEPS)),)
-include $(CCM_DEPS)
endif
ifneq ($(strip $(C_UPPER_DEPS)),)
-include $(C_UPPER_DEPS)
endif
ifneq ($(strip $(CXX_DEPS)),)
-include $(CXX_DEPS)
endif
ifneq ($(strip $(S_DEPS)),)
-include $(S_DEPS)
endif
ifneq ($(strip $(S_UPPER_DEPS)),)
-include $(S_UPPER_DEPS)
endif
ifneq ($(strip $(CXXM_DEPS)),)
-include $(CXXM_DEPS)
endif
ifneq ($(strip $(C++M_DEPS)),)
-include $(C++M_DEPS)
endif
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
ifneq ($(strip $(CPP_DEPS)),)
-include $(CPP_DEPS)
endif
endif

-include ../makefile.defs

OPTIONAL_TOOL_DEPS := \
$(wildcard ../makefile.defs) \
$(wildcard ../makefile.init) \
$(wildcard ../makefile.targets) \


BUILD_ARTIFACT_NAME := RC_v4_H743_TWIPR_24062024
BUILD_ARTIFACT_EXTENSION := elf
BUILD_ARTIFACT_PREFIX :=
BUILD_ARTIFACT := $(BUILD_ARTIFACT_PREFIX)$(BUILD_ARTIFACT_NAME)$(if $(BUILD_ARTIFACT_EXTENSION),.$(BUILD_ARTIFACT_EXTENSION),)

# Add inputs and outputs from these tool invocations to the build variables 
EXECUTABLES += \
RC_v4_H743_TWIPR_24062024.elf \

MAP_FILES += \
RC_v4_H743_TWIPR_24062024.map \

SIZE_OUTPUT += \
default.size.stdout \

OBJDUMP_LIST += \
RC_v4_H743_TWIPR_24062024.list \

OBJCOPY_HEX += \
RC_v4_H743_TWIPR_24062024.hex \


# All Target
all: main-build

# Main-build Target
main-build: RC_v4_H743_TWIPR_24062024.elf secondary-outputs

# Tool invocations
RC_v4_H743_TWIPR_24062024.elf RC_v4_H743_TWIPR_24062024.map: $(OBJS) $(USER_OBJS) J:\work_dir\work_dir\projects\testbed\robots\TWIPR\software\robot\firmware\stm32-mcu-projects\twipr_firmware_project_rev4\STM32H743VITX_FLASH.ld makefile objects.list $(OPTIONAL_TOOL_DEPS)
	arm-none-eabi-g++ -o "RC_v4_H743_TWIPR_24062024.elf" @"objects.list" $(USER_OBJS) $(LIBS) -mcpu=cortex-m7 -T"J:\work_dir\work_dir\projects\testbed\robots\TWIPR\software\robot\firmware\stm32-mcu-projects\twipr_firmware_project_rev4\STM32H743VITX_FLASH.ld" --specs=nosys.specs -Wl,-Map="RC_v4_H743_TWIPR_24062024.map" -Wl,--gc-sections -static --specs=nano.specs -mfpu=fpv5-d16 -mfloat-abi=hard -mthumb -u _printf_float -Wl,--start-group -lc -lm -lstdc++ -lsupc++ -Wl,--end-group
	@echo 'Finished building target: $@'
	@echo ' '

default.size.stdout: $(EXECUTABLES) makefile objects.list $(OPTIONAL_TOOL_DEPS)
	arm-none-eabi-size  $(EXECUTABLES)
	@echo 'Finished building: $@'
	@echo ' '

RC_v4_H743_TWIPR_24062024.list: $(EXECUTABLES) makefile objects.list $(OPTIONAL_TOOL_DEPS)
	arm-none-eabi-objdump -h -S $(EXECUTABLES) > "RC_v4_H743_TWIPR_24062024.list"
	@echo 'Finished building: $@'
	@echo ' '

RC_v4_H743_TWIPR_24062024.hex: $(EXECUTABLES) makefile objects.list $(OPTIONAL_TOOL_DEPS)
	arm-none-eabi-objcopy  -O ihex $(EXECUTABLES) "RC_v4_H743_TWIPR_24062024.hex"
	@echo 'Finished building: $@'
	@echo ' '

# Other Targets
clean:
	-$(RM) RC_v4_H743_TWIPR_24062024.elf RC_v4_H743_TWIPR_24062024.hex RC_v4_H743_TWIPR_24062024.list RC_v4_H743_TWIPR_24062024.map default.size.stdout
	-@echo ' '

secondary-outputs: $(SIZE_OUTPUT) $(OBJDUMP_LIST) $(OBJCOPY_HEX)

fail-specified-linker-script-missing:
	@echo 'Error: Cannot find the specified linker script. Check the linker settings in the build configuration.'
	@exit 2

warn-no-linker-script-specified:
	@echo 'Warning: No linker script specified. Check the linker settings in the build configuration.'

.PHONY: all clean dependents main-build fail-specified-linker-script-missing warn-no-linker-script-specified

-include ../makefile.targets
