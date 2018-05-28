pipeline {
  agent {
    dockerfile {
      filename 'Dockerfile'
    }

  }
  stages {
    stage('test') {
      steps {
        sh 'pwd'
      }
    }
    stage('staging') {
      steps {
        echo 'testing in develop environment'
      }
    }
  }
}