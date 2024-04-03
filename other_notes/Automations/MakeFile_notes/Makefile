# Create variable(s)
ENV_NAME := "dev"
PASSWORD = "password"

# Create a variable with an output
LS_OUTPUT = $(shell ls)

ifeq (${ENV_NAME}, "dev")
	RESULT = "This is a dev environment!"
else
	RESULT = "This is NOT a dev environment!"
endif

# Create a target
say-hello:
	@echo "Hello !!!"

display-ls:
	@echo "ls-content: ${LS_OUTPUT}"

# Add a dependency
say-bye: say-hello display-ls
	@echo "Thank you for coming. Bye!"

if-example:
	@echo "${RESULT}"
