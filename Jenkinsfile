node {
    stage ('Checkout Stage') {
        checkout scm
    }

    stage('Install Application Dependencies') {
        sh 'source /home/ubuntu/.bashrc'
        sh '/home/ubuntu/.pyenv/libexec/pyenv global 3.6.3'
        sh '/home/ubuntu/.pyenv/libexec/pyenv local zamsee-back'
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
