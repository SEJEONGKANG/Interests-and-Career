FROM node:14
WORKDIR /app/frontend

COPY ./package.json /app/frontend
RUN npm install
# 현재 디렉토리의 모든 파일을 도커 컨테이너의 워킹 디렉토리에 복사
COPY . /app/frontend
EXPOSE 8000

# npm start 스크립트 실행
CMD ["npm", "start"]