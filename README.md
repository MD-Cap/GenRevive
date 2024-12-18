# GenRevive Migrator - ADF to Spring

This repository is used to migrate an ADF application into a Spring application using [GenRevive](https://devon.s2-eu.capgemini.com/gitlab/cca-genrevive-global/genrevive).

This document provides instructions for setting up the local environment and configuration in order to use this migrator.

If you want to know more about the main architecture of GenRevive, see the [official documentation](https://devon.s2-eu.capgemini.com/gitlab/cca-genrevive-global/genrevive/-/blob/main/docs/genrevive_arc42_documentation.md). If you want to know more about specific activities, look into the activity files. They include helpful comments and explanations on how they work.

## Project Setup Steps

To run the migrator, follow these steps:
1. Clone the [GenRevive](https://devon.s2-eu.capgemini.com/gitlab/cca-genrevive-global/genrevive) repository, which is needed as a dependency to run this migrator. The GenRevive root folder needs to be located in the same folder as the root folder of this repository.
   >**NOTE:** If needed, GenRevive can be located in a different folder. In this case, adjust the path defined in `pyproject.toml`.
2. Install and run Docker. This is always needed, even if the migrator doesn't run in a container, as the Oracle database starts as a container. To avoid licensing costs, Rancher Desktop can be installed on both Windows and macOS, by following the [official documentation](https://docs.rancherdesktop.io/getting-started/installation).
3. Configure the environment as described in the chapter [Configuration](#configuration).

After the initial project setup steps have been done, there are two alternative options to run the migrator - either in a Docker container or locally.

### Running the migrator in a container

This is the fastest way to get started - no local migrator specific installations necessary. The migrator will start as a Docker container and create its output in the local file system.

1. Make sure Docker Compose is installed. If you installed Rancher Desktop, it is already bundled with it and nothing else needs to be installed. If not, follow the official [Docker Compose installation steps](https://docs.docker.com/compose/install/). 
2. Run the migrator by executing:
   ```bash
   docker-compose up
   ```

The first execution will take longer than subsequent executions, because a Docker Image will be created for the migrator. It will remain available locally for further migrator executions.

### Running the migrator locally

Alternatively, the migrator can run locally instead of in a Docker container. In this case, the following installation steps are required:

1. Follow the [Project Setup Guide for GenRevive](https://devon.s2-eu.capgemini.com/gitlab/cca-genrevive-global/genrevive#project-setup-guide) to install most of the tools and dependencies needed for running this migrator.
   >**NOTE:** After installing Poetry, you do not need to call `poetry lock`, `poetry install` and `poetry build` for the `GenRevive` project. It will get built automatically when using this migrator.
2. Set up a virtual environment in the root of this repository, as described in the chapter [Setting up a Virtual Environment](https://devon.s2-eu.capgemini.com/gitlab/cca-genrevive-global/genrevive#3-setting-up-a-virtual-environment).
   >**NOTE:** This step has to be repeated in this repository even after executing it in the [GenRevive](https://devon.s2-eu.capgemini.com/gitlab/cca-genrevive-global/genrevive) repository. Each repository has a separate virtual environment.
3. Install dependencies using Poetry, as described in the chapter [Installing and Configuring Poetry](https://devon.s2-eu.capgemini.com/gitlab/cca-genrevive-global/genrevive#4-installing-and-configuring-poetry).
   >**NOTE:** Poetry does not need to be installed again. Simply call `poetry lock` and `poetry install` in this repository.
4. Fix an issue with the current CrewAI framework (`^0.28.8`) by using the bugfix described in the [Genrevive Migrator Template](https://devon.s2-eu.capgemini.com/gitlab/cca-genrevive-global/genrevive-migrator-template) under [CrewAI Bugfix 1](https://devon.s2-eu.capgemini.com/gitlab/cca-genrevive-global/genrevive-migrator-template#crewai-bugfix-1-using-callback-option-for-tasks-callback-is-not-triggered). Make sure to make the change in the virtual environment of <b>this</b> repository.
5. Install Required Tools: Ensure Java (version 21), Maven, and Spring Boot CLI are installed. For detailed installation instructions, refer to the [Required CLI Tools and Packages](#install-required-cli-tools-and-packages) section.
6. Run the migrator by executing:
   ```bash
   py main.py
   ```

### Install Required CLI Tools and Packages

If you want to run the migrator locally, ensure that the following tools are installed:

#### Java (Version 21)
- Download [Java 21](https://www.oracle.com/de/java/technologies/downloads/#java21) and follow the official [installation instructions](https://docs.oracle.com/en/java/javase/21/install/overview-jdk-installation.html).
- Verify installation:
   ```bash
   java -version
   ```

#### Maven
- Download [Apache Maven](https://maven.apache.org/download.cgi) and follow the official [installation instructions](https://maven.apache.org/install.html).
- Verify installation:
   ```bash
   mvn -v
   ```

#### Spring Boot CLI
- Download and install from the official Spring website: [Spring Boot CLI](https://docs.spring.io/spring-boot/installing.html#getting-started.installing.cli).
- Verify installation:
   ```bash
   spring --version
   ```

## Configuration

This migrator requires configuration of several environment variables predefined in the following files:
* `./.env.template`
* `./activities/.env.template`
* `./activities/entity_generator/.env.template`
* `./activities/integration_test_generator/.env.template`

For each of these files, a separate `.env` file needs to be created in the same folder and configuration values need to be adjusted there as needed. Many variables in the template files have a predetermined default value, which can be used if no special requirement exists. Please refer to the documentation of each configuration parameter to decide whether the default value needs to be adjusted for your use case.

The documentation for common configuration parameters is described in the [Migrator Template repository](https://devon.s2-eu.capgemini.com/gitlab/cca-genrevive-global/genrevive-migrator-template#configuration).

Configuration parameters specific to this migrator are described in the following tables.

### Global configuration parameters

The following parameters need to be set in the root level `.env` file:

| Environment Variable                  | Required | Description                                                                                                                                                                                                                                                                                 | Valid Values | Example                                                                            |
|:--------------------------------------|:--------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------:|:-----------------------------------------------------------------------------------|
| `LOCAL_GENREVIVE_PATH`                |    No    | Path to your GenRevive repository folder. Only necessary if the migrator runs in a Docker container.                                                                                                                                                                                        |    String    | `../genrevive`                                                                     |
| `LOCAL_ADF_PROJECT_PATH`              |    No    | Path to your local input ADF project directory. Only necessary if the migrator runs in a Docker container and will therefore be different from the `ADF_PROJECT_PATH`, which refers to the working directory of the migrator. This value needs to be an absolute path.                      |    String    | `C:/genrevive-examples/ADF/Summit/Input`                                           |
| `ADF_PROJECT_PATH`                    |   Yes    | Path to your input ADF project directory. Refers to your local directory, if running locally. Otherwise refers to the directory inside of the migrator container. In this case, this value needs to be an absolute path.                                                                    |    String    | `/home/adfproject`                                                                 |
| `ADF_SCHEMA_SQL_FILE`                 |   Yes    | File to your ADF database SQL schema.                                                                                                                                                                                                                                                       |    String    | `${ADF_PROJECT_PATH}/SummitADF_Schema1221/Database/scripts/schema.sql`             |
| `ADF_INSERT_SQL_PATH`                 |   Yes    | Path to your ADF database SQL insert statements.                                                                                                                                                                                                                                            |    String    | `${ADF_PROJECT_PATH}/SummitADF_Schema1221/Database/scripts/data`                   |
| `ADF_SCHEMA_NAME`                     |   Yes    | The schema name in the ADF database. Can be left empty if no tablespace name is used.                                                                                                                                                                                                       |    String    | `""`                                                                               |
| `SPRINGBOOT_PROJECT_NAME`             |   Yes    | Name of you output SpringBoot project.                                                                                                                                                                                                                                                      |    String    | `spring-boot-template`                                                             |
| `SPRINGBOOT_PROJECTS_DIRECTORY`       |   Yes    | Path to your output SpringBoot projects directory.                                                                                                                                                                                                                                          |    String    | `./spring-boot-projects`                                                           |
| `SPRINGBOOT_PROJECT_PATH`             |   Yes    | Path to your output SpringBoot project.                                                                                                                                                                                                                                                     |    String    | `${SPRINGBOOT_PROJECTS_DIRECTORY}/${SPRINGBOOT_PROJECT_NAME}`                      |
| `LOCAL_SPRINGBOOT_PROJECTS_DIRECTORY` |    No    | Path to your local output SpringBoot project directory. Only necessary if the migrator runs in a Docker container and will therefore be different from the `SPRINGBOOT_PROJECTS_DIRECTORY`, which refers to the working directory of the migrator. This value needs to be an absolute path. |    String    | `C:/spring-boot-projects`                                                          |
| `LOCAL_SPRINGBOOT_PROJECT_PATH`       |    No    | Path to your local output SpringBoot project. Only necessary if the migrator runs in a Docker container and will therefore be different from the `SPRINGBOOT_PROJECT_PATH`, which refers to the working directory of the migrator. This value needs to be an absolute path.                 |    String    | `${SPRINGBOOT_PROJECTS_DIRECTORY}/${SPRINGBOOT_PROJECT_NAME}`                      |
| `M2_REPO_PATH`                        |   Yes    | Path to your .m2 repository. If the specified path does not exist, a new folder will be created where the Maven dependencies, plugins and other artifacts will be stored.                                                                                                                   |    String    | `.m2`                                                                              |
| `JAVA_PROJECT_PATH`                   |   Yes    | Path to the Java source code in the target project.                                                                                                                                                                                                                                         |    String    | `${SPRINGBOOT_PROJECT_PATH}/src/main/java`                                         |
| `SPRINGBOOT_SCHEMA_SQL_FILE`          |   Yes    | The path to the sql file containing the schema to be used in execution.                                                                                                                                                                                                                     |    String    | `${SPRINGBOOT_PROJECT_PATH}/src/main/resources/db/changelog/1.0.0/changelog-1.sql` |
| `SPRINGBOOT_INSERT_SQL_FILE`          |   Yes    | The path to the sql file with test data to be used in tests.                                                                                                                                                                                                                                |    String    | `${SPRINGBOOT_PROJECT_PATH}/src/main/resources/db/changelog/1.0.0/changelog-2.sql` |
| `ORACLE_PASSWORD`                     |    No    | The password to be used for the connection to the Oracle database, can be any random string. Only necessary if the migrator runs in a Docker container.                                                                                                                                     |    String    | `t2IHu5gSqNKofgYE7keO`                                                             |
| `BASE_PACKAGE_NAME`                   |   Yes    | The root package for your Spring Boot project.                                                                                                                                                                                                                                              |    String    | `com.example.myapp`                                                                |
| `MODEL_PACKAGE_NAME`                  |   Yes    | The package name to be used for the model entities.                                                                                                                                                                                                                                         |    String    | `${BASE_PACKAGE_NAME}.entities`                                                    |
| `REPOSITORY_PACKAGE_NAME`             |   Yes    | The package name to be used for the repositories.                                                                                                                                                                                                                                           |    String    | `${BASE_PACKAGE_NAME}.repositories`                                                |
| `DTO_PACKAGE_NAME`                    |   Yes    | The package name to be used for the DTOs.                                                                                                                                                                                                                                                   |    String    | `${BASE_PACKAGE_NAME}.dtos`                                                        |
| `SERVICE_PACKAGE_NAME`                |   Yes    | The package name to be used for the services.                                                                                                                                                                                                                                               |    String    | `${BASE_PACKAGE_NAME}.services`                                                    |
| `CONTROLLER_PACKAGE_NAME`             |   Yes    | The package name to be used for the controllers.                                                                                                                                                                                                                                            |    String    | `${BASE_PACKAGE_NAME}.controllers`                                                 |

### Configuration parameters for activities

The following parameters need to be set in the `.env` file under the path `./activities`:

| Environment Variable | Required | Description                                 | Valid Values | Example                                           |
|:---------------------|:--------:|:--------------------------------------------|:------------:|:--------------------------------------------------|
| `SE_PROMPT_FILE`     |   Yes    | The path to the software engineer prompt.   |    String    | `${GENERATOR_HOME_PATH}/prompts/se_prompt.md`     |
| `SE_COOKBOOK_FILE`   |   Yes    | The path to the software engineer cookbook. |    String    | `${GENERATOR_HOME_PATH}/cookbooks/se_cookbook.md` |
| `SR_PROMPT_FILE`     |   Yes    | The path to the software reviewer prompt.   |    String    | `${GENERATOR_HOME_PATH}/prompts/sr_prompt.md`     |
| `SR_COOKBOOK_FILE`   |   Yes    | The path to the software reviewer cookbook. |    String    | `${GENERATOR_HOME_PATH}/cookbooks/sr_cookbook.md` |
| `DEVOPS_PROMPT_FILE` |   Yes    | The path to the devops prompt.              |    String    | `${GENERATOR_HOME_PATH}/prompts/devops_prompt.md` |

### Configuration parameters for the entity generator

The following parameters need to be set in the `.env` file under the path `./activities/entity_generator`:

| Environment Variable     | Required | Description                        | Valid Values | Example                                               |
|:-------------------------|:--------:|:-----------------------------------|:------------:|:------------------------------------------------------|
| `TRANSITIVE_PROMPT_FILE` |   Yes    | The path to the transitive prompt. |    String    | `${GENERATOR_HOME_PATH}/prompts/transitive_prompt.md` |
### Configuration parameters for the integration test generator

The following parameters need to be set in the `.env` file under the path `./activities/integration_test_generator`:

| Environment Variable              | Required | Description                                    | Valid Values | Example                                                        |
|:----------------------------------|:--------:|:-----------------------------------------------|:------------:|:---------------------------------------------------------------|
| `NATIVE_QUERY_PROMPT_FILE`        |   Yes    | The path to the native query prompt.           |    String    | `${GENERATOR_HOME_PATH}/prompts/native_query_prompt.md`        |
| `MODIFY_NATIVE_QUERY_PROMPT_FILE` |   Yes    | The path to an additional native query prompt. |    String    | `${GENERATOR_HOME_PATH}/prompts/modify_native_query_prompt.md` |
