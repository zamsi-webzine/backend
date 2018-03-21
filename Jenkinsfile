node {
    stage ('Checkout Stage') {
        checkout scm
    }

    stage ('Install virtualenv Stage') {
        sh '''
            sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
                libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
                xz-utils tk-dev
            curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
            PATH=/root/.pyenv/bin:$PATH
            pyenv install 3.6.3
            echo 'export PATH="/root/.pyenv/bin:$PATH"' >> ~/.bashrc
            echo 'eval "$(pyenv init -)"' >> ~/.bashrc
            echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
            pyenv virtualenv 3.6.3 zamsee-back
            pyenv local zamsee-back
        '''
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
