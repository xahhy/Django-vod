pipeline {
  agent {
    docker {
      image 'ubuntu'
    }

  }
  stages {
    stage('test') {
      steps {
        sh 'pwd && ls -al&&whoami'
      }
    }
  }
}