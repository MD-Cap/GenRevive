FROM python:3.12-bookworm
SHELL ["/bin/bash", "-c"]
WORKDIR /home/adf2spring

COPY . .
COPY --from=genrevive . /home/genrevive

# Create folder for migrator output
RUN sed -i 's/\r$//' .env
RUN source .env && mkdir -p $SPRINGBOOT_PROJECTS_DIRECTORY

# No longer needed for image build; Environment variables will be pass to the running container
RUN rm .env

# Install Java, Maven & Spring Boot CLI
RUN apt update && apt install -y zip
RUN curl -s "https://get.sdkman.io" | bash
RUN source "/root/.sdkman/bin/sdkman-init.sh"   \
                && sdk install java 21.0.2-open  \
                && sdk install maven 3.9.9 \
                && sdk install springboot 3.3.3
ENV PATH=/root/.sdkman/candidates/java/current/bin:$PATH
ENV PATH=/root/.sdkman/candidates/maven/current/bin:$PATH
ENV PATH=/root/.sdkman/candidates/springboot/current/bin:$PATH

# Create a virtual environment and activate it for further commands
ENV VIRTUAL_ENV=venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install Poetry & dependencies
RUN pip install poetry==1.8.3
RUN poetry lock && poetry install

# Fix bug in crewAI library
RUN sed -i 's/\s*task\.callback\s\=\sself\.task_callback/            self.task_callback = task.callback/' venv/lib/python3.12/site-packages/crewai/crew.py

ENTRYPOINT ["/bin/bash", "-c", "python3 main.py"]


