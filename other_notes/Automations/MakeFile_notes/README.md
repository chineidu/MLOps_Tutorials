# Make and Makefile

## Table of Content

- [Make and Makefile](#make-and-makefile)
  - [Table of Content](#table-of-content)
  - [Make](#make)
    - [Make: Workflow](#make-workflow)
  - [Makefile](#makefile)
    - [Makefile: Structure](#makefile-structure)
    - [Makefile: Benefits](#makefile-benefits)
  - [Makefile: Syntax](#makefile-syntax)
    - [Makefile: Create Variables](#makefile-create-variables)
    - [Makefile: Create Variable With Output](#makefile-create-variable-with-output)
    - [Makefile: Create Target](#makefile-create-target)
      - [Makefile: Display Output W/O Showing The Command](#makefile-display-output-wo-showing-the-command)
    - [Makefile: Create Dependencies](#makefile-create-dependencies)
    - [Makefile: If Statement](#makefile-if-statement)
    - [Makefile: `.PHONY`](#makefile-phony)
    - [Include Keyword](#include-keyword)
    - [Access Environment Variables Loaded From A File](#access-environment-variables-loaded-from-a-file)
    - [Run A Specific Makefile](#run-a-specific-makefile)

## Make

- `make` is a build automation tool.
- It simplifies the process of compiling source code into executable programs or libraries.

### Make: Workflow

- You provide instructions in a special file called a Makefile.
- `make` reads the Makefile and understands the relationships between different files (source code, header files, etc).
- It determines which files need to be recompiled based on their modification times.
make executes the necessary commands (like compilers) to rebuild only the outdated parts, saving time and effort.

## Makefile

- A `Makefile` is a text file containing instructions for make.

### Makefile: Structure

- **Rules**:  It defines `rules` (targets and prerequisites).
  - A `target` is typically the final executable or library you want to build.
  - `Prerequisites` are the source files and other dependencies needed to create the target.

- **Commands**: `commands` specify the exact actions make should take to build the target, like using compilers or linking libraries.

### Makefile: Benefits

- Makefiles promote efficiency by rebuilding only what's necessary.
- They improve maintainability by keeping build instructions centralized and easy to modify.

## Makefile: Syntax

### Makefile: Create Variables

```makefile
# Create variables
ENV_NAME = "dev"
ENV_NAME := "dev" # Set a default value if the variable does not exist.
PASSWORD = "password"
```

### Makefile: Create Variable With Output

```makefile
# Create a variable with an output
LS_OUTPUT = $(shell ls -al)
```

### Makefile: Create Target

- It displays the output and the command.

```makefile
# Create a target
say-hello:
    echo "Hello !!!"
```

- Usage:

```sh
make say-hello

# Output
# echo "Hello !!!"
# Hello !!!
```

#### Makefile: Display Output W/O Showing The Command

- This can be done by adding `@`.

```makefile
# Create a target
say-hello:
    @echo "Hello !!!"
```

- Usage:

```sh
make say-hello

# Output
# Hello !!!
```

### Makefile: Create Dependencies

- In the example below, `say-bye` depends on `say-hello` and `display-ls`.

```makefile
# Create a variable with an output
LS_OUTPUT = $(shell ls)

# Create a target
say-hello:
    @echo "Hello !!!"

display-ls:
    @echo "ls-content: ${LS_OUTPUT}"

# Add dependencies
say-bye: say-hello display-ls
   @echo "Thank you for coming. Bye!"
```

```sh
make say-bye

# Output
# Hello !!!
# ls-content: Makefile README.md
# Thank you for coming. Bye!
```

### Makefile: If Statement

- `ifeq`: if equal to.
- `ifneq`: if NOT equal to.
- Note: It has to be located at the top of the file. i.e. before the targets/dependencies.

```makefile
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
```

```sh
make if-example

# Output
# This is a dev environment!
```

### Makefile: `.PHONY`

- `.PHONY` target in a Makefile is a way to declare that a target is not associated with a real file, but rather a command or set of commands to be executed.
- This helps avoid conflicts and improves the performance of the build process.

```makefile
# Declaring a "clean" target as phony
.PHONY: clean
clean:
    rm -rf *.o *.exe
```

### Include Keyword

- This is used to include files, directories.

```makefile
include dependencies.mk
include my_envs_dir/.env
export # export the env vars
```

### Access Environment Variables Loaded From A File

```makefile
flower:
  # Load environment variables stored in .env
  @set -a && . ./.env && set +a && \
  echo "Running Celery flower..."
  @bash -c "uv run celery -A src.celery.app flower --basic_auth=$$CELERY_FLOWER_USER:$$CELERY_FLOWER_PASSWORD"
```

### Run A Specific Makefile

- You you have more than one makefiles. e.g. `Makefile` and `Makefile.prod`, to run the targets in `Makefile.prod`, run:

```sh
make -f <makefile_name> <target_name>

# e.g.
make -f Makefile.prod if-example
```
