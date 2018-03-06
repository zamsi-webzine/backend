# 이미지
FROM        lanark/zamsee-base:latest
# 유저
MAINTAINER  dfg1499@gmail.com
# 언어 환경 설정
ENV         LANG C.UTF-8
ENV         DJANGO_SETTINGS_MODULE config.settings.dev

# 현재 폴더 전체를 /srv/app에 복사
COPY        . /srv/app
# requirememts 설치
RUN         /root/.pyenv/versions/app/bin/pip install -r \
            /srv/app/requirements.txt

# pyenv 환경 설정
WORKDIR     /srv/app
RUN         pyenv local app

# Nginx
# Nginx 메인 설정 파일을 복사
RUN         cp /srv/app/.config/nginx/base/nginx.conf /etc/nginx/nginx.conf
# 어플리케이션 용 Nginx 파일을 비활성 폴더로 복사
RUN         cp /srv/app/.config/nginx/production/app.conf /etc/nginx/sites-available/
# 기존 활성 폴더를 삭제
RUN         rm -rf /etc/nginx/sites-enabled/*
# 새로 활성 폴더를 만들고 어플리케이션 용 Ngnix 설정 파일을 심볼릭 링크로 연결
RUN         ln -sf /etc/nginx/sites-available/app.conf \
                    /etc/nginx/sites-enabled/app.conf

# uWSGI
# log directory 생성
RUN         mkdir -p /var/log/uwsgi/app

# Supervisor
# 설정 파일 복사
RUN         cp /srv/app/.config/supervisor/base/* \
                /etc/supervisor/conf.d/
RUN         cp /srv/app/.config/supervisor/production/* \
                /etc/supervisor/conf.d/
# foreground 실행
CMD         supervisord -n

# Port open
EXPOSE      80
EXPOSE      5432
