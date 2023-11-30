void setBuildStatus(String message, String state, String context) {
    step([
        $class: "GitHubCommitStatusSetter",
        reposSource: [$class: "ManuallyEnteredRepositorySource", url: "https://github.com/Zerohertz/docker"],
        contextSource: [$class: "ManuallyEnteredCommitContextSource", context: context],
        errorHandlers: [[$class: "ChangingBuildStatusErrorHandler", result: "UNSTABLE"]],
        statusResultSource: [ $class: "ConditionalStatusResultSource", results: [[$class: "AnyBuildResult", message: message, state: state]] ]
    ]);
}

pipeline {
    agent {
        kubernetes {
            yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    jenkins/agent-type: kaniko
spec:
  containers:
    - name: jnlp
      image: jenkins/inbound-agent:latest
      resources:
        requests:
          memory: "512Mi"
          cpu: "500m"
        limits:
          memory: "1024Mi"
          cpu: "1000m"
    - name: ubuntu
      image: ubuntu:latest
      command:
        - sleep
      args:
        - "infinity"
      resources:
        requests:
          memory: "512Mi"
          cpu: "500m"
        limits:
          memory: "1024Mi"
          cpu: "1000m"
    - name: kaniko
      image: gcr.io/kaniko-project/executor:debug
      command:
        - /busybox/cat
      tty: true
      resources:
        requests:
          memory: "2048Mi"
          cpu: "2000m"
        limits:
          memory: "4096Mi"
          cpu: "4000m"
      volumeMounts:
        - name: docker-config
          mountPath: /kaniko/.docker/
  volumes:
    - name: docker-config
      secret:
        secretName: docker-config
            """
        }
    }
    environment {
        DOCKERHUB_USERNAME = "zerohertzkr"
        CHANGE_PATTERNS = "airflow-*" // ${DIR_NAME}-*,${DIR_NAME}-*,...
        DEFAULT_TAG = "v1.0.0"
    }
    stages {
        stage("Detect Changes") {
            steps {
                script {
                    try {
                        setBuildStatus("Detact...", "PENDING", "$STAGE_NAME")
                        def patterns = env.CHANGE_PATTERNS.split(",")
                        def regex = patterns.collect { it.trim() }.join("|")
                        changedDirs = sh(script: "git diff --name-only HEAD^ HEAD | grep -E '${regex}' | xargs -r -n 1 dirname | uniq", returnStdout: true).trim().split("\n")
                        slackSend(color: "good", message: ":+1:  <${env.BUILD_URL}|[${env.JOB_NAME}: ${STAGE_NAME}]> SUCCESS\nBRANCH NAME: ${env.BRANCH_NAME}\nChange Dirs: ${changedDirs}")
                        setBuildStatus("Success", "SUCCESS", "$STAGE_NAME")
                    } catch (Exception e) {
                        def STAGE_ERROR_MESSAGE = e.getMessage().split("\n")[0]
                        setBuildStatus(STAGE_ERROR_MESSAGE, "FAILURE", "$STAGE_NAME")
                        slackSend(color: "danger", message: ":-1:  <${env.BUILD_URL}|[${env.JOB_NAME}: ${STAGE_NAME}]> SUCCESS\nBRANCH NAME: ${env.BRANCH_NAME}\nError Message: ${STAGE_ERROR_MESSAGE}")
                        throw e
                    }
                }
            }
        }
        stage("Kaniko") {
            when {
                expression {
                    return changedDirs != [""]
                }
            }
            steps {
                script {
                    container("ubuntu") {
                        sh """
                            apt-get update
                            apt-get install -y curl jq
                        """
                    }
                    for (dir in changedDirs) {
                        def imageName = dir.replaceAll("/", "-")
                        def newTag = ""
                        container("ubuntu") {
                            def apiResponse = sh(script: """
                                curl -s "https://hub.docker.com/v2/repositories/${DOCKERHUB_USERNAME}/${imageName}/tags/?page_size=100"
                            """, returnStdout: true).trim()
                            if (apiResponse.contains("httperror 404")) {
                                newTag = env.DEFAULT_TAG
                            } else {
                                def currentTag = sh(script: "echo '${apiResponse}' | jq -r '.results[].name' | sort -V | tail -n 1", returnStdout: true).trim()
                                try {
                                    def (major, minor, patch) = currentTag.tokenize(".").collect { it.toInteger() }
                                    newTag = "v${major}.${minor}.${patch + 1}"
                                } catch (Exception e) {
                                    newTag = env.DEFAULT_TAG
                                }
                            }
                        }
                        container("kaniko") {
                            script {
                                def dockerfile = "Dockerfile"
                                def image = "${DOCKERHUB_USERNAME}/${imageName}:${newTag}"
                                try {
                                    setBuildStatus("Build...", "PENDING", "$STAGE_NAME: $image")
                                    sh ""
                                    sh "/kaniko/executor --context ${dir} --dockerfile ${dir}/${dockerfile} --destination ${image}"
                                    setBuildStatus("Success", "SUCCESS", "$STAGE_NAME: $image")
                                    slackSend(color: "good", message: ":+1:  <${env.BUILD_URL}|[${env.JOB_NAME}: ${STAGE_NAME}]> SUCCESS\nBRANCH NAME: ${env.BRANCH_NAME}\nIMAGE: <https://hub.docker.com/repository/docker/zerohertzkr/${imageName}/general|${image}>")
                                } catch (Exception e) {
                                    def STAGE_ERROR_MESSAGE = e.getMessage().split("\n")[0]
                                    setBuildStatus(STAGE_ERROR_MESSAGE, "FAILURE", "$STAGE_NAME: $image")
                                    slackSend(color: "danger", message: ":-1:  <${env.BUILD_URL}|[${env.JOB_NAME}: ${STAGE_NAME}]> SUCCESS\nBRANCH NAME: ${env.BRANCH_NAME}\nIMAGE: ${image}\nError Message: ${STAGE_ERROR_MESSAGE}")
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
