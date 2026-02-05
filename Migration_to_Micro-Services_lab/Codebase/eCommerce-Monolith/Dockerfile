# --- Stage 1: Build the Application ---
# Use a Maven image based on Eclipse Temurin 17
FROM maven:3.9-eclipse-temurin-17 AS build
WORKDIR /app

# Copy project files
COPY pom.xml .
COPY src ./src

# Build the application
RUN mvn clean package -DskipTests

# --- Stage 2: Run the Application ---
# Use the lightweight JRE version of Eclipse Temurin 17
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app

# Copy only the built JAR from the previous stage
COPY --from=build /app/target/*.jar app.jar

# Expose the port
EXPOSE 8080

# Command to run
ENTRYPOINT ["java", "-jar", "app.jar"]