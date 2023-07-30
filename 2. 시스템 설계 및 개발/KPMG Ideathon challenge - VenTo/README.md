# 2023 KPMG IDEATHON

![KakaoTalk_Image_2023-02-19-18-02-08](https://user-images.githubusercontent.com/79076958/219938825-eed986cc-be25-4745-bf57-e2b1d5599966.png)

 
<div>
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white">
<img src="https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white">
<img src="https://img.shields.io/badge/numpy-013243?style=for-the-badge&logo=numpy&logoColor=white">
<img src="https://img.shields.io/badge/GitHub Actions-2088FF?style=for-the-badge&logo=Github Actions&logoColor=white">
<br>
<img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=PyTorch&logoColor=white">
<img src="https://img.shields.io/badge/react-61DAFB?style=for-the-badge&logo=react&logoColor=white">
<img src="https://img.shields.io/badge/flask-000000?style=for-the-badge&logo=flask&logoColor=white">
<img src="https://img.shields.io/badge/scikitlearn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white">
</div>
<br>
<br>


#### VenTo is a platforrm that serves ventures or venture-like companies with three unique services to overcome their limitations.

#### Difficulties for venture companies to raise funds / Difficulties in dealing with legal provisions / Difficulties in seeking overseas expansion 

---
## Services

### 1. R&D Together
"R&D Together" deals with financial limitations venture firms are facing by supporting the appliance of R&D projects financed by the government.

### 2. Contract Together
"Contract Together" deals with toxic probable clauses in contract papers. This service model contracts the clauses in contract papers and distinguishes toxic probable clauses.     

### 3. Issue Together
"Issue Together" supports for the globalization of K-venture companies through customized domestic and international news and issue provision services and introduction of overseas expansion support projects

---
## About our team

|Github|Project Contributions|
|--------|--------|
|[SEJEONG KANG](https://github.com/SEJEONGKANG)|Lead, Contract Together Modeling|
|[JIHYO KIM](https://github.com/Jihyozhixiao)|R&D Together Modeling \& Designs|
|[JUNHO NA](https://github.com/junho328)|Contract Together Modeling \& Web Backend(flask)|
|[YUCHAN PARK](https://github.com/chanchanuu)|Issue Together Modeling \& Web Frontend(React)|
|[JUNWOO AHN](https://github.com/anjunwoo990809)|Issue Together Modeling \& Web Backend(DB)|
|[DONGHYUN JANG](https://github.com/rroyc20)|R&D Together Modeling \& Web Frontend(React)|

---
## Models

|Service|Model (HuggingFace link) |
|--------|--------|
|R&D Together|[rroyc20/RnD-base-tokenizer-mDeBERTa-v3-kor-further](https://huggingface.co/rroyc20/RnD-base-tokenizer-mDeBERTa-v3-kor-further) / [jhgan/ko-sbert-sts](https://huggingface.co/jhgan/ko-sbert-sts)|
|Contract Together|[jhn9803/Contract-base-tokenizer-mDeBERTa-v3-kor-further](https://huggingface.co/jhn9803/Contract-base-tokenizer-mDeBERTa-v3-kor-further) / [jhn9803/Contract-new-tokenizer-mDeBERTa-v3-kor-further](https://huggingface.co/jhn9803/Contract-new-tokenizer-mDeBERTa-v3-kor-further)|
|Issue Together|[sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) / [facebook/bart-large-mnli](https://huggingface.co/facebook/bart-large-mnli)|

---
## How to Run

1. `git clone https://github.com/SEJEONGKANG/KPMG-VenTo.git`

2. Terminal
   
   ```
   # ~/KPMG-VenTo/frontend
   $ npm install --legacy-peer-deps
   $ npm run dev
   ```

   for MacOS user
   ```
   # ~/KPMG-VenTo/backend
   $ python -m venv venv
   $ source venv/bin/activate
   $ pip install -r requirements.txt
   $ flask run
   ```
   
   for Windows user
   ```
   # ~/KPMG-VenTo/backend
   $ python -m venv venv
   $ .\venv\Scripts\activate
   $ pip install -r requirements.txt
   $ flask run
   ```

3. add similar into KPMG-VenTo\backend\torchs

   [download link](https://drive.google.com/drive/folders/1518Vy7GTzgbM64BTmWpdYPhAu_B0uumZ?usp=sharing)

5. Run on Local Server: http://localhost:3000


