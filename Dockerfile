FROM            python:3.6.5-slim

MAINTAINER      lockstom2@gmail.com

# uwsgi는 Pipfile에 기록
RUN             apt -y update && apt -y dist-upgrade
RUN             apt -y install build-essential
RUN             apt -y install nginx supervisor

#

# 로컬의 requirement.txt 파이을 /srv 에 복사 후 pip install 실행
# (build 하는 한경에 requirements.txt 가 있어야 함)
COPY            ./requirements.txt  /srv/
RUN             pip install -r /srv/requirements.txt

ENV             PROJECT_DIR             /srv/project
ENV             BUILD_MODE              production
ENV             DJANGO_SETTINGS_MODULE  config.settings.${BUILD_MODE}

COPY            .   ${PROJECT_DIR}
RUN             mkdir   /var/log/django
#WORKDIR         ${PROJECT_DIR}



# Nginx 설정파일들 복사 미 enabled로 링크
                # avaiable에 있는 파일 복사
RUN             cp -f   ${PROJECT_DIR}/.config/${BUILD_MODE}/nginx.conf \
                        /etc/nginx/nginx.conf &&\

                # avaiable 에 nginx_app.conf 파일 복사
                cp -f   ${PROJECT_DIR}/.config/${BUILD_MODE}/nginx_app.conf \
                        /etc/nginx/sites-available/ && \
                # 이미 sites-enabled 에 있던 모든 내용 삭제
#                rm -f   /etc/nginx/sites-enabled/* &&\

                # 링크 연결
                ln -sf  /etc/nginx/sites-available/nginx_app.conf \
                    /etc/nginx/sites-enabled

# supervisor 설정 복사
RUN             cp -f   ${PROJECT_DIR}/.config/${BUILD_MODE}/supervisor_app.conf \
                    /etc/supervisor/conf.d/

# 7000번 포트 open
EXPOSE          7000

# Run supervisord
CMD             supervisord -n