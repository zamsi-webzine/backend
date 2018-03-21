node {
    stage ('Checkout Stage') {
        checkout scm
    }

    stage ('Install virtualenv Stage') {
        sh 'source ~/.bashrc'
        sh 'pyenv local zamsee-back'
    }

    stage('Install Application Dependencies') {
        sh 'pip install -r requirements/local.txt'
    }

    stage ('Unzip Secrets Stage') {
        sh 'unzip -o -P $PASSWORD_ZIP secrets.zip'
    }

    stage ('Test Stage') {
        def testsError = null
        try {
            sh 'python ./zamsee-back/manage.py jenkins'
        }
        catch(err) {
            testsError = err
            currentBuild.result = 'FAILURE'
        }
        finally {
            if (testsError) {
                throw testsError
            }
        }
    }
}
