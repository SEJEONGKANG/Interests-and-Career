# Extract-audit-opinion ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) ![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB) ![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white) ![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)
This project is part of KIC 2023 Summer Internship. The project aims to find out whether auditor of certain company has been changed or not in current term. We checked auditor's opinion in reports such as business reports or quarterly reports through [DART](https://dart.fss.or.kr/). We mainly used [DART OpenAPI](https://opendart.fss.or.kr/intro/main.do) to download reports and processed them into xml in order to extract information we wanted.

## Participants
| Name | Role | Major | 
| :---: | :---: | :---: 
| Sejeong Kang | Data Pipeline, Backend, Database | Industrial Engineering / Applied Statistics |
| Donghyun Chang | Logic Construction, Frontend | Industrial Engineering |

## Overview
<p align="center">
  <img src="https://github.com/kic-sr/Extract-audit-opinion/assets/139308805/a816ba65-5e21-4af0-96ee-726e61bd79f4"/>
</p> 

Please refer to the [`notion`](https://www.notion.so/kpmgkr/SR-da3885da0f284fcda9983a21590abb33?pvs=4) for detailed explanations and procedures.

## Data Pipeline
### Apache Airflow
<p align="center">
  <img src="https://github.com/kic-sr/Extract-audit-opinion/assets/139308805/c7594402-b364-46d8-beb1-d96fe9ad9449"/>
  Airflow Workflow
</p> 
We first download and process yesterday's data using Apache Airflow. Once the data is downloaded, the airflow dag is activated and process the xml contents. After finishing processing, then the processed data are pushed to MySQL database. This process is done in a daily cycle, and if you want to download past data, you can run below file.

[`main_past_data.py`](https://github.com/kic-sr/Extract-audit-opinion/blob/main/batch/dags/main_past_data.py)


### MySQL
<p align="center">
  <img style="margin:50px 0 10px 0 width=100%" src="https://github.com/kic-sr/Extract-audit-opinion/assets/139330944/0c38f6b6-9702-4bce-a750-7b2b46b1d6be"/>
  Database ERD
</p>

When the data is pushed to the databse daily, it provokes trigger that determines whether the company was designated for the report year or not. If it is, then the trigger saves the corporation code and the designated year.

### FastAPI
![image](https://github.com/kic-sr/Extract-audit-opinion/assets/139308805/4d3f91b4-b49a-4e77-ab38-c9bfa9e4f4cf)
We have created the necessary functionalities as APIs and organized them using separate routers for each feature.
- analysis_router.py : Router containing APIs related to company analysis.
- contact_router.py : Router containing APIs related to potential customer management.
- info_router.py : Router containing APIs related to company information.
- starred_router.py : Router containing APIs related to bookmarking.
- user_router.py : Router containing APIs related to user (login) management.

## Logic
We first extracted all the tables in the auditor-related section. Once we extracted the tables, we then checked whether the tables contain headers and bodies. If the tables don't have headers, we checked the first two rows of the table and made it the headers. Then, we checked if "auditor" is in one of the header columns or not.

If "auditor" is in the header, then we added it to an array. We checked the first table of the array, because the first table of the array mostly seems to contain current auditor, previous auditor, and auditor two years ago (some exceptions do exist, so we did some exception handling). From the first table of the array, we obtained the information of the auditor for 3 years.

We checked if the auditor for the current year (the year the report was written) and the auditor for the previous year are the same or not. By doing this, we successfully checked the auditor change.

Furthermore, we tried to understand the intention of the request and found out that the auditors wanted to check whether the corporations were designated auditors by the FINANCIAL SUPERVISORY SERVICE (금융감독원), or the corporations can freely designate auditors.

Thus, we tried to develop the logic to check whether the corporation was designated or not in the year the report was written. We used [NER (Named Entity Recognition)](https://huggingface.co/xlm-roberta-large-finetuned-conll03-english) to recognize organizations in the "감사인의 변경 여부" text.

If the auditor for the current year was recognized by the model and the text contains wording that can be a basis for designation, such as "11조," "증권선물위원회," "금융감독원," "지정감사," "상장" (these words were collected based on [외부감사법](https://www.law.go.kr/%EB%B2%95%EB%A0%B9/%EC%A3%BC%EC%8B%9D%ED%9A%8C%EC%82%AC%EB%93%B1%EC%9D%98%EC%99%B8%EB%B6%80%EA%B0%90%EC%82%AC%EC%97%90%EA%B4%80%ED%95%9C%EB%B2%95%EB%A5%A0)), we considered such corporations designated for the year the report was written.

We saved the information of the corporation code and designated year in the MySQL database and used it to find the potential target of audit for the next year. If the auditors for this year and the latest two years are the same, and if any of the three years was classified as a designated year, then we added such corporation to the target corporation list and viewed them on the web.

## How to Use
1. If you have docker desktop, initialize it. If not, download it from the [link](https://www.docker.com/products/docker-desktop/) and initialize it.
2. Download all the files from git using download .zip or below code
```bash
gh repo clone kic-sr/Extract-audit-opinion
```
3. Once you've downloaded all the files, turn on CMD in /batch
4. Build image for airflow container
```cmd
docker build -t sr_airflow_image .
```
3. change repository to the Extract-audit-opinion
4. Docker Compose
```cmd
docker-compose up -d
```
5. You're ready to go!
## References
